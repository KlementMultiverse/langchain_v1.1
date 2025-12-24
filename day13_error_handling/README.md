# Day 13: Error Handling & Resilience

**Date**: December 23, 2025
**Focus**: Production-grade error handling, retry mechanisms, and graceful degradation
**Tech Stack**: LangChain 1.2, Groq API, Production Patterns

---

## 🎯 Why Error Handling Matters

**Production reality:**
- ❌ APIs fail (network timeouts, rate limits)
- ❌ Models hallucinate or return unexpected formats
- ❌ Tools execute with errors
- ❌ Users send malicious/invalid input
- ❌ Services go down temporarily

**Your agent MUST handle these gracefully!**

Without proper error handling:
- Users see cryptic error messages
- Applications crash
- Security vulnerabilities
- Poor user experience

With error handling:
- Automatic recovery from failures
- User-friendly messages
- Security hardening
- Production reliability

---

## 📁 Programs

### **13_01_basic_error_handling.py** - Fundamental Error Patterns
**Concepts**: Try/except, input validation, user-friendly errors

**What it does**:
- Tool-level error handling (validate before executing)
- Agent-level error handling (catch API failures)
- Division by zero prevention
- Overflow protection
- Clear error messages

**Key Learning**: Two-layer error handling - tools AND agent invocation

```python
@tool
def divide(a: float, b: float) -> float:
    try:
        if b == 0:
            raise ValueError("Cannot divide by zero!")
        return a / b
    except Exception as e:
        return f"Error: {str(e)}"

# Agent level
try:
    result = agent.invoke({"messages": messages})
except Exception as e:
    print(f"API Error: {e}")
```

**Output**:
```
TEST: Division by zero
❌ Error in divide: Cannot divide by zero!
🤖 Agent: "Division by zero is undefined. Try a different number."
```

---

### **13_02_retry_mechanism.py** - Exponential Backoff
**Concepts**: Retry logic, exponential backoff, jitter, resilience

**What it does**:
- Automatic retry on transient failures
- Exponential backoff (1s → 2s → 4s → 8s)
- Jitter to prevent thundering herd
- Configurable max retries
- Production-grade retry decorator

**Key Learning**: Most API failures are temporary - retry automatically!

```python
@retry_with_exponential_backoff(max_retries=3, initial_delay=1.0)
def call_api():
    return api_call()

# Delays:
# Attempt 1: Fail → Wait 1s
# Attempt 2: Fail → Wait 2s (exponential)
# Attempt 3: Success! ✅
```

**Output**:
```
🔄 Attempt 1/4...
⚠️  Attempt 1 failed: API timeout
⏳ Waiting 0.36s before retry...

🔄 Attempt 2/4...
⚠️  Attempt 2 failed: API timeout
⏳ Waiting 1.22s before retry...

🔄 Attempt 3/4...
✅ Success after 3 attempts!
```

**When to Retry**:
- ✅ Network timeouts
- ✅ Rate limit errors (429)
- ✅ Service unavailable (503)
- ❌ Authentication errors (401)
- ❌ Bad request (400)
- ❌ Logic errors (division by zero)

---

### **13_03_input_validation.py** - Security & Sanitization
**Concepts**: Input validation, security, overflow prevention, sanitization

**What it does**:
- Validate all user inputs before processing
- Type validation (int, float, string)
- Range validation (min/max values)
- Email format validation
- Overflow prevention (999^999 blocked!)
- String sanitization (remove dangerous characters)

**Key Learning**: NEVER trust user input - validate everything!

```python
def validate_number(value, min_val, max_val):
    try:
        num = float(value)
        if num != num:  # NaN check
            return False, "Invalid: NaN"
        if num == float('inf'):
            return False, "Invalid: Infinity"
        if num < min_val or num > max_val:
            return False, "Out of range"
        return True, num
    except ValueError:
        return False, "Not a number"
```

