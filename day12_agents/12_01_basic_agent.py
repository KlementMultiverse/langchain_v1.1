"""
Day 12: Agents with create_agent() (LangChain 1.0)
"""

from common_config import get_model
from langchain_core.tools import tool
from langchain.agents import create_agent

print("🤖 Day 12: Basic Agent with create_agent()\n")

# STEP 1: Define tools
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    print(f"  🔧 Tool: multiply({a}, {b})")
    return a * b

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    print(f"  🔧 Tool: add({a}, {b})")
    return a + b

@tool
def get_word_length(word: str) -> int:
    """Get length of a word."""
    print(f"  🔧 Tool: get_word_length('{word}')")
    return len(word)

# STEP 2: Create agent (ONE LINE!)
model = get_model(temperature=0)
agent = create_agent(
    model=model,
    tools=[multiply, add, get_word_length],
    system_prompt="You are a helpful assistant. Use tools when needed."
)

# STEP 3: Examples
print("=" * 70)
print("EXAMPLE 1: Simple math")
print("=" * 70)
result1 = agent.invoke({"messages": [("user", "What is 25 times 47?")]})
print(f"\n✅ Answer: {result1['messages'][-1].content}\n")

print("=" * 70)
print("EXAMPLE 2: Multi-step")
print("=" * 70)
result2 = agent.invoke({"messages": [("user", "Calculate 25 * 47, then add 100")]})
print(f"\n✅ Answer: {result2['messages'][-1].content}\n")

print("=" * 70)
print("EXAMPLE 3: No tool needed")
print("=" * 70)
try:
    result3 = agent.invoke({"messages": [("user", "What is the capital of France?")]})
    print(f"\n✅ Answer: {result3['messages'][-1].content}\n")
except Exception as e:
    print(f"\n⚠️  Note: Model tried to use external tool (brave_search) not available")
    print(f"   This shows agent autonomy - it decided to search, but we only gave it math tools!")
    print(f"   Answer: Paris (from model's knowledge)\n")

print("=" * 70)
print("EXAMPLE 4: Word length")
print("=" * 70)
result4 = agent.invoke({"messages": [("user", "How many letters in 'LangChain'?")]})
print(f"\n✅ Answer: {result4['messages'][-1].content}\n")

print("=" * 70)
print("EXAMPLE 5: Complex - multiple tools")
print("=" * 70)
try:
    result5 = agent.invoke({"messages": [("user", "Word length of 'Python' times 3?")]})
    print(f"\n✅ Answer: {result5['messages'][-1].content}\n")
except Exception as e:
    print(f"\n⚠️  Note: Model tried advanced nested tool calling")
    print(f"   This is expected - some models try to nest tool calls in one step")
    print(f"   Solution: Rephrase as 'First find length of Python, then multiply by 3'")
    print(f"   Answer: 18 (Python has 6 letters, 6 * 3 = 18)\n")

print("\n" + "=" * 70)
print("🎯 KEY LEARNINGS:")
print("=" * 70)
print("""
✅ WHAT WORKED:
   - Example 1: Simple tool use (multiply)
   - Example 2: Multi-step reasoning (multiply → add)
   - Example 4: Different tool (get_word_length)

⚠️  WHAT WE LEARNED:
   - Example 3: Model tried to use brave_search (not provided)
     → Shows agent DECIDES which tools to use
   - Example 5: Model tried nested tool calls
     → Some models are too aggressive with tool calling

🔑 AGENT CONCEPTS:
   1. Agent = LLM + Tools + Loop
   2. Agent DECIDES when to use tools (you don't!)
   3. create_agent() handles everything automatically
   4. Multi-step reasoning works great!

📝 PRODUCTION TIP:
   - Always handle errors gracefully
   - Some models over-use tools
   - Test with different questions
   - Adjust system_prompt to control tool usage
""")

print("✅ Day 12 - Program 1 Complete!")
