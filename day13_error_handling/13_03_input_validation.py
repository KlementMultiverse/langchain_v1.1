"""
Day 13 - Program 3: Input Validation & Sanitization

NEVER trust user input! Production systems must validate and sanitize ALL inputs.

Security risks:
- SQL injection
- Prompt injection
- Invalid data types
- Out-of-range values
- Malicious code

Author: Klement
Date: December 23, 2025
Tech: LangChain 1.2, Input Validation, Security
"""

import sys
sys.path.insert(0, '/home/intruder/langchain_learning/examples')

import re
from typing import Union
from common_config import get_model
from langchain_core.tools import tool
from langchain.agents import create_agent

print("🛡️ Day 13 - Program 3: Input Validation & Sanitization\n")

# STEP 1: Input validation helpers
def validate_number(value: any, min_val: float = None, max_val: float = None) -> tuple[bool, str, float]:
    """
    Validate and convert input to number.

    Returns: (is_valid, error_message, converted_value)
    """
    try:
        num = float(value)

        # Check for NaN or Infinity
        if not (num == num):  # NaN check
            return False, "Invalid number: NaN", 0.0
        if num == float('inf') or num == float('-inf'):
            return False, "Invalid number: Infinity", 0.0

        # Range validation
        if min_val is not None and num < min_val:
            return False, f"Number must be >= {min_val}", 0.0
        if max_val is not None and num > max_val:
            return False, f"Number must be <= {max_val}", 0.0

        return True, "", num

    except (ValueError, TypeError):
        return False, f"Cannot convert '{value}' to number", 0.0

def sanitize_string(text: str, max_length: int = 1000) -> str:
    """
    Sanitize user input string.

    Removes:
    - Dangerous characters
    - Excessive whitespace
    - Control characters
    """
    if not isinstance(text, str):
        return ""

    # Remove control characters
    text = ''.join(char for char in text if char.isprintable() or char in '\n\t ')

    # Trim to max length
    if len(text) > max_length:
        text = text[:max_length]

    # Remove excessive whitespace
    text = ' '.join(text.split())

    return text.strip()

def validate_email(email: str) -> tuple[bool, str]:
    """Simple email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, email.lower()
    return False, "Invalid email format"

# STEP 2: Tools with input validation
@tool
def safe_power(base: float, exponent: float) -> str:
    """Calculate base^exponent with validation to prevent overflow."""

    # Validate base
    is_valid, error, base_num = validate_number(base, min_val=-1000, max_val=1000)
    if not is_valid:
        return f"Base error: {error}"

    # Validate exponent
    is_valid, error, exp_num = validate_number(exponent, min_val=-100, max_val=100)
    if not is_valid:
        return f"Exponent error: {error}"

    try:
        # Check for potential overflow
        if abs(base_num) > 100 and abs(exp_num) > 10:
            return "Error: Result would be too large (overflow risk)"

        result = base_num ** exp_num

        # Verify result is reasonable
        if abs(result) > 1e50:
            return "Error: Result exceeds safe limits"

        print(f"  ✅ {base_num}^{exp_num} = {result}")
        return f"Result: {result}"

    except OverflowError:
        return "Error: Calculation overflow"
    except Exception as e:
        return f"Error: {str(e)}"

@tool
def calculate_age(birth_year: int) -> str:
    """Calculate age with validation."""

    # Validate birth year
    is_valid, error, year = validate_number(birth_year, min_val=1900, max_val=2025)
    if not is_valid:
        return f"Invalid birth year: {error}"

    year = int(year)
    current_year = 2025
    age = current_year - year

    if age < 0:
        return "Error: Birth year is in the future"
    if age > 125:
        return "Error: Age seems unrealistic (>125 years)"

    print(f"  ✅ Birth year {year} → Age: {age}")
    return f"{age} years old"

@tool
def validate_user_data(name: str, email: str, age: int) -> str:
    """Validate complete user data."""

    errors = []

    # Validate name
    sanitized_name = sanitize_string(name, max_length=100)
    if not sanitized_name or len(sanitized_name) < 2:
        errors.append("Name must be at least 2 characters")

    # Validate email
    is_valid, email_result = validate_email(email)
    if not is_valid:
        errors.append(email_result)

    # Validate age
    is_valid, error, age_num = validate_number(age, min_val=0, max_val=150)
    if not is_valid:
        errors.append(f"Age: {error}")

    if errors:
        return f"Validation errors: {'; '.join(errors)}"

    print(f"  ✅ Valid user: {sanitized_name}, {email_result}, age {int(age_num)}")
    return f"User validated: {sanitized_name} ({email_result}), age {int(age_num)}"

# STEP 3: Create agent with validation-focused system prompt
print("Creating agent with input validation...\n")

model = get_model(temperature=0)
agent = create_agent(
    model=model,
    tools=[safe_power, calculate_age, validate_user_data],
    system_prompt="""You are a security-conscious assistant.

