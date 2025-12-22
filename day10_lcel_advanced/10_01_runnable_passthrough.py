"""
Day 10 - LCEL Advanced: RunnablePassthrough
============================================

CONCEPT: RunnablePassthrough allows you to pass data through chains unchanged
while also using it in other parts of the chain.

USE CASE: When you need the same input in multiple places in your chain.

PRODUCTION PATTERN: Data flow control in complex chains
"""

from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# Initialize model
model = ChatOllama(model="qwen3:4b", temperature=0.7)

# ============================================
# EXAMPLE 1: Basic RunnablePassthrough
# ============================================
print("=" * 60)
print("EXAMPLE 1: Basic RunnablePassthrough")
print("=" * 60)

# Simple chain that passes input through
chain = RunnablePassthrough() | model | StrOutputParser()

result = chain.invoke("What is machine learning in one sentence?")
print(f"\nInput passed through to model:\n{result}\n")


# ============================================
# EXAMPLE 2: RunnablePassthrough with assign()
# ============================================
print("=" * 60)
print("EXAMPLE 2: RunnablePassthrough.assign() - Add new data")
print("=" * 60)

def get_word_count(text):
    """Helper function to count words"""
    return len(text.split())

# Chain that adds word count to the input dictionary
chain_with_count = (
    RunnablePassthrough.assign(
        word_count=lambda x: get_word_count(x["text"])
    )
)

input_data = {"text": "LangChain is a framework for building LLM applications"}
result = chain_with_count.invoke(input_data)

print(f"\nOriginal input: {input_data}")
print(f"After assign: {result}")
print(f"  - Original text: {result['text']}")
print(f"  - Added word_count: {result['word_count']}\n")


# ============================================
# EXAMPLE 3: Complex Chain with Passthrough
# ============================================
print("=" * 60)
print("EXAMPLE 3: Using RunnablePassthrough in RAG-like pattern")
print("=" * 60)

# Simulate retrieving context (in real RAG, this would be from vector DB)
def retrieve_context(query):
    """Simulates document retrieval"""
    knowledge_base = {
        "python": "Python is a high-level programming language known for readability.",
        "langchain": "LangChain is a framework for building applications with LLMs.",
        "rag": "RAG (Retrieval Augmented Generation) combines retrieval with generation."
    }

    # Simple keyword matching
    for key, value in knowledge_base.items():
        if key in query.lower():
            return value
    return "No relevant context found."

# Create prompt template
template = """Answer the question based on the context below.

Context: {context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

# Build chain with RunnablePassthrough
rag_chain = (
    {
        "context": lambda x: retrieve_context(x["question"]),
        "question": RunnablePassthrough()  # Pass the question through
    }
    | prompt
    | model
    | StrOutputParser()
)

# Test the chain
question_input = {"question": "What is LangChain?"}
answer = rag_chain.invoke(question_input)

print(f"\nQuestion: {question_input['question']}")
print(f"Answer: {answer}\n")


# ============================================
# EXAMPLE 4: Multiple Passthrough Values
# ============================================
print("=" * 60)
print("EXAMPLE 4: Multiple values with RunnablePassthrough")
print("=" * 60)

# Prompt that needs multiple inputs
multi_template = """You are a {role} expert.

Task: {task}

Style: {style}

Provide your response:"""

multi_prompt = ChatPromptTemplate.from_template(multi_template)

# Chain that uses multiple passthrough values
multi_chain = (
    {
        "role": lambda x: x["role"],
        "task": lambda x: x["task"],
        "style": lambda x: x["style"]
    }
    | multi_prompt
    | model
    | StrOutputParser()
)

input_params = {
    "role": "Python programmer",
    "task": "Explain list comprehension",
    "style": "beginner-friendly"
}

response = multi_chain.invoke(input_params)

print(f"\nRole: {input_params['role']}")
print(f"Task: {input_params['task']}")
print(f"Style: {input_params['style']}")
print(f"\nResponse:\n{response}\n")


# ============================================
# PRODUCTION TIP
# ============================================
print("=" * 60)
print("PRODUCTION TIP: When to use RunnablePassthrough")
print("=" * 60)
print("""
✅ USE RunnablePassthrough when:
   - You need the same input in multiple places
   - Building RAG chains (pass question while retrieving context)
   - Adding metadata to pipeline without modifying original data
   - Creating reusable chain components

❌ DON'T use when:
   - Simple linear chains (unnecessary overhead)
   - Input needs transformation (use RunnableLambda instead)

💡 COMMON PATTERN:
   {
       "context": retriever,
       "question": RunnablePassthrough()
   }
   This passes the question unchanged while retrieving context
""")

print("\n✅ Day 10 - Program 1 Complete!")
print("Next: 10_02_runnable_lambda.py - Custom transformations\n")
