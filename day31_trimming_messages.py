"""
Message Trimming Middleware - Clean Conversation History

Demonstrates how to remove ToolMessages from conversation history to prevent
users from seeing internal debug logs and tool outputs. Critical for production
agents that need clean, user-facing conversations.

Module: 3 - Production-Ready Agents
Lesson: 3.2 - Managing Messages
Pattern: Pre-process messages with @before_agent decorator
Key Concept: Clean UX by removing internal tool noise
"""

from dotenv import load_dotenv
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import before_agent
from langgraph.runtime import Runtime
from langchain.messages import ToolMessage, RemoveMessage, AIMessage, HumanMessage
from typing import Any
from pprint import pprint

load_dotenv()


print("=" * 80)
print("MESSAGE TRIMMING MIDDLEWARE - CLEAN CONVERSATION UX")
print("=" * 80)
print("\n💡 Purpose: Remove ToolMessages to prevent users seeing debug logs")
print("💡 Use Case: Customer support, data analysis, any tool-using agent\n")


# =============================================================================
# PART 1: THE PROBLEM - Without Trimming
# =============================================================================

print("=" * 80)
print("PART 1: THE PROBLEM - Users See Debug Logs")
print("=" * 80)

print("\n❌ WITHOUT TRIMMING:")
print("   User asks: 'What's the temperature of the device?'")
print("   User sees:")
print("   • 'My device won't turn on. What should I do?'")
print("   • 'blorp-x7 initiating diagnostic ping…' ← TOOL NOISE")
print("   • 'Is the device plugged in and turned on?'")
print("   • 'Yes, it's plugged in and turned on.'")
print("   • 'temp=42C voltage=2.9v … greeble complete.' ← TOOL NOISE")
print("   • 'Is the device showing any lights or indicators?'")
print("   • 'What's the temperature of the device?'")
print("\n   Users don't need to see 'blorp-x7' or 'voltage=2.9v'")
print("   They just need the answer.")


# =============================================================================
# PART 2: THE SOLUTION - Message Trimming
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 2: THE SOLUTION - Trim ToolMessages")
print("=" * 80)

@before_agent
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Remove all the tool messages from the state"""
    messages = state['messages']
    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
    return {"messages": [RemoveMessage(id=m.id) for m in tool_messages]}


print("\n✅ Middleware created with @before_agent decorator")
print("   • Runs BEFORE AI sees messages")
print("   • Finds all ToolMessages")
print("   • Removes them from conversation history")
print("   • AI sees clean Human + AI messages only")


# =============================================================================
# PART 3: TESTING THE MIDDLEWARE
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 3: TESTING MESSAGE TRIMMING")
print("=" * 80)

agent = create_agent(
    model='gpt-4o-mini',
    checkpointer=InMemorySaver(),
    middleware=[trim_messages]
)

print("\n✅ Agent created with trimming middleware")

# Simulate conversation with tool messages
print("\n" + "─" * 80)
print("SIMULATING CONVERSATION (7 messages including 2 ToolMessages)")
print("─" * 80)

response = agent.invoke(
    {"messages": [
        HumanMessage(content="My device won't turn on. What should I do?"),
        ToolMessage(content="blorp-x7 initiating diagnostic ping…", tool_call_id="1"),
        AIMessage(content="Is the device plugged in and turned on?"),
        HumanMessage(content="Yes, it's plugged in and turned on."),
        ToolMessage(content="temp=42C voltage=2.9v … greeble complete.", tool_call_id="2"),
        AIMessage(content="Is the device showing any lights or indicators?"),
        HumanMessage(content="What's the temperature of the device?")
    ]},
    {"configurable": {"thread_id": "1"}}
)

print("\n📊 RESULT AFTER TRIMMING:")
print(f"   Total messages in response: {len(response['messages'])}")
print(f"   ToolMessages removed: 2")
print(f"   Clean messages remaining: {len(response['messages'])}")

print("\n📝 CLEAN MESSAGE HISTORY:")
for i, msg in enumerate(response['messages'], 1):
    msg_type = type(msg).__name__
    content_preview = msg.content[:60] + "..." if len(msg.content) > 60 else msg.content
    print(f"   {i}. [{msg_type}] {content_preview}")

print("\n✅ No ToolMessages visible to user!")
print("   Users see clean conversation flow only.")


# =============================================================================
# PART 4: THE CODE BREAKDOWN
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 4: CODE BREAKDOWN - Line by Line")
print("=" * 80)

print("""
@before_agent
def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    messages = state['messages']
    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
    return {"messages": [RemoveMessage(id=m.id) for m in tool_messages]}

LINE BY LINE:

1. @before_agent
   → Decorator that runs this function BEFORE AI processes messages
   → Runs inside agent.invoke(), not when creating agent

