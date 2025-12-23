"""
Day 11: Production Hybrid RAG
- Query Expansion (Keywords + LLM)
- Hybrid Search (BM25 + Vector)
- Parallel Execution
"""

from common_config import get_model
from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from typing import List
import re

print("🔧 Setting up Production RAG...")

# ============================================
# LOAD DOCUMENTS
# ============================================
BASE_DIR = "/home/intruder/langchain_learning/examples"
files = {
    "txt1": f"{BASE_DIR}/langchain_1000_lines.txt",
    "txt2": f"{BASE_DIR}/langgraph_features.txt",
    "md": f"{BASE_DIR}/langgraph_quickstart.md",
    "pdf": f"{BASE_DIR}/langgraph_guide.pdf"
}

all_docs = (
    TextLoader(files["txt1"]).load() +
    TextLoader(files["txt2"]).load() +
    UnstructuredMarkdownLoader(files["md"]).load() +
    PyPDFLoader(files["pdf"]).load()
)

chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(all_docs)

# Create retrievers
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_documents(chunks, embeddings, persist_directory=f"{BASE_DIR}/chroma_day11")
semantic_retriever = vector_store.as_retriever(search_kwargs={"k": 10})
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 10

model = get_model(temperature=0)
print(f"✅ Ready! Loaded {len(chunks)} chunks from 4 files\n")


# ============================================
# PYDANTIC MODEL (Day 7: Structured Output)
# ============================================
class ExpandedQueries(BaseModel):
    """LLM generates multiple query versions"""
    queries: List[str] = Field(
        description="Exactly 4 high-quality search queries",
        min_length=4,
        max_length=4
    )
    reasoning: str = Field(description="Brief explanation of query strategy")


# ============================================
# PART 1: QUERY GENERATION
# ============================================
def extract_keywords(data: dict) -> List[str]:
    """Extract keywords without LLM (FREE) - only meaningful words"""
    question = data["question"]
    stop_words = {'what', 'is', 'how', 'why', 'the', 'a', 'an', 'does', 'do', 'can', 'are', 'waht', 'whats'}
    words = re.findall(r'\b\w+\b', question.lower())

    # Only keep words that are 4+ chars and not typos
    keywords = []
    for w in words:
        if w not in stop_words and len(w) >= 4:
            # Skip if looks like typo (no vowels)
            if any(vowel in w for vowel in 'aeiou'):
                keywords.append(w)

    return list(set(keywords))  # No uppercase duplicates


expansion_template = """You are a search query optimizer. Generate EXACTLY 4 high-quality search queries.

Original Question: {question}

Requirements:
1. Cover different aspects of the question
2. Use proper spelling and grammar
3. Include synonyms and related terms
4. Make queries specific and clear
5. Each query should be a complete, well-formed question or phrase

Example:
Question: "What is LangChain?"
Good queries:
1. "What is LangChain framework?"
2. "LangChain library explanation"
3. "How does LangChain work?"
4. "LangChain features and capabilities"

Now generate 4 queries for the user's question."""

expansion_prompt = ChatPromptTemplate.from_template(expansion_template)
llm_expander = expansion_prompt | model.with_structured_output(ExpandedQueries)

# RunnableParallel: Keywords + LLM at SAME TIME (Day 10)
parallel_expansion = RunnableParallel(
    keywords=RunnableLambda(extract_keywords),
    llm_expansion=llm_expander
)


# ============================================
# PART 2: COMBINE QUERIES
# ============================================
def combine_queries(data: dict) -> dict:
    """Merge keywords + LLM queries, keep only quality ones"""
    keywords = data["expansion"]["keywords"]
    llm_queries = data["expansion"]["llm_expansion"].queries

    # Start with LLM queries (higher quality)
    all_queries = llm_queries.copy()

    # Add keywords only if they're meaningful (4+ chars)
    for kw in keywords:
        if len(kw) >= 4 and kw.lower() not in [q.lower() for q in all_queries]:
            all_queries.append(kw)

    # Return queries + pass through original question
    return {
        "queries": all_queries[:5],
        "question": data["question"]
    }

query_combiner = RunnableLambda(combine_queries)


# ============================================
# PART 3: HYBRID SEARCH (BM25 + Vector)
# ============================================
def hybrid_search_one_query(query: str) -> List:
    """Search with BOTH keyword and semantic"""
    bm25_results = bm25_retriever.invoke(query)
    vector_results = semantic_retriever.invoke(query)

    # Deduplicate
    seen = set()
    unique = []
    for chunk in bm25_results + vector_results:
        h = hash(chunk.page_content[:100])
        if h not in seen:
            seen.add(h)
            unique.append(chunk)
    return unique


# ============================================
# PART 4: PARALLEL MULTI-QUERY SEARCH
# ============================================
def safe_search(data: dict, index: int) -> List:
    """Search query at index"""
    queries = data["queries"]
    return hybrid_search_one_query(queries[index]) if index < len(queries) else []

# RunnableParallel: Search ALL queries at SAME TIME (Day 10)
def create_search_results(data: dict) -> dict:
    """Search all queries in parallel and pass through question"""
    queries = data["queries"]

    # Search results
    results = {
        "q1": safe_search(data, 0),
        "q2": safe_search(data, 1),
        "q3": safe_search(data, 2),
        "q4": safe_search(data, 3),
        "q5": safe_search(data, 4)
    }

    # Pass through question
    return {
        "search_results": results,
        "question": data["question"]
    }

