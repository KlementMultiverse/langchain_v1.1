"""
Day 10 - LCEL Advanced: RunnableBranch (Conditional Routing)
=============================================================

CONCEPT: RunnableBranch adds IF/ELSE logic to your chains

THINK OF IT AS: "If condition A, do this. Else if condition B, do that. Otherwise, default."

WHY IT MATTERS: Different inputs need different handling!

EXAMPLE:
- If question is about code → Route to code expert
- Else if question is about math → Route to math expert
- Else → Route to general assistant

USE CASE: Smart routing, personalization, multi-agent systems

PRODUCTION PATTERN: Customer service bots, intelligent assistants
"""

from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Initialize model
model = ChatOllama(model="qwen3:4b", temperature=0.7)


# ============================================
# EXAMPLE 1: Simple Branching (Text Length)
# ============================================
print("=" * 60)
print("EXAMPLE 1: Route based on text length")
print("=" * 60)

def is_short(text):
    """Check if text is short"""
    return len(text.split()) < 5

def is_medium(text):
    """Check if text is medium"""
    return 5 <= len(text.split()) < 15

# Define handlers for each branch
def handle_short(text):
    return f"SHORT text detected: '{text}' (Word count: {len(text.split())})"

def handle_medium(text):
    return f"MEDIUM text detected: '{text}' (Word count: {len(text.split())})"

def handle_long(text):
    return f"LONG text detected: '{text}' (Word count: {len(text.split())})"

# Create branching logic
branch = RunnableBranch(
    (is_short, RunnableLambda(handle_short)),      # If short → handler 1
    (is_medium, RunnableLambda(handle_medium)),    # Else if medium → handler 2
    RunnableLambda(handle_long)                    # Else → default handler
)

# Test with different lengths
test_texts = [
    "Hello",  # Short
    "LangChain makes building AI apps easy and fun",  # Medium
    "This is a long text that contains many words and will demonstrate how the branching logic routes longer inputs to the appropriate handler based on word count"  # Long
]

for text in test_texts:
    result = branch.invoke(text)
    print(result)

print()


# ============================================
# EXAMPLE 2: Route to Different AI Prompts
# ============================================
print("=" * 60)
print("EXAMPLE 2: Smart routing based on question type")
print("=" * 60)

def is_code_question(question):
    """Check if question is about programming"""
    code_keywords = ["code", "python", "function", "programming", "debug", "error"]
    return any(keyword in question.lower() for keyword in code_keywords)

def is_math_question(question):
    """Check if question is about math"""
    math_keywords = ["calculate", "math", "equation", "solve", "number"]
    return any(keyword in question.lower() for keyword in math_keywords)

# Define specialized prompts
code_template = """You are an expert programmer. Answer this coding question:

Question: {question}

Provide code examples where relevant."""

math_template = """You are a math expert. Solve this mathematical problem:

Question: {question}

Show step-by-step calculations."""

general_template = """You are a helpful assistant. Answer this question:

Question: {question}"""

code_prompt = ChatPromptTemplate.from_template(code_template)
math_prompt = ChatPromptTemplate.from_template(math_template)
general_prompt = ChatPromptTemplate.from_template(general_template)

# Create chains for each specialty
code_chain = code_prompt | model | StrOutputParser()
math_chain = math_prompt | model | StrOutputParser()
general_chain = general_prompt | model | StrOutputParser()

# Route based on question type
router = RunnableBranch(
    (is_code_question, code_chain),     # Code questions → Code expert
    (is_math_question, math_chain),     # Math questions → Math expert
    general_chain                        # Everything else → General assistant
)

# Create full chain: format input → route
smart_assistant = (
    RunnableLambda(lambda q: {"question": q})
    | router
)

# Test with different question types
questions = [
    "How do I write a Python function?",           # Code
    "Calculate 25 * 47",                          # Math
    "What is the capital of France?"              # General
]

for question in questions:
    print(f"Question: {question}")
    answer = smart_assistant.invoke(question)
    print(f"Answer: {answer}\n")


# ============================================
# EXAMPLE 3: User Role-Based Routing
# ============================================
print("=" * 60)
print("EXAMPLE 3: Personalization based on user role")
print("=" * 60)

