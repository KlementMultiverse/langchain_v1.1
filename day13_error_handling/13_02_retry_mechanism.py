"""
Day 13 - Program 2: Retry Mechanism with Exponential Backoff

Production systems MUST handle temporary failures:
- Network timeouts
- API rate limits
- Temporary service outages
- Transient errors

Solution: Retry with exponential backoff!

Author: Klement
Date: December 23, 2025
Tech: LangChain 1.2, Retry Logic, Exponential Backoff
"""

import sys
sys.path.insert(0, '/home/intruder/langchain_learning/examples')

import time
from typing import Any, Callable
from common_config import get_model
from langchain_core.tools import tool
from langchain.agents import create_agent

print("🔄 Day 13 - Program 2: Retry Mechanism with Exponential Backoff\n")

# STEP 1: Retry decorator with exponential backoff
def retry_with_exponential_backoff(
    max_retries: int = 3,
    initial_delay: float = 1.0,
    exponential_base: float = 2.0,
    jitter: bool = True
):
    """
    Retry decorator with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        initial_delay: Starting delay in seconds
        exponential_base: Multiplier for delay (2.0 = double each time)
        jitter: Add randomness to prevent thundering herd

    Delays: 1s → 2s → 4s → 8s → ...
    """
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    print(f"  🔄 Attempt {attempt + 1}/{max_retries + 1}...")
                    result = func(*args, **kwargs)
                    if attempt > 0:
                        print(f"  ✅ Success after {attempt + 1} attempts!")
                    return result

                except Exception as e:
                    last_exception = e

                    if attempt == max_retries:
                        print(f"  ❌ Failed after {max_retries + 1} attempts")
                        raise last_exception

                    # Add jitter (randomness) to prevent all clients retrying at once
                    import random
                    actual_delay = delay
                    if jitter:
                        actual_delay = delay * (0.5 + random.random())

                    print(f"  ⚠️  Attempt {attempt + 1} failed: {str(e)[:50]}")
                    print(f"  ⏳ Waiting {actual_delay:.2f}s before retry...")
                    time.sleep(actual_delay)

                    # Exponential backoff
                    delay *= exponential_base

            raise last_exception

        return wrapper
    return decorator

# STEP 2: Simulated unreliable tool (fails sometimes)
failure_count = 0

@tool
def unreliable_api_call(query: str) -> str:
    """
    Simulates an unreliable API that fails randomly.
    Used to demonstrate retry logic.
    """
    global failure_count
    failure_count += 1

    # Simulate: Fail first 2 times, succeed on 3rd
    if failure_count < 3:
        raise ConnectionError(f"API timeout (simulated failure #{failure_count})")

    # Reset counter and succeed
    failure_count = 0
    result = f"API response for: '{query}'"
    print(f"  ✅ Tool succeeded: {result}")
    return result

# STEP 3: Wrap tool with retry logic
@retry_with_exponential_backoff(max_retries=3, initial_delay=0.5, exponential_base=2.0)
def call_unreliable_api(query: str) -> str:
    """Call API with automatic retry on failure."""
    return unreliable_api_call.invoke({"query": query})

# STEP 4: Production-grade agent invoke with retry
def invoke_agent_with_retry(agent, messages, max_retries=3):
    """
    Invoke agent with retry logic for API failures.

    Production pattern for handling:
    - Network timeouts
    - Rate limits
    - Temporary service outages
    """
    @retry_with_exponential_backoff(max_retries=max_retries, initial_delay=1.0)
    def _invoke():
        return agent.invoke({"messages": messages})

    return _invoke()

# STEP 5: Create tools with retry built-in
@tool
def multiply_with_retry(a: float, b: float) -> float:
    """Multiply two numbers (production-grade with retry)."""
    @retry_with_exponential_backoff(max_retries=2, initial_delay=0.5)
    def _multiply():
        result = a * b
        print(f"  ✅ multiply({a}, {b}) = {result}")
        return result

    return _multiply()