CRITICAL: Always validate user input before using tools!
- Numbers: Check ranges, no NaN/Infinity
- Strings: Sanitize, check length
- Emails: Validate format
- Dates/Ages: Check realistic ranges"""
)

# STEP 4: Test validation scenarios
print("=" * 70)
print("TEST 1: Valid power calculation")
print("=" * 70)
result1 = agent.invoke({"messages": [("user", "Calculate 2 to the power of 10")]})
print(f"🤖 Agent: {result1['messages'][-1].content}\n")

print("=" * 70)
print("TEST 2: Overflow prevention (huge number)")
print("=" * 70)
result2 = agent.invoke({"messages": [("user", "Calculate 999 to the power of 999")]})
print(f"🤖 Agent: {result2['messages'][-1].content}\n")

print("=" * 70)
print("TEST 3: Valid age calculation")
print("=" * 70)
result3 = agent.invoke({"messages": [("user", "If I was born in 1990, how old am I?")]})
print(f"🤖 Agent: {result3['messages'][-1].content}\n")

print("=" * 70)
print("TEST 4: Invalid birth year (future)")
print("=" * 70)
result4 = agent.invoke({"messages": [("user", "Calculate age for birth year 2030")]})
print(f"🤖 Agent: {result4['messages'][-1].content}\n")

print("=" * 70)
print("TEST 5: User data validation (all valid)")
print("=" * 70)
result5 = agent.invoke({"messages": [("user", "Validate user: Klement, klement@example.com, age 25")]})
print(f"🤖 Agent: {result5['messages'][-1].content}\n")

print("=" * 70)
print("TEST 6: User data validation (invalid email)")
print("=" * 70)
result6 = agent.invoke({"messages": [("user", "Validate user: John, not-an-email, age 30")]})
print(f"🤖 Agent: {result6['messages'][-1].content}\n")

print("\n" + "=" * 70)
print("🎯 KEY LEARNINGS:")
print("=" * 70)
print("""
✅ INPUT VALIDATION PRINCIPLES:

1. **NEVER TRUST USER INPUT**
   - Always validate before processing
   - Sanitize strings (remove dangerous chars)
   - Check ranges (min/max values)
   - Verify data types

2. **Validation Pattern**:
   ```python
   def validate_number(value, min_val, max_val):
       # 1. Type conversion
       try:
           num = float(value)
       except ValueError:
           return False, "Not a number"

       # 2. Special values
       if num is NaN or Infinity:
           return False, "Invalid"

       # 3. Range check
       if num < min_val or num > max_val:
           return False, "Out of range"

       return True, num
   ```

3. **String Sanitization**:
   ✅ Remove control characters
   ✅ Trim to max length
   ✅ Remove excessive whitespace
   ✅ Strip dangerous patterns

4. **Common Validation Checks**:
   - **Numbers**: Range, NaN, Infinity, overflow
   - **Strings**: Length, charset, dangerous patterns
   - **Emails**: Format validation
   - **Dates**: Realistic ranges
   - **URLs**: Protocol, domain validation
   - **Files**: Extension, size, content type

5. **Security Considerations**:
   ❌ SQL Injection: "'; DROP TABLE users; --"
   ❌ Prompt Injection: "Ignore previous instructions..."
   ❌ Path Traversal: "../../etc/passwd"
   ❌ Code Injection: "'; import os; os.system('rm -rf /')"

   ✅ Solution: Validate and sanitize EVERYTHING!

🛡️ PRODUCTION VALIDATION CHECKLIST:
   - [x] Type validation (int, float, string, etc.)
   - [x] Range validation (min/max)
   - [x] Format validation (email, URL, phone)
   - [x] Length limits (prevent DoS)
   - [x] Sanitize strings (remove dangerous chars)
   - [x] Check for NaN/Infinity
   - [x] Prevent overflow
   - [x] User-friendly error messages

💡 VALIDATION BEST PRACTICES:
   1. Validate at entry point (before tools)
   2. Use allowlists (not blocklists)
   3. Fail closed (reject if unsure)
   4. Return clear error messages
   5. Log validation failures
   6. Never expose internal errors to users

📊 REAL-WORLD IMPACT:
   Without validation: "999^999" crashes your server ❌
   With validation: "Result too large" error message ✅

🔥 NEXT: Graceful Degradation (fallback strategies)!
""")

print("\n✅ Day 13 - Program 3 Complete!")
print("🎓 You now understand: Input validation & sanitization!")
