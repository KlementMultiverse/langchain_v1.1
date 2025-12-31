"""
Travel Agent - AI Agent using External MCP Server

This program demonstrates connecting to an external MCP server (Kiwi.com)
to search for real flight information using the streamable_http transport.

Course: LangChain Academy - Module 2.1 (Model Context Protocol)
Date: December 30, 2025
Student: Klement

Key Concepts:
- External MCP server connection (streamable_http transport)
- Real-time flight search using Kiwi.com API
- Agent autonomy (AI decides to use search tool)
- Stateless operation (no checkpointer for external MCP)
"""

import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.messages import HumanMessage

# Load environment variables (API keys)
load_dotenv()


async def main():
    """
    Travel Agent that searches for flights using Kiwi.com's MCP server.

    Flow:
    1. Connect to Kiwi.com MCP server via streamable_http
    2. Get available tools (flight search)
    3. Create AI agent with those tools
    4. Ask for flight search
    5. AI autonomously calls search tool
    6. Display formatted results
    """

    print("=" * 70)
    print("🛫 TRAVEL AGENT - AI-Powered Flight Search")
    print("=" * 70)

    # Step 1: Connect to Kiwi.com external MCP server
    print("\n📡 Connecting to Kiwi.com MCP server...")
    client = MultiServerMCPClient(
        {
            "travel_server": {
                "transport": "streamable_http",  # External HTTP transport
                "url": "https://mcp.kiwi.com"     # Kiwi.com's MCP server URL
            }
        }
    )

    # Step 2: Get available tools from the server
    print("🔧 Fetching available tools...")
    tools = await client.get_tools()
    print(f"✅ Got {len(tools)} tools from Kiwi.com server\n")

    # Step 3: Create AI agent with flight search tools
    # NOTE: No checkpointer! External MCP servers don't need memory
    agent = create_agent(
        model="gpt-4o-mini",
        tools=tools,
        system_prompt="You are a travel agent. No follow up questions."
    )

    # Step 4: Search for flights
    print("🔍 Searching for flights: San Francisco → Tokyo (March 31, 2026)...\n")

    response = await agent.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Get me a direct flight from San Francisco to Tokyo on March 31st, 2026"
                )
            ]
        }
    )

    # Step 5: Display results
    print("=" * 70)
    print("✈️  FLIGHT SEARCH RESULTS")
    print("=" * 70)
    print(response["messages"][-1].content)
    print("=" * 70)

    print("\n✅ Travel Agent completed successfully!")
    print("\n💡 Key Learning: External MCP servers (streamable_http) provide")
    print("   powerful tools without writing any backend code!")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
