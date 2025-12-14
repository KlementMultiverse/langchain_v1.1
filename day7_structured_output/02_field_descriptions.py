"""
Lesson 2: Field Descriptions - Guide the LLM

What we're learning:
- How to add descriptions to Pydantic fields
- How to set constraints (min/max values)
- How to see what the LLM actually sees (JSON Schema)

Author: Klement
Date: December 13, 2025
Tech: Pydantic v2
"""

from pydantic import BaseModel, Field
import json

# Before: Basic Pydantic (Lesson 1)
# class Person(BaseModel):
#     name: str
#     age: int

# After: With Field descriptions and constraints
class Person(BaseModel):
    """A person with validated data"""
    name: str = Field(description="Full name of the person")
    age: int = Field(description="Age in years", ge=0, le=120)
    email: str = Field(description="Email address")
    city: str = Field(description="City where person lives")

print("="*60)
print("LESSON 2: Field Descriptions & Constraints")
print("="*60)

# 1. Create valid person
print("\n1. Creating valid person:")
john = Person(
    name="John Smith",
    age=30,
    email="john@email.com",
    city="New York"
)
print(f"✅ Valid: {john.name}, {john.age}, {john.city}")

# 2. Test constraints (age must be 0-120)
print("\n2. Testing age constraint (must be 0-120):")
try:
    old = Person(
        name="Ancient One",
        age=500,
        email="ancient@email.com",
        city="Atlantis"
    )
except Exception as e:
    print("❌ Validation failed!")
    print("   Age 500 is INVALID (must be 0-120)")

# THIS IS THE IMPORTANT PART - See what LLM sees!
print("\n" + "="*60)
print("WHAT THE LLM SEES (JSON Schema):")
print("="*60)

schema = Person.model_json_schema()
print(json.dumps(schema, indent=2))

print("\n" + "="*60)
print("KEY POINTS:")
print("="*60)
print("✅ Field descriptions tell LLM what to extract")
print("✅ Constraints (ge=0, le=120) enforce data rules")
print("✅ model_json_schema() shows what LLM actually sees")
print("✅ This is how you debug LLM extraction issues!")