@tool
def divide_with_retry(a: float, b: float) -> str:
    """Divide with retry and validation."""
    if b == 0:
        return "Error: Cannot divide by zero"

    @retry_with_exponential_backoff(max_retries=2, initial_delay=0.5)
    def _divide():
        result = a / b
        print(f"  ✅ divide({a}, {b}) = {result}")
        return str(result)

    return _divide()

# STEP 6: Create agent
print("Creating agent with retry-enabled tools...\n")

model = get_model(temperature=0)
agent = create_agent(
    model=model,
    tools=[multiply_with_retry, divide_with_retry],
    system_prompt="You are a reliable math assistant with automatic retry on failures."
)

print("=" * 70)
print("TEST 1: Unreliable API with automatic retry")
print("=" * 70)

print("\n📝 Scenario: API fails 2 times, succeeds on 3rd attempt")
print("Watch the retry mechanism in action:\n")

try:
    result = call_unreliable_api("test query")
    print(f"\n✅ Final result: {result}\n")
except Exception as e:
    print(f"\n❌ All retries failed: {e}\n")

print("=" * 70)
print("TEST 2: Agent with retry on valid operation")
print("=" * 70)

try:
    result2 = invoke_agent_with_retry(
        agent,
        [("user", "What is 25 times 8?")]
    )
    print(f"🤖 Agent: {result2['messages'][-1].content}\n")
except Exception as e:
    print(f"❌ Agent failed: {e}\n")

print("=" * 70)
print("TEST 3: Multiple operations in conversation")
print("=" * 70)

conversation = []
conversation.append(("user", "Calculate 100 divided by 4"))

try:
    result3 = invoke_agent_with_retry(agent, conversation)
    print(f"🤖 Agent: {result3['messages'][-1].content}\n")
except Exception as e:
    print(f"❌ Agent failed: {e}\n")

print("\n" + "=" * 70)
print("🎯 KEY LEARNINGS:")
print("=" * 70)
print("""
✅ RETRY PATTERNS:

1. **Exponential Backoff Formula**:
   Attempt 1: Wait 1s
   Attempt 2: Wait 2s (1s × 2)
   Attempt 3: Wait 4s (2s × 2)
   Attempt 4: Wait 8s (4s × 2)

   Why? Gives service time to recover!

2. **Retry Decorator Pattern**:
   ```python
   @retry_with_exponential_backoff(max_retries=3)
   def my_function():
       # Code that might fail
       return result
   ```

3. **When to Retry**:
   ✅ Network timeouts
   ✅ Rate limit errors (429)
   ✅ Service unavailable (503)
   ✅ Temporary API errors

   ❌ Authentication errors (401)
   ❌ Bad request (400)
   ❌ Not found (404)
   ❌ Division by zero (logic errors)

4. **Jitter (Randomness)**:
   - Prevents "thundering herd"
   - Multiple clients don't retry at exact same time
   - Spreads load on recovering service

5. **Production Configuration**:
   ```python
   # For user-facing APIs (fast fail)
   max_retries=2, initial_delay=0.5s

   # For background jobs (can wait)
   max_retries=5, initial_delay=2s

   # For critical operations (must succeed)
   max_retries=10, initial_delay=1s
   ```

🛡️ PRODUCTION CHECKLIST:
   - [x] Retry on transient errors
   - [x] Exponential backoff
   - [x] Jitter to prevent thundering herd
   - [x] Max retry limit (prevent infinite loops)
   - [x] Log retry attempts
   - [x] User-friendly timeout messages

💡 RETRY BEST PRACTICES:
   1. Set reasonable max_retries (3-5 is typical)
   2. Use exponential backoff (not linear)
   3. Add jitter for distributed systems
   4. Log all retry attempts for debugging
   5. Show users "Retrying..." for long waits
   6. Have a final fallback when retries exhausted

📊 REAL-WORLD EXAMPLE:
   OpenAI API call fails → Retry 3 times with backoff → Success!
   Without retry: User sees error ❌
   With retry: User never knows it failed ✅

🔥 NEXT: Input Validation & Sanitization!
""")

print("\n✅ Day 13 - Program 2 Complete!")
print("🎓 You now understand: Retry mechanisms with exponential backoff!")
