"""
  Lesson 5: LangChain + Pydantic = Structured Output

  What we're learning:
  - How to use .with_structured_output() with Pydantic models
  - Extract structured data from unstructured text
  - See the complete extraction pipeline in action

  This is THE production pattern for data extraction!

  Author: Klement
  Date: December 13, 2025
  Tech: LangChain 1.1.3, Pydantic v2, Ollama (qwen3:4b)
  """



from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field
import json
from typing import Optional

print("="*60)
print("LESSON 5: LangChain + Pydantic Structured Output")
print("="*60)
 
# Step 1 Define what we want to extract (Pydantic Model)
class PersonInfo(BaseModel):
	"""Information about a person extracted from text"""
	name: str = Field(description="Full name of the person")
	age: int = Field(description="Age in years")
	city: str = Field(description="City name only, without state or country (e.g., 'Austin' not 'Austin, Texas')")
	occupation: Optional[str] = Field(default=None, description="Person's job title, profession, or career (e.g., engineer, data scientist, teacher)") 
	email: Optional[str] = Field(default=None, description=" Email address if mentioned")

print("\n1.Pydantic model defined")
print("-" * 60)
print(" We want to extract to name, age, city, occupation, email")
print(" Required Fields: name, age, city")
print(" Optional fields: occupation, email")

# Step 2: Create llm with structured output
print("\n2.Setting up LLM with structured output")
print("-" * 60)
model = ChatOllama(model="qwen3:4b", temperature=0)

# Magic line - Connect Pydantic model to LLM
# Using format="json" instead of method="json_mode" for better field name compliance
structured_llm = model.with_structured_output(PersonInfo)
print("✅ LLM configured to output PersonInfo objects")
print("✅ Using .with_structured_output() !")

# Step 3: Extract from unstructured text
print("\n3. Extracting Data from Text:")
print("-" * 60)

# Example 1: Simple text
text1 = "Hi, I'm John Smith, 30 years old, living in New York. I work as a software engineer."

print(f"Input text: \"{text1}\"")
print("\nExtracting...")
 
result1 = structured_llm.invoke(text1)

print(f"\n✅ Extracted Data:")
print(f"   Name: {result1.name}")
print(f"   Age: {result1.age}")
print(f"   City: {result1.city}")
print(f"   Occupation: {result1.occupation}")
print(f"   Email: {result1.email}")


# Example 2: Missing optional fields
print("\n" + "="*60)
print("4. Handling Missing Optional Fields:")
print("-" * 60)
text2 = "My name is Sarah Johnson, I'm 28, and I live in San Francisco."

print(f"Input text: \"{text2}\"")
print("\nExtracting...")

result2 = structured_llm.invoke(text2)
print(f"\n✅ Extracted Data:")
print(f"   Name: {result2.name}")
print(f"   Age: {result2.age}")
print(f"   City: {result2.city}")
print(f"   Occupation: {result2.occupation} ← No occupation mentioned, defaults to None")
print(f"   Email: {result2.email} ← No email mentioned, defaults to None")

# Example 3: More complex text with all fields
print("\n" + "="*60)
print("5. Complex Text with All Fields:")
print("-" * 60)

text3 = """
Extract person information from this text. For city, extract ONLY the city name without state.
For occupation, extract the job title if mentioned.

Text: Meet Alice Cooper, a 35-year-old data scientist based in Austin, Texas.
You can reach her at alice.cooper@email.com for consulting opportunities.
"""

print(f"Input text: {text3}")
print("\nExtracting...")
result3 = structured_llm.invoke(text3)

print(f"\n✅ Extracted Data:")
print(f"   Name: {result3.name}")
print(f"   Age: {result3.age}")
print(f"   City: {result3.city}")
print(f"   Occupation: {result3.occupation}")
print(f"   Email: {result3.email}")


# Show the JSON representation
print("\n" + "="*60)
print("6. JSON Representation (for APIs/databases):")
print("-" * 60)
print(json.dumps(result3.model_dump(), indent=2))

print(result3.model_dump())

print("\n" + "="*60)
print("KEY POINTS:")
print("="*60)
print("✅ Define Pydantic model = Define what to extract")
print("✅ .with_structured_output(Model) = Connect LLM to model")
print("✅ LLM.invoke(text) = Get validated Pydantic object back")
print("✅ Optional fields handle missing data gracefully")
print("✅ Prompt engineering in text helps guide extraction")
print("✅ .model_dump() converts to dict/JSON for database/API")
print("✅ Result is type-safe, validated, ready for production!")
print()
print("PRODUCTION USE CASES:")
print("  • Resume parsing → Extract skills, experience, education")
print("  • Invoice processing → Extract line items, totals, dates")
print("  • Customer support → Extract intent, sentiment, priority")
print("  • Document analysis → Extract key entities, relationships")