**Output**:
```
TEST: Overflow prevention
User: "Calculate 999^999"
Validation: ❌ BLOCKED!
Agent: "Result would be too large (overflow risk)"

TEST: Email validation
klement@example.com → ✅ Valid
not-an-email → ❌ Invalid format
```

**Security Threats Prevented**:
- ❌ SQL Injection
- ❌ Prompt Injection
- ❌ Path Traversal
- ❌ Code Injection
- ❌ Denial of Service (huge inputs)

---

### **13_04_graceful_degradation.py** - Fallback Strategies
**Concepts**: Fallback patterns, cache strategies, multi-level degradation

**What it does**:
- Primary tool fails → Use fallback tool
- API unavailable → Use cached data
- Advanced feature fails → Use simple alternative
- ALL tools fail → Return manual/approximate response

**Key Learning**: NEVER return just "error" - always provide SOMETHING!

```python
# 3-Level Fallback Strategy
def get_weather(location):
    # Level 1: Try real-time API (best)
    try:
        return api_weather(location)
    except:
        pass

    # Level 2: Try cache (good)
    if location in cache:
        return cache[location] + " (cached from 1 hour ago)"

    # Level 3: Generic response (acceptable)
    return "Weather data unavailable. Check weather.com"
```

**Output**:
```
Attempt 1:
⚠️  Level 3: Generic response
Agent: "Weather data temporarily unavailable. Check weather.com"

Attempt 2:
✅ Level 1: Real-time weather
Agent: "Weather in San Francisco: 72°F, Sunny (real-time)"

Attempt 3:
⚠️  Level 2: Cached weather
Agent: "Weather: 70°F, Partly cloudy (cached from 1 hour ago)"
```

**User Experience**:
- ✅ GOOD: "Weather: 70°F (from cache, may not be current)"
- ❌ BAD: "Error 503: Service unavailable"

---

## 🔑 Key Concepts Summary

### **1. Two-Layer Error Handling**
```python
# Layer 1: Tool level
@tool
def my_tool(param):
    try:
        return process(param)
    except Exception as e:
        return f"Error: {e}"

# Layer 2: Agent level
try:
    result = agent.invoke(messages)
except Exception as e:
    # Handle API/network errors
    retry_or_fallback()
```

### **2. Exponential Backoff Formula**
```
delay = initial_delay * (exponential_base ^ attempt)

Attempt 1: 1s
Attempt 2: 2s  (1 × 2¹)
Attempt 3: 4s  (1 × 2²)
Attempt 4: 8s  (1 × 2³)
```

### **3. Jitter (Randomness)**
```python
actual_delay = delay * (0.5 + random.random())

# Instead of ALL clients retrying at exactly 2s:
# Client 1: Retries at 1.7s
# Client 2: Retries at 2.3s
# Client 3: Retries at 1.9s
# Spreads load!
```

### **4. Input Validation Checklist**
- [ ] Type validation (convert to correct type)
- [ ] Range validation (min/max values)
- [ ] Special values (NaN, Infinity, null)
- [ ] Format validation (email, URL, phone)
- [ ] Length limits (prevent DoS)
- [ ] Character sanitization (remove dangerous chars)

### **5. Graceful Degradation Levels**
```
Level 1: Real-time API ✅ (best, but might fail)
Level 2: Recent cache ⚠️  (good, reliable)
Level 3: Stale cache ⚠️  (acceptable, always works)
Level 4: Manual/generic ⚠️  (last resort)
```

---

## 🚀 Running the Programs

```bash
# Navigate to directory
cd /home/intruder/langchain_learning/examples

# Activate virtual environment
source ../venv_langchain_dec2025/bin/activate

# Set Python path
export PYTHONPATH=/home/intruder/langchain_learning/examples:$PYTHONPATH

# Run programs
python day13_error_handling/13_01_basic_error_handling.py
python day13_error_handling/13_02_retry_mechanism.py
python day13_error_handling/13_03_input_validation.py
python day13_error_handling/13_04_graceful_degradation.py
```

---

## 📊 Production Impact

