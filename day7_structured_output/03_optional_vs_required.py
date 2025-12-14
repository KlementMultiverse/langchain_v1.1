"""
Lesson 3: Required vs Optional Fields

What we're learning:
- How Pydantic decides if a field is required or optional
- How to make fields optional
- What LLM sees in JSON Schema for both

Author: Klement
Date: December 13, 2025
Tech: Pydantic v2
"""

from pydantic import BaseModel, Field
from typing import Optional
import json

print("="*60)
print("LESSON 3: Required vs Optional Fields")
print("="*60)

# Example 1: ALL REQUIRED (no default values)
class PersonRequired(BaseModel):
    """All fields are required"""
    name: str
    age: int
    city: str

print("\n1. ALL REQUIRED FIELDS (no defaults):")
print("-" * 60)

# This works - all fields provided
person1 = PersonRequired(name="John", age=30, city="NYC")
print(f"✅ All fields provided: {person1.name}, {person1.age}, {person1.city}")

# This fails - missing city
try:
    person2 = PersonRequired(name="Jane", age=25)
except Exception as e:
    print(f"❌ Missing 'city' field → Error!")
    print(f"   Pydantic says: Field required")

# See the JSON Schema
schema1 = PersonRequired.model_json_schema()
print("\nJSON Schema (see 'required' list):")
print(f"Required fields: {schema1['required']}")

# Example 2: SOME OPTIONAL (with default values)
class PersonOptional(BaseModel):
    """Some fields are optional"""
    name: str                    # ← Required (no default)
    age: int                     # ← Required (no default)
    city: str = "Unknown"        # ← Optional (has default)
    country: str = "USA"         # ← Optional (has default)

print("\n" + "="*60)
print("2. SOME OPTIONAL FIELDS (have defaults):")
print("-" * 60)

# This works - optional fields use defaults
person3 = PersonOptional(name="Bob", age=40)
print(f"✅ Only required fields: {person3.name}, {person3.age}")
print(f"   Optional fields used defaults: {person3.city}, {person3.country}")

# This also works - override defaults
person4 = PersonOptional(name="Alice", age=35, city="London", country="UK")
print(f"✅ All fields provided: {person4.name}, {person4.city}, {person4.country}")

# See the JSON Schema
schema2 = PersonOptional.model_json_schema()
print("\nJSON Schema (see 'required' list):")
print(f"Required fields: {schema2['required']}")
print(f"All fields: {list(schema2['properties'].keys())}")

# Example 3: TRULY OPTIONAL (can be None)
class PersonNullable(BaseModel):
    """Some fields can be None"""
    name: str                        # ← Required, cannot be None
    age: int                         # ← Required, cannot be None
    city: Optional[str] = None       # ← Optional, can be None
    email: Optional[str] = None      # ← Optional, can be None

print("\n" + "="*60)
print("3. NULLABLE FIELDS (Optional[type]):")
print("-" * 60)

# This works - optional fields are None
person5 = PersonNullable(name="Charlie", age=50)
print(f"✅ Only required: {person5.name}, {person5.age}")
print(f"   Nullable fields: city={person5.city}, email={person5.email}")

# This also works - provide values
person6 = PersonNullable(name="Diana", age=28, city="Paris", email="diana@email.com")
print(f"✅ All provided: {person6.name}, {person6.city}, {person6.email}")

# See the JSON Schema
schema3 = PersonNullable.model_json_schema()
print("\nJSON Schema (see what's required):")
print(f"Required fields: {schema3['required']}")
print("\nFull JSON Schema for PersonNullable:")
print(json.dumps(schema3, indent=2))

print("\n" + "="*60)
print("KEY RULES:")
print("="*60)
print("1. NO DEFAULT VALUE → Required in JSON Schema")
print("   Example: name: str")
print()
print("2. HAS DEFAULT VALUE → Optional in JSON Schema")
print("   Example: city: str = 'Unknown'")
print()
print("3. OPTIONAL[TYPE] → Can be None, not required")
print("   Example: email: Optional[str] = None")
print()
print("✅ Pydantic automatically creates 'required' list!")
print("✅ LLM sees this in JSON Schema and knows what's mandatory!")
