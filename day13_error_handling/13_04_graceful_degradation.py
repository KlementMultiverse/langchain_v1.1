"""
Day 13 - Program 4: Graceful Degradation & Fallback Strategies

When things fail, DON'T CRASH - degrade gracefully!

Strategies:
1. Primary tool fails → Use fallback tool
2. API unavailable → Use cached data
3. Advanced feature fails → Use simple alternative
4. All tools fail → Return partial/manual response

Author: Klement
Date: December 23, 2025
Tech: LangChain 1.2, Fallback Patterns, Resilience
"""

import sys
sys.path.insert(0, '/home/intruder/langchain_learning/examples')

from common_config import get_model
from langchain_core.tools import tool
from langchain.agents import create_agent

print("🎯 Day 13 - Program 4: Graceful Degradation\n")

# STEP 1: Primary and fallback tools
@tool
def advanced_calculator(expression: str) -> str:
    """
    Advanced calculator (simulates sometimes failing).
    Primary tool - more features but less reliable.
    """
    # Simulate 40% failure rate
    import random
    if random.random() < 0.4:
        print("  ❌ Advanced calculator unavailable")
        raise ConnectionError("Advanced calculator service down")

    try:
        # In production: Use advanced math library
        result = eval(expression)  # Simplified for demo
        print(f"  ✅ Advanced calc: {expression} = {result}")
        return f"Result: {result}"
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")

@tool
def simple_calculator(a: float, b: float, operation: str) -> str:
    """
    Simple calculator - basic operations only.
    Fallback tool - fewer features but 100% reliable.
    """
    operations = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else "Error: Division by zero"
    }

    if operation not in operations:
        return f"Error: Operation '{operation}' not supported. Use: add, subtract, multiply, divide"

    try:
        result = operations[operation](a, b)
        print(f"  ✅ Simple calc: {a} {operation} {b} = {result}")
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# STEP 2: Cache simulation (for when API is down)
knowledge_cache = {
    "pi": "3.14159",
    "e": "2.71828",
    "speed_of_light": "299,792,458 m/s",
    "earth_radius": "6,371 km"
}

@tool
def get_scientific_constant(name: str) -> str:
    """
    Get scientific constant.
    Tries API first, falls back to cache if API fails.
    """
    import random

    # Simulate API availability
    api_available = random.random() > 0.3

    if api_available:
        # Simulate API call
        if name.lower() in knowledge_cache:
            value = knowledge_cache[name.lower()]
            print(f"  ✅ API: Retrieved {name} = {value}")
            return f"{name}: {value} (from API)"
        else:
            print(f"  ⚠️  API: Constant '{name}' not found")
            return f"Constant '{name}' not found"
    else:
        # Fallback to cache
        print(f"  ⚠️  API unavailable, using cache...")
        if name.lower() in knowledge_cache:
            value = knowledge_cache[name.lower()]
            print(f"  ✅ Cache: Retrieved {name} = {value}")
            return f"{name}: {value} (from cache - may be outdated)"
        else:
            return f"Sorry, '{name}' not available offline"

# STEP 3: Multi-level fallback pattern
@tool
def get_weather(location: str) -> str:
    """
    Get weather with 3-level fallback:
    1. Real-time API (best)
    2. Cached data (good)
    3. Generic response (acceptable)
    """
    import random

    # Level 1: Try real-time API
    if random.random() > 0.7:
        print(f"  ✅ Level 1: Real-time weather for {location}")
        return f"Weather in {location}: 72°F, Sunny (real-time data)"

    # Level 2: Try cache
    if random.random() > 0.5:
        print(f"  ⚠️  Level 2: Using cached weather for {location}")
        return f"Weather in {location}: 70°F, Partly cloudy (cached data from 1 hour ago)"

    # Level 3: Generic response
    print(f"  ⚠️  Level 3: Generic response for {location}")
    return f"Sorry, weather data for {location} temporarily unavailable. Please try again later or check weather.com"

# STEP 4: Create resilient agent
print("Creating agent with graceful degradation...\n")

model = get_model(temperature=0)
agent = create_agent(
    model=model,
    tools=[advanced_calculator, simple_calculator, get_scientific_constant, get_weather],
    system_prompt="""You are a resilient assistant with fallback strategies.

DEGRADATION STRATEGY:
1. Try primary tool first
2. If it fails, try fallback tool
3. If both fail, provide manual/approximate answer
4. ALWAYS give user SOME answer (never just "error")

IMPORTANT:
- Explain when using fallback ("API down, using cache...")
- Indicate data freshness ("cached from 1 hour ago")
- Be transparent about limitations"""
)

