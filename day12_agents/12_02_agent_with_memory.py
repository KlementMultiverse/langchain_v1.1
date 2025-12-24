"""
Day 12 - Program 2: Agent with Memory

Combines:
- Agents (Day 12) - Tool calling
- Memory (Day 5) - Conversation history

Result: Agent that remembers previous conversations!

Author: Klement
Date: December 23, 2025
Tech: LangChain 1.2, Agents, Memory
"""

import sys
sys.path.insert(0, '/home/intruder/langchain_learning/examples')

from common_config import get_model
from langchain_core.tools import tool
from langchain.agents import create_agent

print("🧠 Day 12 - Program 2: Agent with Memory\n")

# STEP 1: Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together."""
    print(f"  🔧 Tool: multiply({a}, {b})")
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    print(f"  🔧 Tool: add({a}, {b})")
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtract b from a."""
    print(f"  🔧 Tool: subtract({a}, {b})")
    return a - b

@tool
def save_preference(item: str, value: str) -> str:
    """Save a user preference (like favorite color, name, etc)."""
    print(f"  💾 Saving: {item} = {value}")
    return f"Saved {item}: {value}"

# STEP 2: Create agent
model = get_model(temperature=0, model_name="llama-3.3-70b-versatile")
agent = create_agent(
    model=model,
    tools=[multiply, add, subtract, save_preference],
    system_prompt="""You are a helpful math assistant with memory.

Remember information the user tells you across the conversation.
When the user mentions their name, preferences, or previous results, remember them!"""
)

# STEP 3: Create conversation memory
conversation_history = []

print("=" * 70)
print("CONVERSATION 1: Introduction")
print("=" * 70)

# Turn 1: User introduces themselves
user_msg_1 = "Hi! My name is Klement."
print(f"👤 User: {user_msg_1}")

conversation_history.append(("user", user_msg_1))
result_1 = agent.invoke({"messages": conversation_history})

# Get agent's response
agent_response_1 = result_1['messages'][-1].content
print(f"🤖 Agent: {agent_response_1}\n")

# Add agent response to history
conversation_history.append(("assistant", agent_response_1))

print("=" * 70)
print("CONVERSATION 2: Math with memory")
print("=" * 70)

# Turn 2: Do some math
user_msg_2 = "What's 15 times 8?"
print(f"👤 User: {user_msg_2}")

conversation_history.append(("user", user_msg_2))
result_2 = agent.invoke({"messages": conversation_history})

agent_response_2 = result_2['messages'][-1].content
print(f"🤖 Agent: {agent_response_2}\n")
conversation_history.append(("assistant", agent_response_2))

print("=" * 70)
print("CONVERSATION 3: Reference previous result")
print("=" * 70)

# Turn 3: Reference previous calculation
user_msg_3 = "Add 50 to that result"  # "that" = 120 from previous!
print(f"👤 User: {user_msg_3}")

conversation_history.append(("user", user_msg_3))
result_3 = agent.invoke({"messages": conversation_history})

agent_response_3 = result_3['messages'][-1].content
print(f"🤖 Agent: {agent_response_3}\n")
conversation_history.append(("assistant", agent_response_3))

print("=" * 70)
print("CONVERSATION 4: Remember name")
print("=" * 70)

# Turn 4: Ask about name
user_msg_4 = "What's my name?"
print(f"👤 User: {user_msg_4}")

conversation_history.append(("user", user_msg_4))
result_4 = agent.invoke({"messages": conversation_history})

agent_response_4 = result_4['messages'][-1].content
print(f"🤖 Agent: {agent_response_4}\n")
conversation_history.append(("assistant", agent_response_4))

print("\n" + "=" * 70)
print("🎯 KEY LEARNINGS:")
print("=" * 70)
print("""
✅ MEMORY WORKS!
   - Agent remembered your name from Turn 1
   - Agent remembered calculation result (120) from Turn 2
   - Agent understood "that" refers to previous result

🔑 HOW IT WORKS:
   1. conversation_history = [] (store all messages)
   2. Add user message: conversation_history.append(("user", msg))
   3. Pass to agent: agent.invoke({"messages": conversation_history})
   4. Add agent response: conversation_history.append(("assistant", response))
   5. Repeat!

🧠 MEMORY PATTERN:
   User Msg → Add to history → Agent processes → Add response → Next turn

📊 CONVERSATION FLOW:
   Turn 1: "My name is Klement" → [saved to history]
   Turn 2: "What's 15 times 8?" → [agent sees name + new question]
   Turn 3: "Add 50 to that" → [agent sees all previous, knows "that" = 120]
   Turn 4: "What's my name?" → [agent retrieves from Turn 1]

💡 PRODUCTION TIP:
   - Store conversation_history in database for persistence
   - Limit history size (e.g., last 10 messages) to save tokens
   - Clear history when starting new session
   - Add timestamps to track conversation flow
""")

print("\n✅ Day 12 - Program 2 Complete!")
print("🎓 You now understand: Agents + Memory!")
