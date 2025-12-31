"""
Runtime Context - Pass User Data to Tools Without Repeated Database Queries

This demonstrates the Runtime Context pattern where user preferences are fetched
once and passed through context, allowing tools to read from memory instead of
querying the database repeatedly.

Module: 2.2 Runtime Context
Pattern: Fetch once, use everywhere
Performance: 10x fewer database queries
"""

import asyncio
from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

load_dotenv()


# Define context structure (user preferences)
@dataclass
class UserContext:
    name: str
    country: str
    discount_rate: float


# Tools that read from runtime.context (no database queries)
@tool
def get_user_name(runtime: ToolRuntime) -> str:
    """Get the user's name from context"""
    return runtime.context.name


@tool
def get_user_country(runtime: ToolRuntime) -> str:
    """Get the user's country from context"""
    return runtime.context.country


@tool
def get_discount_rate(runtime: ToolRuntime) -> str:
    """Get the user's discount rate from context"""
    return f"{runtime.context.discount_rate * 100}%"


async def main():
    print("=" * 70)
    print("RUNTIME CONTEXT PATTERN")
    print("=" * 70)

    # Create agent with context schema and tools
    agent = create_agent(
        model="gpt-4o-mini",
        context_schema=UserContext,
        tools=[get_user_name, get_user_country, get_discount_rate]
    )

    # Simulate database fetch (happens ONCE at session start)
    print("\n📊 Fetching user data from database...")
    user_data = {
        "name": "Sarah Chen",
        "country": "Singapore",
        "discount_rate": 0.15
    }
    print(f"Retrieved: {user_data}")

    # Create context from fetched data
    context = UserContext(
        name=user_data["name"],
        country=user_data["country"],
        discount_rate=user_data["discount_rate"]
    )

    # Multiple questions - tools read from context (no DB queries)
    questions = [
        "What's my name and country?",
        "What discount do I get?",
        "Am I eligible for the Singapore promotion?"
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n💬 Question {i}: {question}")

        response = await agent.ainvoke(
            {"messages": [HumanMessage(content=question)]},
            context=context
        )

        print(f"🤖 Response: {response['messages'][-1].content}")

    print("\n" + "=" * 70)
    print("✅ Pattern Complete")
    print("\n💡 Key Insight:")
    print("   - Database queried: 1 time (at session start)")
    print("   - Tools called: Multiple times")
    print("   - Tools read from: runtime.context (memory)")
    print("   - Result: Zero additional database queries")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