2. def trim_messages(state: AgentState, runtime: Runtime)
   → state: Current agent state with all messages
   → runtime: LangGraph runtime (not used here, but required parameter)

3. messages = state['messages']
   → Extract message list from state
   → Example: [HumanMessage(...), ToolMessage(...), AIMessage(...)]

4. tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
   → List comprehension that filters only ToolMessages
   → isinstance(m, ToolMessage) checks if message is a ToolMessage
   → Result: [ToolMessage(...), ToolMessage(...)]

5. return {"messages": [RemoveMessage(id=m.id) for m in tool_messages]}
   → For each ToolMessage, create RemoveMessage(id=m.id)
   → RemoveMessage tells LangGraph to delete that message
   → Returns dictionary with "messages" key (required format)
""")


# =============================================================================
# PART 5: PRODUCTION PATTERNS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 5: PRODUCTION PATTERNS")
print("=" * 80)

print("\n📚 PATTERN 1: REMOVE ONLY TOOLMESSAGES (Most Common)")
print("─" * 80)
print("""
@before_agent
def trim_tool_messages(state, runtime):
    messages = state["messages"]
    tool_messages = [m for m in messages if isinstance(m, ToolMessage)]
    return {"messages": [RemoveMessage(id=m.id) for m in tool_messages]}

Use Case: Customer support, data analysis
Why: Users don't need to see internal tool outputs
""")

print("\n📚 PATTERN 2: REMOVE MULTIPLE MESSAGE TYPES")
print("─" * 80)
print("""
from langchain.messages import SystemMessage

@before_agent
def trim_system_and_tool(state, runtime):
    messages = state["messages"]
    noise = [m for m in messages if isinstance(m, (ToolMessage, SystemMessage))]
    return {"messages": [RemoveMessage(id=m.id) for m in noise]}

Use Case: Complex agents with system prompts
Why: Remove both tool noise and system messages
""")

print("\n📚 PATTERN 3: KEEP LAST N MESSAGES, REMOVE OLDER")
print("─" * 80)
print("""
@before_agent
def keep_recent_only(state, runtime):
    messages = state["messages"]
    if len(messages) > 10:
        old_messages = messages[:-10]  # All except last 10
        return {"messages": [RemoveMessage(id=m.id) for m in old_messages]}
    return None  # Don't modify if <= 10 messages

Use Case: Long conversations with memory limits
Why: Keep conversation fresh, remove old context
""")


# =============================================================================
# PART 6: EXECUTION FLOW
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 6: EXECUTION FLOW - When Middleware Runs")
print("=" * 80)

print("""
TIMELINE:

1. agent = create_agent(middleware=[trim_messages])
   → Agent created
   → Middleware REGISTERED (not run yet)

2. agent.invoke({...})
   → @before_agent runs NOW
   → trim_messages() executes
   → ToolMessages removed from state

3. AI processes messages
   → Sees clean message history
   → No ToolMessages in context
   → Generates better response

4. Response returned
   → User sees clean conversation
   → No debug logs visible
""")


# =============================================================================
# SUMMARY AND BEST PRACTICES
# =============================================================================

print("\n\n" + "=" * 80)
print("✅ MESSAGE TRIMMING - COMPLETE")
print("=" * 80)

print("\n🎯 KEY LEARNINGS:")
print("   1. @before_agent runs before AI sees messages")
print("   2. RemoveMessage(id=...) deletes messages from state")
print("   3. isinstance(m, ToolMessage) filters by message type")
print("   4. List comprehension is shorthand for filtering")
print("   5. Return format: {'messages': [RemoveMessage(...)]}")

print("\n💼 PRODUCTION USE CASES:")
print("   • Customer support (hide database queries)")
print("   • Data analysis (hide calculation steps)")
print("   • Code review (hide file operations)")
print("   • Document Q&A (hide retrieval steps)")

print("\n⚠️  COMMON MISTAKES:")
print("   1. No trimming → Users see debug logs")
print("   2. Wrong message type → Removes user messages")
print("   3. Forget @before_agent → Doesn't run at all")
print("   4. Remove too much → AI loses context")

print("\n🚀 PRODUCTION CHECKLIST:")
print("   ✓ Use @before_agent for pre-processing")
print("   ✓ Filter by message type (ToolMessage, SystemMessage)")
print("   ✓ Test with real conversation flows")
print("   ✓ Verify user-facing messages are clean")
print("   ✓ Monitor that AI still has enough context")

print("\n📚 NEXT STEPS:")
print("   • Combine with SummarizationMiddleware for token savings")
print("   • Add custom trimming logic (keep last N, time-based, etc.)")
print("   • Use in production agents with tools")
print("   • Test user experience improvements")

print("\n" + "=" * 80)
print("🎓 Clean conversations = Production ready")
print("=" * 80)