### **Without Error Handling** ❌
```
User: "Calculate 10 / 0"
System: [CRASH] ZeroDivisionError
User: Sees stack trace, confused
Developer: Gets angry support tickets
```

### **With Error Handling** ✅
```
User: "Calculate 10 / 0"
System: Validates input, prevents division
Agent: "Cannot divide by zero. Please provide non-zero divisor."
User: Understands the issue
Developer: Sleeps peacefully
```

### **Without Retry** ❌
```
API: [Temporary timeout]
System: Returns error immediately
User: "App is broken!"
```

### **With Retry** ✅
```
API: [Temporary timeout]
System: Retries automatically (1s, 2s, 4s)
API: Recovers on 3rd attempt
System: Returns result
User: Never knows anything failed
```

---

## 🛡️ Production Checklist

### **Error Handling**
- [x] Try/except around all tool logic
- [x] Try/except around agent.invoke()
- [x] Validate inputs before processing
- [x] Return user-friendly error messages
- [x] Log errors for debugging
- [x] Never expose internal errors to users

### **Retry Logic**
- [x] Retry on transient errors only
- [x] Exponential backoff (not linear)
- [x] Add jitter for distributed systems
- [x] Set max retry limit (prevent infinite loops)
- [x] Log all retry attempts
- [x] Timeout for total retry duration

### **Input Validation**
- [x] Type validation
- [x] Range validation
- [x] Format validation
- [x] Length limits
- [x] Sanitize strings
- [x] Check for NaN/Infinity
- [x] Prevent overflow

### **Graceful Degradation**
- [x] Primary + fallback tools
- [x] Cache for offline operation
- [x] Multiple data freshness levels
- [x] Transparent to user
- [x] Always return SOMETHING
- [x] Indicate data quality

---

## 💡 Best Practices

### **1. When to Retry**
```python
# ✅ RETRY these:
- Network timeouts
- Rate limits (429)
- Service unavailable (503)
- Temporary API errors

# ❌ DON'T RETRY these:
- Authentication errors (401)
- Bad request (400)
- Not found (404)
- Logic errors (validation failures)
```

### **2. Error Message Quality**
```python
# ❌ Bad
return "Error"

# ⚠️  Better
return "API Error: 503"

# ✅ Best
return "Service temporarily unavailable. Please try again in a moment."
```

### **3. Fail Open vs Fail Closed**
```python
# Security features: Fail CLOSED
if not validate_auth():
    return "Access denied"  # Deny by default

# Availability features: Fail OPEN
try:
    return get_realtime_data()
except:
    return get_cached_data()  # Degrade gracefully
```

---

## 🔥 Real-World Examples

### **Google Search**
```
Server 1 down → Try server 2
Server 2 down → Try server 3
All down → Cached results from 5 min ago
```

### **Netflix**
```
4K stream fails → 1080p
1080p fails → 720p
720p fails → 480p
480p fails → Pause and buffer
```

### **E-commerce**
```
Real-time inventory fails → Cached (warn: may be outdated)
Payment API fails → Queue order for processing
Shipping calc fails → Manual estimate
```

---

## 🎯 What's Next?

**Day 14**: Week 2 Integration Project
- Combine ALL Week 2 concepts
- Production-grade system
- Error handling + Streaming + RAG + Agents

---

**Author**: Klement
**Repository**: https://github.com/KlementMultiverse/langchain_v1.1
**Learning Journey**: 3-Week LangChain Production Mastery

---

## 📝 Quick Reference

```python
# Error Handling Pattern
try:
    result = tool.invoke(input)
except SpecificError as e:
    handle_specific(e)
except Exception as e:
    log_error(e)
    return user_friendly_message

# Retry Pattern
@retry_with_exponential_backoff(max_retries=3)
def unreliable_function():
    return api_call()

# Validation Pattern
is_valid, error, value = validate_number(input, min=0, max=100)
if not is_valid:
    return error

# Fallback Pattern
try:
    return primary_tool()
except:
    try:
        return fallback_tool()
    except:
        return manual_response()
```

🎉 **Production-ready error handling complete!**
