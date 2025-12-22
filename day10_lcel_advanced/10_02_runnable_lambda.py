"""
Day 10 - LCEL Advanced: RunnableLambda
=======================================

CONCEPT: RunnableLambda lets you insert custom Python functions into LCEL chains.

DIFFERENCE FROM RunnablePassthrough:
- RunnablePassthrough = Pass data UNCHANGED
- RunnableLambda = TRANSFORM data with your function

USE CASE: Data preprocessing, cleaning, validation, API calls, custom logic

PRODUCTION PATTERN: Insert business logic into LLM chains
"""

from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Initialize model
model = ChatOllama(model="qwen3:4b", temperature=0.7)


# ============================================
# EXAMPLE 1: Basic RunnableLambda
# ============================================
print("=" * 60)
print("EXAMPLE 1: Basic RunnableLambda - Simple transformation")
print("=" * 60)

def uppercase_text(text):
    """Convert text to uppercase"""
    return text.upper()

# Create a runnable from the function
uppercase_runnable = RunnableLambda(uppercase_text)

# Test it standalone
input_text = "hello world"
output = uppercase_runnable.invoke(input_text)

print(f"Input:  {input_text}")
print(f"Output: {output}\n")


# ============================================
# EXAMPLE 2: RunnableLambda in a Chain
# ============================================
print("=" * 60)
print("EXAMPLE 2: RunnableLambda for preprocessing")
print("=" * 60)

def clean_text(text):
    """Remove extra whitespace and lowercase"""
    return text.strip().lower()

def extract_keywords(text):
    """Extract words longer than 3 characters"""
    words = text.split()
    keywords = [w for w in words if len(w) > 3]
    return ", ".join(keywords)

# Build chain: clean → extract keywords → analyze with AI
template = "Analyze these keywords and provide insights: {keywords}"
prompt = ChatPromptTemplate.from_template(template)

analysis_chain = (
    RunnableLambda(clean_text)           # Step 1: Clean
    | RunnableLambda(extract_keywords)   # Step 2: Extract keywords
    | (lambda kw: {"keywords": kw})      # Step 3: Format for prompt
    | prompt                              # Step 4: Create prompt
    | model                               # Step 5: AI analysis
    | StrOutputParser()                   # Step 6: Parse output
)

dirty_input = "  LangChain is a FRAMEWORK for building AI applications  "
result = analysis_chain.invoke(dirty_input)

print(f"Original input: '{dirty_input}'")
print(f"After cleaning:  'langchain is a framework for building ai applications'")
print(f"Keywords extracted: 'langchain, framework, building, applications'")
print(f"AI Analysis: {result}\n")


# ============================================
# EXAMPLE 3: Data Validation with RunnableLambda
# ============================================
print("=" * 60)
print("EXAMPLE 3: Input validation")
print("=" * 60)

def validate_and_clean_email(email):
    """Validate email format and clean it"""
    email = email.strip().lower()

    # Basic validation
    if "@" not in email or "." not in email:
        return {"valid": False, "email": email, "error": "Invalid email format"}

    return {"valid": True, "email": email, "error": None}

# Chain: validate → format response
validation_chain = RunnableLambda(validate_and_clean_email)

# Test with valid email
valid_email = "  User@Example.COM  "
result1 = validation_chain.invoke(valid_email)
print(f"Input: '{valid_email}'")
print(f"Result: {result1}")

# Test with invalid email
invalid_email = "not-an-email"
result2 = validation_chain.invoke(invalid_email)
print(f"\nInput: '{invalid_email}'")
print(f"Result: {result2}\n")


# ============================================
# EXAMPLE 4: Simulating API Call with RunnableLambda
# ============================================
print("=" * 60)
print("EXAMPLE 4: External data fetching (simulated API)")
print("=" * 60)

def fetch_user_data(user_id):
    """Simulates fetching user data from API"""
    # In production: requests.get(f"api.example.com/users/{user_id}")
    user_database = {
        "101": {"name": "Alice", "role": "Engineer", "projects": 5},
        "102": {"name": "Bob", "role": "Designer", "projects": 3},
        "103": {"name": "Charlie", "role": "Manager", "projects": 8}
    }
    return user_database.get(user_id, {"error": "User not found"})

def format_user_summary(user_data):
    """Format user data for LLM"""
    if "error" in user_data:
        return user_data["error"]

    return f"Name: {user_data['name']}, Role: {user_data['role']}, Projects: {user_data['projects']}"

# Chain: fetch data → format → create personalized message
template = """Based on this user info: {user_info}

Write a personalized greeting message for them."""

prompt = ChatPromptTemplate.from_template(template)

user_greeting_chain = (
    RunnableLambda(fetch_user_data)      # Fetch from "API"
    | RunnableLambda(format_user_summary) # Format for LLM
    | (lambda info: {"user_info": info})  # Prepare for prompt
    | prompt                               # Create prompt
    | model                                # Generate greeting
    | StrOutputParser()
)

user_id = "101"
greeting = user_greeting_chain.invoke(user_id)

print(f"User ID: {user_id}")
print(f"Greeting: {greeting}\n")


# ============================================
# EXAMPLE 5: Combining Multiple Transformations
# ============================================
print("=" * 60)
print("EXAMPLE 5: Data pipeline with multiple RunnableLambdas")
print("=" * 60)

def count_words(text):
    """Count words in text"""
    return {"text": text, "word_count": len(text.split())}

def categorize_length(data):
    """Categorize text by length"""
    count = data["word_count"]
    if count < 5:
        category = "very short"
    elif count < 15:
        category = "short"
    elif count < 30:
        category = "medium"
    else:
        category = "long"

    return {**data, "category": category}

def create_summary(data):
    """Create human-readable summary"""
    return f"Text length: {data['category']} ({data['word_count']} words)"

# Multi-step transformation pipeline
pipeline = (
    RunnableLambda(count_words)
    | RunnableLambda(categorize_length)
    | RunnableLambda(create_summary)
)

test_texts = [
    "Hello",
    "LangChain makes building AI applications easy",
    "This is a medium length text that demonstrates how the pipeline categorizes different text lengths based on word count"
]

for text in test_texts:
    result = pipeline.invoke(text)
    print(f"Text: '{text[:50]}...'")
    print(f"Summary: {result}\n")


# ============================================
# COMPARISON: RunnablePassthrough vs RunnableLambda
# ============================================
print("=" * 60)
print("WHEN TO USE WHICH?")
print("=" * 60)
print("""
RunnablePassthrough:
✅ Pass data UNCHANGED
✅ Use same input in multiple places
✅ Example: RAG (question goes to retriever AND prompt)

RunnableLambda:
✅ TRANSFORM data with custom function
✅ Data cleaning, validation, API calls
✅ Example: Clean text before sending to AI

REAL EXAMPLE - RAG with preprocessing:
{
    "context": retriever,
    "question": RunnableLambda(clean_question)  # Clean before passing!
}

Why not RunnablePassthrough for question?
Because we need to CLEAN it first!
""")

print("\n✅ Day 10 - Program 2 Complete!")
print("Next: 10_03_parallel_execution.py - Run multiple tasks at once\n")
