"""
Multi-Agent Wedding Planner - Coordinator-Specialist Pattern

Demonstrates multi-agent coordination with state management.
Coordinator agent delegates tasks to three specialist subagents:
- Travel agent (MCP flight search)
- Venue agent (web search)
- Playlist agent (SQL database)

Module: 2.4 Wedding Planner
Pattern: Coordinator delegates to specialists, state management with runtime tools
Key Concepts: State schema, Command updates, ToolRuntime, execution order
"""

import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from typing import Dict, Any
from tavily import TavilyClient
from langchain.tools import tool, ToolRuntime
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentState, create_agent
from langchain.messages import HumanMessage, ToolMessage
from langgraph.types import Command
from pprint import pprint

load_dotenv()


# Setup Tools
print("Setting up MCP client...")
client = MultiServerMCPClient({
    "travel_server": {
        "transport": "streamable_http",
        "url": "https://mcp.kiwi.com"
    }
})


async def setup_tools():
    tools = await client.get_tools()
    print(f"Got {len(tools)} MCP tools")
    return tools


# Web Search Tool
tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)


# SQL Database Tool
db = SQLDatabase.from_uri("sqlite:///resources/Chinook.db")

@tool
def query_playlist_db(query: str) -> str:
    """Query the database for playlist information"""
    try:
        return db.run(query)
    except Exception as e:
        return f"Error querying database: {e}"


# Create State
class WeddingState(AgentState):
    origin: str
    destination: str
    guest_count: str
    genre: str


async def main():
    # Get flight tools
    flight_tools = await setup_tools()

    # Create Subagents
    print("\nCreating subagents...")

    travel_agent = create_agent(
        model="gpt-4o-mini",
        tools=flight_tools,
        system_prompt="""
        You are a travel agent. Search for flights to the desired destination wedding location.
        You are not allowed to ask any more follow up questions, you must find the best flight options based on the following criteria:
        - Price (lowest, economy class)
        - Duration (shortest)
        - Date: Choose a specific date for the wedding based on the best time of year for this location
          IMPORTANT: You MUST provide exact date parameters (year and month) when searching.
          Current year is 2026. Pick a month 3-6 months from now that has good weather for a wedding at this destination.
        To make things easy, only look for one ticket, one way.
        You may need to make multiple searches to iteratively find the best options.
        You will be given no extra information, only the origin and destination. It is your job to think critically about the best options.
        Once you have found the best options, let the user know your shortlist of options.
        """
    )

    venue_agent = create_agent(
        model="gpt-4o-mini",
        tools=[web_search],
        system_prompt="""
        You are a venue specialist. Search for venues in the desired location, and with the desired capacity.
        You are not allowed to ask any more follow up questions, you must find the best venue options based on the following criteria:
        - Price (lowest)
        - Capacity (exact match)
        - Reviews (highest)
        You may need to make multiple searches to iteratively find the best options.
        """
    )

    playlist_agent = create_agent(
        model="gpt-4o-mini",
        tools=[query_playlist_db],
        system_prompt="""
        You are a playlist specialist. Query the sql database and curate the perfect playlist for a wedding given a genre.
        Once you have your playlist, calculate the total duration and cost of the playlist, each song has an associated price.
        If you run into errors when querying the database, try to fix them by making changes to the query.
        Do not come back empty handed, keep trying to query the db until you find a list of songs.
        You may need to make multiple queries to iteratively find the best options.
        """
    )

    print("Subagents created!")

    # Create wrapper tools
    @tool
    async def search_flights(runtime: ToolRuntime) -> str:
        """Travel agent searches for flights to the desired destination wedding location."""
        origin = runtime.state["origin"]
        destination = runtime.state["destination"]
        response = await travel_agent.ainvoke({"messages": [HumanMessage(content=f"Find flights from {origin} to {destination}")]})
        return response['messages'][-1].content

    @tool
    def search_venues(runtime: ToolRuntime) -> str:
        """Venue agent chooses the best venue for the given location and capacity."""
        destination = runtime.state["destination"]
        capacity = runtime.state["guest_count"]
        query = f"Find wedding venues in {destination} for {capacity} guests"
        response = venue_agent.invoke({"messages": [HumanMessage(content=query)]})
        return response['messages'][-1].content

    @tool
    def suggest_playlist(runtime: ToolRuntime) -> str:
        """Playlist agent curates the perfect playlist for the given genre."""
        genre = runtime.state["genre"]
        query = f"Find {genre} tracks for wedding playlist"
        response = playlist_agent.invoke({"messages": [HumanMessage(content=query)]})
        return response['messages'][-1].content

    @tool
    def update_state(origin: str, destination: str, guest_count: str, genre: str, runtime: ToolRuntime) -> Command:
        """Update the state when you know all of the values: origin, destination, guest_count, genre"""
        return Command(update={
            "origin": origin,
            "destination": destination,
            "guest_count": guest_count,
            "genre": genre,
            "messages": [ToolMessage("Successfully updated state", tool_call_id=runtime.tool_call_id)]
        })

    # Create Coordinator
    print("\nCreating coordinator...")

    coordinator = create_agent(
        model="gpt-4o-mini",
        tools=[search_flights, search_venues, suggest_playlist, update_state],
        state_schema=WeddingState,
        system_prompt="""
        You are a wedding coordinator.

        CRITICAL: You MUST call update_state() FIRST before doing anything else!
        Extract the origin, destination, guest_count, and genre from the user's message.
        Then call update_state(origin, destination, guest_count, genre).

        Only AFTER the state is updated can you delegate tasks to your specialists:
        - search_flights() for flight options
        - search_venues() for venue options
        - suggest_playlist() for music playlist

        Once you have received their answers, coordinate the perfect wedding plan.
        """
    )

    print("Coordinator created!")

    # Test
    print("\n" + "="*70)
    print("TESTING WEDDING PLANNER")
    print("="*70)

    response = await coordinator.ainvoke({
        "messages": [HumanMessage(content="I'm from London and I'd like a wedding in Paris for 100 guests, jazz-genre")],
    })

    print("\n" + "="*70)
    print("FINAL RESPONSE:")
    print("="*70)
    pprint(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
