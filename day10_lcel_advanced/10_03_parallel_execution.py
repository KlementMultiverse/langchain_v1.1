"""
Day 10 - LCEL Advanced: RunnableParallel
=========================================

CONCEPT: RunnableParallel runs multiple tasks at the SAME TIME (concurrently)

WHY IT MATTERS: Speed! Instead of waiting for each task to finish, run them all at once.

EXAMPLE:
- Sequential: Task A (2s) → Task B (2s) → Task C (2s) = 6 seconds total
- Parallel:   Task A, B, C all run together = 2 seconds total (3x faster!)

USE CASE: Generate multiple outputs from same input (sentiment + summary + keywords)

PRODUCTION PATTERN: Multi-task AI analysis, batch processing
"""

from langchain_core.runnables import RunnableParallel, RunnableLambda
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
import time

# Initialize model
model = ChatOllama(model="qwen3:4b", temperature=0.7)


# ============================================
# EXAMPLE 1: Basic Parallel Execution
# ============================================
print("=" * 60)
print("EXAMPLE 1: Run multiple analyses in parallel")
print("=" * 60)

# Define three different analysis tasks
def analyze_sentiment(text):
    """Analyze sentiment"""
    prompt = ChatPromptTemplate.from_template("What is the sentiment of this text (positive/negative/neutral)? Text: {text}")
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"text": text})

def extract_summary(text):
    """Extract one-sentence summary"""
    prompt = ChatPromptTemplate.from_template("Summarize this in ONE sentence: {text}")
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"text": text})

def extract_keywords(text):
    """Extract keywords"""
    prompt = ChatPromptTemplate.from_template("Extract 3 keywords from this text: {text}")
    chain = prompt | model | StrOutputParser()
    return chain.invoke({"text": text})

# Create parallel chain
parallel_chain = RunnableParallel(
    sentiment=RunnableLambda(analyze_sentiment),
    summary=RunnableLambda(extract_summary),
    keywords=RunnableLambda(extract_keywords)
)

# Test text
text = "LangChain is an amazing framework that makes building AI applications incredibly easy and fun!"

print("Analyzing text in parallel...\n")
start_time = time.time()

result = parallel_chain.invoke(text)

elapsed = time.time() - start_time

print(f"Input: {text}\n")
print(f"Results:")
print(f"  Sentiment: {result['sentiment']}")
print(f"  Summary: {result['summary']}")
print(f"  Keywords: {result['keywords']}")
print(f"\nTime taken: {elapsed:.2f} seconds")
print("(All 3 analyses ran at the SAME TIME!)\n")


# ============================================
# EXAMPLE 2: Parallel with Different Input Processing
# ============================================
print("=" * 60)
print("EXAMPLE 2: Parallel processing with transformations")
print("=" * 60)

def count_words(text):
    """Count words"""
    return len(text.split())

def count_chars(text):
    """Count characters"""
    return len(text)

def get_first_word(text):
    """Get first word"""
    return text.split()[0] if text.split() else ""

# Parallel chain with simple functions
stats_chain = RunnableParallel(
    word_count=RunnableLambda(count_words),
    char_count=RunnableLambda(count_chars),
    first_word=RunnableLambda(get_first_word)
)

test_text = "Hello world from LangChain"
stats = stats_chain.invoke(test_text)

print(f"Text: {test_text}")
print(f"Results: {stats}\n")


# ============================================
# EXAMPLE 3: Parallel + Sequential (Real RAG Pattern)
# ============================================
print("=" * 60)
print("EXAMPLE 3: Parallel retrieval + Sequential processing")
print("=" * 60)

def retrieve_from_docs(query):
    """Simulates document retrieval"""
    docs = {
        "langchain": "LangChain is a framework for building LLM applications.",
        "python": "Python is a programming language.",
        "rag": "RAG combines retrieval with generation."
    }
    for key, value in docs.items():
        if key in query.lower():
            return value
    return "No context found."

def retrieve_from_web(query):
    """Simulates web search"""
    return f"Web results for: {query}"

def get_user_history(query):
    """Simulates user history lookup"""
    return "User has asked about AI frameworks before."

# Parallel retrieval from multiple sources
parallel_retrieval = RunnableParallel(
    doc_context=RunnableLambda(retrieve_from_docs),
    web_context=RunnableLambda(retrieve_from_web),
    user_history=RunnableLambda(get_user_history)
)

# Then sequential: combine contexts → prompt → model
def combine_contexts(data):
    """Combine all retrieved data"""
    combined = f"""
Document: {data['doc_context']}
Web: {data['web_context']}
History: {data['user_history']}
"""
    return combined

template = """Based on these sources:
{context}

Answer this question: {question}"""

prompt = ChatPromptTemplate.from_template(template)

# Full chain: parallel retrieval → combine → answer
rag_chain = (
    {
        "context": parallel_retrieval | RunnableLambda(combine_contexts),
        "question": RunnableLambda(lambda x: x)
    }
    | prompt
    | model
    | StrOutputParser()
)

question = "What is LangChain?"
print(f"Question: {question}\n")
print("Retrieving from multiple sources in parallel...")

answer = rag_chain.invoke(question)
print(f"\nAnswer: {answer}\n")


# ============================================
# EXAMPLE 4: Parallel with Dictionary Output
# ============================================
print("=" * 60)
print("EXAMPLE 4: Using dictionary syntax (shorthand)")
print("=" * 60)

# You can also use dictionary syntax (same as RunnableParallel)
parallel_dict = {
    "uppercase": RunnableLambda(lambda x: x.upper()),
    "lowercase": RunnableLambda(lambda x: x.lower()),
    "length": RunnableLambda(lambda x: len(x)),
    "reversed": RunnableLambda(lambda x: x[::-1])
}

text = "Hello"
result = RunnableParallel(**parallel_dict).invoke(text)

print(f"Input: {text}")
print(f"Results: {result}\n")


# ============================================
# PRODUCTION TIPS
# ============================================
print("=" * 60)
print("PRODUCTION TIPS: When to use RunnableParallel")
print("=" * 60)
print("""
✅ USE RunnableParallel when:
   - Multiple INDEPENDENT tasks (no dependencies)
   - Tasks can run at the SAME TIME
   - Want to speed up processing
   - Multi-source retrieval (docs + web + DB)
   - Generate multiple outputs (sentiment + summary + keywords)

❌ DON'T use when:
   - Tasks depend on each other (use sequential |)
   - Tasks must run in specific order
   - One task needs output from another

SPEED COMPARISON:
Sequential: Task1 (2s) → Task2 (2s) → Task3 (2s) = 6 seconds
Parallel:   Task1, Task2, Task3 (all at once) = 2 seconds

REAL EXAMPLE - Multi-source RAG:
RunnableParallel(
    docs=search_documents,      # Search vector DB
    web=search_web,             # Search internet
    sql=query_database          # Query SQL DB
)
All 3 searches happen at SAME TIME! Then combine results.

SYNTAX OPTIONS:
1. RunnableParallel(key1=task1, key2=task2)
2. {"key1": task1, "key2": task2}  (shorthand, same thing!)
""")

print("\n✅ Day 10 - Program 3 Complete!")
print("Next: 10_04_branching_logic.py - If/else conditional routing\n")
