"""
Lesson 4: Nested Pydantic Models

What we're learning:
- How to nest one Pydantic model inside another
- How to validate complex hierarchical data
- What LLM sees for nested structures in JSON Schema

Author: Klement
Date: December 13, 2025
Tech: Pydantic v2
"""

from pydantic import BaseModel, Field
from typing import List
import json

print("="*60)
print("LESSON 4: Nested Pydantic Models")
print("="*60)

# Step 1: Create the nested model (Address)
class Address(BaseModel):
    """Physical address"""
    street: str = Field(description="Street address")
    city: str = Field(description="City name")
    country: str = Field(description="Country name")
    zipcode: str = Field(description="Postal code")

# Step 2: Use it inside another model (Person)
class Person(BaseModel):
    """Person with nested address"""
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")
    address: Address  # ← NESTED MODEL!

print("\n1. Creating person with nested address:")
print("-" * 60)

# Create an address first
home_address = Address(
    street="123 Main St",
    city="New York",
    country="USA",
    zipcode="10001"
)

# Create person with that address
john = Person(
    name="John Smith",
    age=30,
    address=home_address
)

print(f"✅ Person: {john.name}, {john.age}")
print(f"✅ Address: {john.address.street}, {john.address.city}")

# OR create it all at once using a dictionary
print("\n2. Creating person with inline address (from dict):")
print("-" * 60)

jane = Person(
    name="Jane Doe",
    age=28,
    address={
        "street": "456 Oak Ave",
        "city": "Los Angeles",
        "country": "USA",
        "zipcode": "90001"
    }
)

print(f"✅ Person: {jane.name}, {jane.age}")
print(f"✅ Address: {jane.address.street}, {jane.address.city}")

# Step 3: Even deeper nesting - Person with multiple addresses
class PersonWithMultipleAddresses(BaseModel):
    """Person with list of addresses"""
    name: str
    age: int
    addresses: List[Address]  # ← LIST of nested models!

print("\n3. Person with MULTIPLE addresses:")
print("-" * 60)

bob = PersonWithMultipleAddresses(
    name="Bob Johnson",
    age=45,
    addresses=[
        {"street": "789 Pine St", "city": "Chicago", "country": "USA", "zipcode": "60601"},
        {"street": "321 Elm Rd", "city": "Miami", "country": "USA", "zipcode": "33101"}
    ]
)

print(f"✅ Person: {bob.name}, {bob.age}")
print(f"✅ Has {len(bob.addresses)} addresses:")
for i, addr in enumerate(bob.addresses, 1):
    print(f"   {i}. {addr.city}, {addr.country}")

# THE IMPORTANT PART - See the nested JSON Schema
print("\n" + "="*60)
print("WHAT THE LLM SEES (Nested JSON Schema):")
print("="*60)

schema = Person.model_json_schema()
print(json.dumps(schema, indent=2))

print("\n" + "="*60)
print("KEY POINTS:")
print("="*60)
print("✅ Nest models by using them as field types: address: Address")
print("✅ Pydantic validates the ENTIRE nested structure")
print("✅ LLM sees the full hierarchy in JSON Schema")
print("✅ Use List[Model] for multiple nested objects")
print("✅ This is how you extract complex real-world data!")
print()
print("REAL-WORLD EXAMPLES:")
print("  • Invoice → List[LineItem]")
print("  • Resume → List[JobExperience]")
print("  • Order → List[Product]")
