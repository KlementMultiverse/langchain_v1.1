"""
Multi-Agent Systems - Delegation Pattern

Demonstrates how to create specialized subagents and coordinate them
with a main agent using the delegation pattern.

Module: 2.3 Multi-Agent Systems
Pattern: Main agent delegates tasks to specialized subagents
Key Concept: Sequential execution, agent-as-tool wrapper
"""

import asyncio
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage
from pprint import pprint

load_dotenv()


# Step 1: Create specialized tools
@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5


@tool
def square(x: float) -> float:
    """Calculate the square of a number"""
    return x ** 2


# Step 2: Create specialized subagents (each with ONE tool)
subagent_1 = create_agent(
    model='gpt-4o-mini',
    tools=[square_root]  # Only knows square root
)

subagent_2 = create_agent(
    model='gpt-4o-mini',
    tools=[square]  # Only knows square
)


# Step 3: Wrap subagents in tools (so main agent can call them)
@tool
def call_subagent_1(x: float) -> float:
    """Call subagent 1 to calculate the square root of a number"""
    response = subagent_1.invoke(
        {"messages": [HumanMessage(content=f"Calculate the square root of {x}")]}
    )
    return response["messages"][-1].content


@tool
def call_subagent_2(x: float) -> float:
    """Call subagent 2 to calculate the square of a number"""
    response = subagent_2.invoke(
        {"messages": [HumanMessage(content=f"Calculate the square of {x}")]}
    )
    return response["messages"][-1].content


# Step 4: Create main agent (coordinator with subagent tools)
main_agent = create_agent(
    model='gpt-4o-mini',
    tools=[call_subagent_1, call_subagent_2],
    system_prompt="You are a helpful assistant who can call subagents to calculate the square root or square of a number."
)


async def main():
    print("=" * 70)
    print("MULTI-AGENT DELEGATION PATTERN")
    print("=" * 70)

    print("\n🏗️ Architecture:")
    print("   Main Agent (Coordinator)")
    print("   ├── Tool: call_subagent_1 → Subagent 1 (square_root)")
    print("   └── Tool: call_subagent_2 → Subagent 2 (square)")

    print("\n" + "=" * 70)
    print("TEST 1: Square Root Request")
    print("=" * 70)

    question1 = "What is the square root of 456?"
    print(f"\n💬 User: {question1}")

    response1 = await main_agent.ainvoke(
        {"messages": [HumanMessage(content=question1)]}
    )

    print(f"\n🤖 Main Agent: {response1['messages'][-1].content}")

    print("\n📊 What happened:")
    print("   1. Main agent saw 'square root' in question")
    print("   2. Main agent called: call_subagent_1(456)")
    print("   3. call_subagent_1 invoked subagent_1")
    print("   4. subagent_1 used square_root tool: √456 ≈ 21.4")
    print("   5. Result returned to main agent")
    print("   6. Main agent responded to user")

    print("\n" + "=" * 70)
    print("TEST 2: Square Request")
    print("=" * 70)

    question2 = "What is the square of 25?"
    print(f"\n💬 User: {question2}")

    response2 = await main_agent.ainvoke(
        {"messages": [HumanMessage(content=question2)]}
    )

    print(f"\n🤖 Main Agent: {response2['messages'][-1].content}")

    print("\n📊 What happened:")
    print("   1. Main agent saw 'square' (not 'square root') in question")
    print("   2. Main agent called: call_subagent_2(25)")
    print("   3. call_subagent_2 invoked subagent_2")
    print("   4. subagent_2 used square tool: 25² = 625")
    print("   5. Result returned to main agent")
    print("   6. Main agent responded to user")

    print("\n" + "=" * 70)
    print("✅ Multi-Agent Pattern Complete")
    print("\n💡 Key Concepts:")
    print("   - Subagents are specialists (one tool each)")
    print("   - Wrapper tools allow main agent to call subagents")
    print("   - Main agent decides which subagent to use")
    print("   - Execution is sequential (one at a time)")
    print("   - Pattern: Main → Pick subagent → Subagent executes → Return")
    print("\n🌍 Real-world examples:")
    print("   - Travel Agent: Flight subagent, hotel subagent, car rental subagent")
    print("   - Customer Service: Billing subagent, tech support subagent")
    print("   - Research Assistant: Search subagent, summarize subagent")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
