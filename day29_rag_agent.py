"""
RAG Agent - Retrieval-Augmented Generation with Document Search

Demonstrates AI agent that can search PDF documents using semantic search.
Agent converts documents to embeddings, stores in vector database, and retrieves
relevant information to answer questions.

Module: 2 Bonus - RAG Agent
Pattern: Document loading → Chunking → Embeddings → Vector store → Agent tool
Key Concept: Give AI access to search your documents (like a library card)
"""

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

load_dotenv()


# STEP 1: Load PDF Document
print("=" * 70)
print("STEP 1: LOADING PDF DOCUMENT")
print("=" * 70)

# Note: For this example, you'll need a PDF file. Using placeholder path.
# Replace with your actual PDF path or download a sample employee handbook
pdf_path = "resources/acmecorp-employee-handbook.pdf"

try:
    loader = PyPDFLoader(pdf_path)
    data = loader.load()
    print(f"✅ Loaded PDF: {len(data)} pages")
    print(f"📄 First page preview: {data[0].page_content[:200]}...")
except FileNotFoundError:
    print(f"⚠️  PDF not found at {pdf_path}")
    print("Creating sample document for demonstration...")
    # Create sample data for demonstration
    from langchain_core.documents import Document
    data = [
        Document(
            page_content="""ACME Corp Employee Handbook

            Vacation Policy:
            Employees receive 10 days of paid vacation in their first year.
            After completing 3 years of service, employees receive 15 days.
            After 5 years, employees receive 20 days of paid vacation annually.

            Sick Leave:
            All employees receive 5 days of paid sick leave per year.
            Unused sick days do not roll over to the next year.

            Remote Work Policy:
            Employees may work remotely up to 2 days per week with manager approval.
            Full-time remote work requires director-level approval.
            """,
            metadata={"source": "sample", "page": 0}
        )
    ]
    print(f"✅ Created sample document for demonstration")


# STEP 2: Split Document into Chunks
print("\n" + "=" * 70)
print("STEP 2: SPLITTING DOCUMENT INTO CHUNKS")
print("=" * 70)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,       # Each chunk = ~1000 characters
    chunk_overlap=200,     # Overlap to prevent cutting sentences
    add_start_index=True   # Track where chunk came from
)
all_splits = text_splitter.split_documents(data)

print(f"📚 Total chunks created: {len(all_splits)}")
print(f"📄 First chunk preview: {all_splits[0].page_content[:200]}...")


# STEP 3: Create Embeddings (Convert text to numbers)
print("\n" + "=" * 70)
print("STEP 3: CREATING EMBEDDINGS MODEL")
print("=" * 70)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
print("✅ Embeddings model initialized: text-embedding-3-large")
print("💡 Embeddings convert text into numbers that represent meaning")


# STEP 4: Create Vector Store (Database for embeddings)
print("\n" + "=" * 70)
print("STEP 4: CREATING VECTOR STORE")
print("=" * 70)

vector_store = InMemoryVectorStore(embeddings)
print("✅ Vector store created (InMemoryVectorStore)")
print("⚠️  Note: InMemoryVectorStore is RAM-based (lost on restart)")
print("📌 Production: Use ChromaDB, Pinecone, or Weaviate")


# STEP 5: Add Documents to Vector Store
print("\n" + "=" * 70)
print("STEP 5: INDEXING DOCUMENTS")
print("=" * 70)

print(f"⏳ Converting {len(all_splits)} chunks to embeddings and storing...")
ids = vector_store.add_documents(documents=all_splits)
print(f"✅ Indexed {len(ids)} document chunks")
print(f"🆔 Sample IDs: {ids[:3]}...")


# STEP 6: Test Semantic Search
print("\n" + "=" * 70)
print("STEP 6: TESTING SEMANTIC SEARCH")
print("=" * 70)

test_query = "How many days of vacation does an employee get in their first year?"
print(f"🔍 Query: {test_query}")

results = vector_store.similarity_search(test_query)
print(f"\n✅ Found {len(results)} relevant chunks")
print(f"📄 Most relevant chunk:\n{results[0].page_content}\n")


# STEP 7: Create RAG Tool (Wrap search as agent tool)
print("=" * 70)
print("STEP 7: CREATING RAG TOOL")
print("=" * 70)

@tool
def search_handbook(query: str) -> str:
    """Search the employee handbook for information using semantic search"""
    results = vector_store.similarity_search(query)
    return results[0].page_content

print("✅ Created search_handbook tool")
print("💡 AI agent can now search documents using this tool")


# STEP 8: Create Agent with RAG Tool
print("\n" + "=" * 70)
print("STEP 8: CREATING RAG AGENT")
print("=" * 70)

agent = create_agent(
    model="gpt-4o-mini",
    tools=[search_handbook],
    system_prompt="You are a helpful HR assistant that can search the employee handbook to answer questions."
)

print("✅ RAG Agent created")
print("🤖 Model: gpt-4o-mini")
print("🔧 Tools: search_handbook")


# STEP 9: Ask Questions to RAG Agent
print("\n" + "=" * 70)
print("STEP 9: TESTING RAG AGENT")
print("=" * 70)

questions = [
    "How many days of vacation does an employee get in their first year?",
    "What is the sick leave policy?",
    "Can employees work remotely?"
]

for i, question in enumerate(questions, 1):
    print(f"\n{'─' * 70}")
    print(f"Question {i}: {question}")
    print('─' * 70)

    response = agent.invoke({
        "messages": [HumanMessage(content=question)]
    })

    # Show the conversation flow
    print("\n📨 Conversation Flow:")
    for msg in response['messages']:
        msg_type = type(msg).__name__
        if hasattr(msg, 'content') and msg.content:
            print(f"  {msg_type}: {msg.content[:100]}...")
        elif hasattr(msg, 'tool_calls') and msg.tool_calls:
            print(f"  {msg_type}: Called tool '{msg.tool_calls[0]['name']}'")

    print(f"\n💬 Final Answer: {response['messages'][-1].content}")


# Summary
print("\n" + "=" * 70)
print("✅ RAG AGENT COMPLETE")
print("=" * 70)
print("\n💡 Key Learnings:")
print("   1. PDF → Text: Load documents with PyPDFLoader")
print("   2. Split: Chunk documents (1000 chars, 200 overlap)")
print("   3. Embeddings: Convert text to meaning-numbers")
print("   4. Vector Store: Index chunks for semantic search")
print("   5. RAG Tool: Wrap search as agent tool")
print("   6. Agent: AI decides when to search documents")
print("\n🎯 RAG = Give AI a library card to search YOUR documents!")
print("=" * 70)