# STEP 5: Test graceful degradation
print("=" * 70)
print("TEST 1: Calculator with automatic fallback")
print("=" * 70)

for i in range(1, 4):
    print(f"\nAttempt {i}:")
    try:
        result = agent.invoke({"messages": [("user", "Calculate 15 times 8")]})
        print(f"🤖 Agent: {result['messages'][-1].content}")
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 70)
print("TEST 2: Scientific constant with cache fallback")
print("=" * 70)

for i in range(1, 3):
    print(f"\nAttempt {i}:")
    result = agent.invoke({"messages": [("user", "What is the value of pi?")]})
    print(f"🤖 Agent: {result['messages'][-1].content}")

print("\n" + "=" * 70)
print("TEST 3: Weather with 3-level fallback")
print("=" * 70)

for i in range(1, 4):
    print(f"\nAttempt {i}:")
    result = agent.invoke({"messages": [("user", "What's the weather in San Francisco?")]})
    print(f"🤖 Agent: {result['messages'][-1].content}")

print("\n" + "=" * 70)
print("🎯 KEY LEARNINGS:")
print("=" * 70)
print("""
✅ GRACEFUL DEGRADATION STRATEGIES:

1. **Tool Fallback Pattern**:
   Primary (advanced) → Fallback (simple) → Manual response

   Example:
   - Advanced calculator fails → Use simple calculator
   - Simple calculator fails → Return approximate answer

2. **Data Freshness Levels**:
   ```
   Level 1: Real-time API ✅ (best)
   Level 2: Recent cache ⚠️  (good)
   Level 3: Old cache ⚠️  (acceptable)
   Level 4: Manual/approximate ⚠️  (last resort)
   ```

3. **Cache-First Pattern** (for slow APIs):
   ```python
   def get_data():
       # 1. Check cache first (fast)
       if in_cache and fresh:
           return cached_data

       # 2. Try API (slower)
       try:
           data = api_call()
           update_cache(data)
           return data
       except:
           # 3. Return stale cache
           return cached_data + " (may be outdated)"
   ```

4. **Multi-Model Fallback**:
   ```
   GPT-4 (best, expensive) → GPT-3.5 (good, cheap) → Local model (basic, free)
   ```

5. **Circuit Breaker Pattern**:
   - If tool fails 5 times → Stop trying for 1 minute
   - Prevents wasting resources on dead service
   - Automatically resume when service recovers

🛡️ DEGRADATION CHECKLIST:
   - [x] Primary tool + fallback tool
   - [x] Cache for offline operation
   - [x] Multiple data freshness levels
   - [x] Transparent to user (explain what happened)
   - [x] NEVER return just "error" - always provide SOMETHING
   - [x] Indicate data quality/freshness

💡 USER EXPERIENCE PRINCIPLES:
   ✅ GOOD: "Weather: 70°F (from cache, may not be current)"
   ❌ BAD: "Error 503: Service unavailable"

   ✅ GOOD: "Advanced calc down, used simple calc: 120"
   ❌ BAD: "Calculator service error"

   ✅ GOOD: "Can't get real-time data. Check weather.com"
   ❌ BAD: "API timeout"

📊 REAL-WORLD EXAMPLES:

**Google Search**:
- Server 1 down → Try server 2
- Server 2 down → Try server 3
- All down → Cached results from 5 min ago

**Netflix**:
- High quality stream fails → Medium quality
- Medium fails → Low quality
- Low fails → Pause and buffer

**E-commerce**:
- Real-time inventory fails → Cached inventory (warn: may not be accurate)
- Payment API fails → Queue order, process later
- Shipping calc fails → Manual estimate

🎯 PRODUCTION BEST PRACTICES:

1. **Fail Open vs Fail Closed**:
   - Security: Fail closed (deny if unsure)
   - Availability: Fail open (allow with warning)

2. **Monitoring**:
   - Track fallback usage rate
   - Alert if using fallbacks >10%
   - Indicates primary system issues

3. **Testing**:
   - Chaos engineering (randomly fail services)
   - Verify fallbacks actually work
   - Test with cache at different staleness levels

🔥 COMPLETE! Day 13 mastery achieved!
""")

print("\n✅ Day 13 - Program 4 Complete!")
print("🎓 You now understand: Graceful degradation & fallback strategies!")
print("\n🎉 DAY 13 COMPLETE - ERROR HANDLING MASTERY! 🎉")