def is_beginner(user_data):
    """Check if user is beginner"""
    return user_data.get("level") == "beginner"

def is_advanced(user_data):
    """Check if user is advanced"""
    return user_data.get("level") == "advanced"

# Different explanations for different levels
def explain_for_beginner(data):
    template = """Explain {topic} in VERY SIMPLE terms for a complete beginner.
Use analogies and avoid technical jargon."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"topic": data["topic"]})

def explain_for_intermediate(data):
    template = """Explain {topic} for someone with basic knowledge.
Include some technical details."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"topic": data["topic"]})

def explain_for_advanced(data):
    template = """Explain {topic} for an expert.
Go deep into technical details, edge cases, and best practices."""
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"topic": data["topic"]})

# Route based on user level
personalized_explainer = RunnableBranch(
    (is_beginner, RunnableLambda(explain_for_beginner)),
    (is_advanced, RunnableLambda(explain_for_advanced)),
    RunnableLambda(explain_for_intermediate)  # Default: intermediate
)

# Test with different user levels
users = [
    {"level": "beginner", "topic": "neural networks"},
    {"level": "intermediate", "topic": "neural networks"},
    {"level": "advanced", "topic": "neural networks"}
]

for user in users:
    print(f"User level: {user['level']}")
    print(f"Topic: {user['topic']}")
    explanation = personalized_explainer.invoke(user)
    print(f"Explanation: {explanation}\n")


# ============================================
# EXAMPLE 4: Language Detection + Routing
# ============================================
print("=" * 60)
print("EXAMPLE 4: Detect language and route accordingly")
print("=" * 60)

def is_spanish(text):
    """Simple Spanish detection"""
    spanish_words = ["hola", "como", "que", "es", "por", "gracias"]
    return any(word in text.lower() for word in spanish_words)

def is_french(text):
    """Simple French detection"""
    french_words = ["bonjour", "merci", "comment", "est", "le", "la"]
    return any(word in text.lower() for word in french_words)

def respond_in_spanish(text):
    template = "Responde en español: {text}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"text": text})

def respond_in_french(text):
    template = "Répondez en français: {text}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"text": text})

def respond_in_english(text):
    template = "Respond in English: {text}"
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"text": text})

# Language router
language_router = RunnableBranch(
    (is_spanish, RunnableLambda(respond_in_spanish)),
    (is_french, RunnableLambda(respond_in_french)),
    RunnableLambda(respond_in_english)
)

# Test
texts = [
    "Hola, como estas?",
    "Bonjour, comment allez-vous?",
    "Hello, how are you?"
]

for text in texts:
    print(f"Input: {text}")
    response = language_router.invoke(text)
    print(f"Response: {response}\n")


# ============================================
# PRODUCTION TIPS
# ============================================
print("=" * 60)
print("PRODUCTION TIPS: When to use RunnableBranch")
print("=" * 60)
print("""
✅ USE RunnableBranch when:
   - Different inputs need different handling
   - Route to specialized models/prompts
   - Personalization based on user data
   - Multi-agent systems (route to different agents)
   - A/B testing (route % of traffic)

❌ DON'T use when:
   - All inputs handled the same way
   - Simple linear processing

STRUCTURE:
RunnableBranch(
    (condition1, handler1),    # If condition1 → run handler1
    (condition2, handler2),    # Else if condition2 → run handler2
    default_handler            # Else → run default
)

REAL EXAMPLES:

1. Customer Service:
   - Billing question → Billing agent
   - Technical question → Tech support agent
   - General question → General agent

2. Content Moderation:
   - Toxic content → Block + log
   - Inappropriate → Warning
   - Clean → Approve

3. Smart Assistants:
   - Complex query → GPT-4 (expensive but smart)
   - Simple query → GPT-3.5 (cheap and fast)

4. Multi-language Support:
   - Spanish → Spanish model
   - French → French model
   - Default → English model
""")

print("\n✅ Day 10 - All Programs Complete! 🎉")
print("You've mastered LCEL Advanced Runnables!\n")