parallel_search = RunnableLambda(create_search_results)


# ============================================
# PART 5: DEDUPLICATION
# ============================================
def deduplicate_all(data: dict) -> dict:
    """Remove duplicates across all results"""
    results_dict = data["search_results"]

    seen = set()
    unique = []
    for query_results in results_dict.values():
        for chunk in query_results:
            h = hash(chunk.page_content[:100])
            if h not in seen:
                seen.add(h)
                unique.append(chunk)

    # Pass through question
    return {
        "chunks": unique,
        "question": data["question"]
    }

deduplicator = RunnableLambda(deduplicate_all)


# ============================================
# PART 6: RE-RANKING & ANSWER GENERATION
# ============================================
def rerank_chunks(data: dict) -> List:
    """Re-rank chunks by relevance - prioritize actual content over metadata"""
    chunks = data["chunks"]
    question = data["question"]

    scored_chunks = []
    question_words = set(re.findall(r'\b\w{4,}\b', question.lower()))  # Only 4+ char words

    for chunk in chunks:
        content = chunk.page_content.lower()

        # Penalize metadata/TODO chunks
        is_metadata = any(marker in content[:100] for marker in ['**day ', '- [ ]', 'todo', '###', '##'])

        if is_metadata:
            score = -1000  # Very low score
        else:
            # Score by keyword overlap + content quality
            chunk_words = set(re.findall(r'\b\w{4,}\b', content))
            overlap = len(question_words & chunk_words)

            # Bonus for longer meaningful content
            content_length_bonus = min(len(content) // 100, 5)

            score = overlap + content_length_bonus

        scored_chunks.append((score, chunk))

    # Sort by score (highest first)
    scored_chunks.sort(key=lambda x: x[0], reverse=True)

    # Return top chunks without scores
    return [chunk for score, chunk in scored_chunks]


def prepare_context(chunks: List) -> dict:
    """Take top 5 BEST chunks after re-ranking"""
    context = "\n\n".join([c.page_content for c in chunks[:5]])
    return {"context": context}

answer_template = """Answer based ONLY on context. If unsure, say "I don't know."

Context:
{context}

Question: {question}

Answer:"""

answer_prompt = ChatPromptTemplate.from_template(answer_template)
answer_chain = answer_prompt | model | StrOutputParser()


# ============================================
# FULL PIPELINE (LCEL - Day 3 + Day 10)
# ============================================
# Using RunnablePassthrough to keep question throughout pipeline!

full_pipeline = (
    # Input: {"question": "What is LangChain?"}

    # Step 1: Expand query (keywords + LLM in parallel)
    RunnablePassthrough.assign(
        expansion=parallel_expansion
    )
    # Output: {"question": "...", "expansion": {...}}

    # Step 2: Combine queries
    | query_combiner
    # Output: {"queries": [...], "question": "..."}

    # Step 3: Search all queries (parallel)
    | parallel_search
    # Output: {"search_results": {...}, "question": "..."}

    # Step 4: Deduplicate
    | deduplicator
    # Output: {"chunks": [...], "question": "..."}

    # Step 5: Re-rank by relevance
    | RunnableLambda(rerank_chunks)
    # Output: [reranked chunks]

    # Step 6: Prepare context
    | RunnableLambda(prepare_context)
    # Output: {"context": "..."}
)


# ============================================
# INTERACTIVE LOOP
# ============================================
print("=" * 70)
print("PRODUCTION HYBRID RAG - INTERACTIVE MODE")
print("=" * 70)
print("\nType 'exit' to quit\n")

while True:
    question = input("❓ Your question: ").strip()

    if question.lower() == 'exit':
        print("\n👋 Goodbye!")
        break

    if not question:
        continue

    print(f"\n🔍 Step 1: Query expansion...")
    step1 = RunnablePassthrough.assign(expansion=parallel_expansion).invoke({"question": question})
    print(f"   Keywords: {step1['expansion']['keywords']}")
    print(f"   LLM queries: {step1['expansion']['llm_expansion'].queries}")

    print(f"\n🔍 Step 2: Combining...")
    step2 = query_combiner.invoke(step1)
    print(f"   Final queries: {step2['queries']}")

    print(f"\n🔍 Step 3: Hybrid search...")
    step3 = parallel_search.invoke(step2)
    total = sum(len(v) for v in step3['search_results'].values())
    print(f"   Total chunks: {total}")

    print(f"\n🔍 Step 4: Deduplicating...")
    step4 = deduplicator.invoke(step3)
    print(f"   Unique chunks: {len(step4['chunks'])}")

    print(f"\n🔍 Step 5: Re-ranking...")
    step5 = rerank_chunks(step4)
    print(f"   Top 5 chunks selected")

    print(f"\n🔍 Step 6: Preparing context...")
    context_result = prepare_context(step5)
    print(f"   Context size: {len(context_result['context'])} chars")
    print(f"   First 200 chars: {context_result['context'][:200]}...")

    print(f"\n🔍 Step 7: Generating answer...")
    # Generate answer
    answer = answer_chain.invoke({
        "context": context_result["context"],
        "question": question
    })

    print(f"\n✅ ANSWER:")
    print("=" * 70)
    print(answer)
    print("=" * 70 + "\n")
