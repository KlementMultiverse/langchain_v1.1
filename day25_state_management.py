"""
State Management - AI Agent with Persistent Memory

This demonstrates how AI agents can remember user preferences across
different conversation sessions using state management.

Module: 2.2 State Management
Pattern: Persistent memory with thread_id
Key Concept: State persists across sessions, Context does not
"""

import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent, AgentState
from langchain.tools import tool, ToolRuntime
from langgraph.types import Command
from langgraph.checkpoint.memory import InMemorySaver
from langchain.messages import HumanMessage, ToolMessage
from pprint import pprint

load_dotenv()


# Define custom state schema (inherits from AgentState for 'messages' field)
class UserPreferences(AgentState):
    favourite_colour: str


# Tool that WRITES to state
@tool
def save_favourite_colour(favourite_colour: str, runtime: ToolRuntime) -> Command:
    """Save the user's favourite colour to persistent state"""
    return Command(update={
        "favourite_colour": favourite_colour,
        "messages": [ToolMessage(
            f"Saved your favourite colour: {favourite_colour}",
            tool_call_id=runtime.tool_call_id
        )]
    })


# Tool that READS from state
@tool
def get_favourite_colour(runtime: ToolRuntime) -> str:
    """Retrieve the user's favourite colour from persistent state"""
    try:
        return f"Your favourite colour is {runtime.state['favourite_colour']}"
    except KeyError:
        return "No favourite colour found in state"


async def main():
    print("=" * 70)
    print("STATE MANAGEMENT - PERSISTENT MEMORY DEMO")
    print("=" * 70)

    # Create agent with state schema and checkpointer
    agent = create_agent(
        model="gpt-4o-mini",
        tools=[save_favourite_colour, get_favourite_colour],
        checkpointer=InMemorySaver(),  # Required for state persistence
        state_schema=UserPreferences
    )

    print("\n📝 SESSION 1: User reveals preference")
    print("-" * 70)

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="My favourite colour is green")]},
        {"configurable": {"thread_id": "user_123"}}
    )

    print(f"🤖 Agent: {response['messages'][-1].content}")
    print(f"💾 State saved with thread_id: user_123")

    print("\n⏰ Time passes... (simulating days later)")

    print("\n📝 SESSION 2: Different conversation, same user")
    print("-" * 70)

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="What's my favourite colour?")]},
        {"configurable": {"thread_id": "user_123"}}  # Same thread_id!
    )

    print(f"🤖 Agent: {response['messages'][-1].content}")
    print(f"✅ Agent remembered from previous session!")

    print("\n📝 SESSION 3: Different user (different thread_id)")
    print("-" * 70)

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content="What's my favourite colour?")]},
        {"configurable": {"thread_id": "user_456"}}  # Different thread_id
    )

    print(f"🤖 Agent: {response['messages'][-1].content}")
    print(f"❌ No memory for this user (different thread_id)")

    print("\n" + "=" * 70)
    print("✅ State Management Complete")
    print("\n💡 Key Concepts:")
    print("   - State persists across sessions (unlike Context)")
    print("   - thread_id identifies unique users/conversations")
    print("   - Tools WRITE with Command(update={...})")
    print("   - Tools READ with runtime.state['key']")
    print("   - Checkpointer required for persistence")
    print("   - Production: Use PostgreSQLSaver instead of InMemorySaver")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
