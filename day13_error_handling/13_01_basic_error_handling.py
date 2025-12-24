"""
Day 13 - Program 1: Basic Error Handling

Learn how to handle errors gracefully in production LangChain applications.

Errors you'll handle:
- API failures
- Network timeouts
- Invalid tool parameters
- Model errors
- Tool execution failures

Author: Klement
Date: December 23, 2025
Tech: LangChain 1.2, Error Handling, Production Patterns
"""

import sys
sys.path.insert(0, '/home/intruder/langchain_learning/examples')

from common_config import get_model
from langchain_core.tools import tool
from langchain.agents import create_agent

print("🛡️ Day 13 - Program 1: Basic Error Handling\n")

# STEP 1: Define tools with error handling
@tool
def divide(a: float, b: float) -> float:
    """Divide a by b. Returns error if b is zero."""
    try:
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        result = a / b
        print(f"  ✅ Tool: divide({a}, {b}) = {result}")
        return result
    except Exception as e:
        error_msg = f"Error in divide: {str(e)}"
        print(f"  ❌ {error_msg}")
        return error_msg

@tool
def safe_multiply(a: float, b: float) -> float:
    """Multiply two numbers with overflow protection."""
    try:
        result = a * b
        # Check for overflow (very large numbers)
        if abs(result) > 1e100:
            raise ValueError("Result too large! Overflow risk.")
        print(f"  ✅ Tool: multiply({a}, {b}) = {result}")
        return result
    except Exception as e:
        error_msg = f"Error in multiply: {str(e)}"
        print(f"  ❌ {error_msg}")
        return error_msg

@tool
def calculate_percentage(value: float, total: float) -> str:
    """Calculate percentage with validation."""
    try:
        if total == 0:
            return "Error: Total cannot be zero"
        if value < 0 or total < 0:
            return "Error: Values must be positive"

        percentage = (value / total) * 100
        result = f"{percentage:.2f}%"
        print(f"  ✅ Tool: {value}/{total} = {result}")
        return result
    except Exception as e:
        error_msg = f"Error calculating percentage: {str(e)}"
        print(f"  ❌ {error_msg}")
        return error_msg

# STEP 2: Create agent with error-aware system prompt
print("Creating agent with error handling...\n")

try:
    model = get_model(temperature=0)
    agent = create_agent(
        model=model,
        tools=[divide, safe_multiply, calculate_percentage],
        system_prompt="""You are a helpful math assistant.

IMPORTANT ERROR HANDLING RULES:
1. If a tool returns an error message, explain it to the user clearly
2. Don't try the same operation again if it failed
3. Suggest alternatives when operations fail
4. Always validate user input before using tools"""
    )
    print("✅ Agent created successfully\n")
except Exception as e:
    print(f"❌ Failed to create agent: {e}")
    sys.exit(1)

# STEP 3: Test error scenarios
print("=" * 70)
print("TEST 1: Division by zero (Expected error)")
print("=" * 70)

try:
    result1 = agent.invoke({"messages": [("user", "What is 10 divided by 0?")]})
    print(f"🤖 Agent: {result1['messages'][-1].content}\n")
except Exception as e:
    print(f"❌ Agent invocation failed: {e}\n")

print("=" * 70)
print("TEST 2: Valid division (Should work)")
print("=" * 70)

try:
    result2 = agent.invoke({"messages": [("user", "What is 100 divided by 5?")]})
    print(f"🤖 Agent: {result2['messages'][-1].content}\n")
except Exception as e:
    print(f"❌ Agent invocation failed: {e}\n")

print("=" * 70)
print("TEST 3: Percentage calculation with zero total (Error)")
print("=" * 70)

try:
    result3 = agent.invoke({"messages": [("user", "What percentage is 50 out of 0?")]})
    print(f"🤖 Agent: {result3['messages'][-1].content}\n")
except Exception as e:
    print(f"❌ Agent invocation failed: {e}\n")

print("=" * 70)
print("TEST 4: Valid percentage calculation")
print("=" * 70)

try:
    result4 = agent.invoke({"messages": [("user", "What percentage is 25 out of 200?")]})
    print(f"🤖 Agent: {result4['messages'][-1].content}\n")
except Exception as e:
    print(f"❌ Agent invocation failed: {e}\n")

print("=" * 70)
print("TEST 5: API error simulation (timeout/network)")
print("=" * 70)

# Simulate API failure scenario
conversation_history = []
conversation_history.append(("user", "Calculate 123 times 456"))

try:
    result5 = agent.invoke({"messages": conversation_history})
    print(f"🤖 Agent: {result5['messages'][-1].content}\n")
except Exception as e:
    # This is how you'd handle API failures in production
    print(f"❌ API Error occurred: {type(e).__name__}")
    print(f"   Error details: {str(e)}")
    print(f"   🔄 In production: Retry with exponential backoff")
    print(f"   💡 User message: 'Service temporarily unavailable, please try again'\n")

print("\n" + "=" * 70)
print("🎯 KEY LEARNINGS:")
print("=" * 70)
print("""
✅ ERROR HANDLING PATTERNS:

1. **Tool-Level Error Handling**:
   ```python
   @tool
   def my_tool(param):
       try:
           # Tool logic
           return result
       except Exception as e:
           return f"Error: {str(e)}"
   ```

2. **Agent-Level Error Handling**:
   ```python
   try:
       result = agent.invoke({"messages": messages})
   except Exception as e:
       # Handle API/network errors
       print(f"Error: {e}")
   ```

3. **Input Validation** (Before calling tools):
   - Check for zero division
   - Validate ranges
   - Check data types
   - Sanitize strings

4. **Error Messages**:
   - ❌ Bad: "Error"
   - ✅ Good: "Cannot divide by zero. Please provide non-zero divisor."

🛡️ PRODUCTION CHECKLIST:
   - [x] Try/except around all tool logic
   - [x] Try/except around agent.invoke()
   - [x] Validate inputs before processing
   - [x] Return user-friendly error messages
   - [x] Log errors for debugging
   - [ ] Retry logic (Program 2)
   - [ ] Fallback strategies (Program 3)

💡 NEXT: Retry mechanisms with exponential backoff!
""")

print("✅ Day 13 - Program 1 Complete!")
print("🎓 You now understand: Error handling in LangChain agents!")
