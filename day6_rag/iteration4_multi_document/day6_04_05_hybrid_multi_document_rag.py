"""
Day 6 Hybrid Multi-Document RAG
- Multi-format loading (TXT, MD, PDF)
- Hybrid retrieval (semantic + BM25)
- Source attribution
"""

from langchain_community.document_loaders import TextLoader, UnstructuredMarkdownLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
import os


print("Hybrid Retreival Multi-Document RAG")
print("=" * 60)

# File Paths
BASE_DIR = "/home/intruder/langgraph_learning/examples"
files = {
	"txt1": f"{BASE_DIR}/langchain_1000_lines.txt",
	"txt2": f"{BASE_DIR}/langgraph_features.txt",
	"md": f"{BASE_DIR}/langgraph_quickstart.md",
	"pdf": f"{BASE_DIR}/langgraph_guide.pdf"
   }

# Load documents

print("Loading documents...")
txt1_loader = TextLoader(files["txt1"])
txt2_loader = TextLoader(files["txt2"])
md_loader = UnstructuredMarkdownLoader(files["md"])
pdf_loader = PyPDFLoader(files["pdf"])

docs_txt1 = txt1_loader.load()
docs_txt2 = txt2_loader.load()
docs_md = md_loader.load()
docs_pdf = pdf_loader.load()

# Combine all documents
all_docs = docs_txt1 + docs_txt2 + docs_md + docs_pdf
print(f"✅ Loaded {len(all_docs)} documents from 4 sources:")
print(f"   - {os.path.basename(files['txt1'])} ({len(docs_txt1)} doc)")
print(f"   - {os.path.basename(files['txt2'])} ({len(docs_txt2)} doc)")
print(f"   - {os.path.basename(files['md'])} ({len(docs_md)} doc)")
print(f"   - {os.path.basename(files['pdf'])} ({len(docs_pdf)} pages)")

 
# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter( 
	chunk_size=500,
	chunk_overlap=50
   )

chunks = text_splitter.split_documents(all_docs)

# Add chunk ID's
for idx, chunk in enumerate(chunks):
	chunk.metadata["chunk_id"] = idx

print(f" Created {len(chunks)} chunks with metadata")

# Create semantic retriever
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_documents( documents=chunks, embedding=embeddings, persist_directory="./chroma_hybrid_db")

semantic_retriever = vector_store.as_retriever( search_kwargs={"k": 20})


print("Semantic search Ready")

# Create BM25 keyword retriever

print("\n Creating BM25  Retriever")
bm25_retriever = BM25Retriever.from_documents(chunks)
bm25_retriever.k = 20

print("Keyword search Ready \n")

print("Creating hybrid search (manual merge)")

def hybrid_search(query, k=5):
	"""Combine semantic and keyword search results"""
	# Get results from both retrievers
	semantic_results = semantic_retriever.invoke(query)
	bm25_results = bm25_retriever.invoke(query)

	# Combine and deduplicate by content
	seen = set()
	combined = []

	for doc in semantic_results + bm25_results:
		content_hash = hash(doc.page_content[:100])
		if content_hash not in seen:
			seen.add(content_hash)
			combined.append(doc)

	return combined[:k]

print(" Hybrid search ready - (semantic + keyword)")

# Initialize the chat model

model = ChatOllama(model="qwen3:4b")

conversation_history = []

# Interactive Q&A loop
print("\n" + "="*70)
print("💬 HYBRID RAG CHATBOT READY!")
print("Ask questions about LangChain/LangGraph (or 'quit' to exit)")
print("="*70)

while True:
	query = input("\n You: ").strip()
	if query.lower() in ['quit','exit','q']:
		print("\n Good Bye")
		break

	if not query:
		continue

	# Retrive relevant chunks with hybrid search
	print("\n🔍 Searching (hybrid: semantic + keyword)...")
	results = hybrid_search(query, k=5)

	# show retrived chunks with metadata
	print(f"\n📄 Found {len(results)} relevant chunks:\n")


	for i, doc in enumerate(results[:3], 1):
		print(f"   [{i}] Source: {os.path.basename(doc.metadata['source'])}")
		if 'page' in doc.metadata:
			print(f"       Page: {doc.metadata['page'] + 1}")
		if 'chunk_id' in doc.metadata:
			print(f"       Chunk ID: {doc.metadata['chunk_id']}")
		print(f"       Preview: {doc.page_content[:120]}...")
		print()

	# Build context from top 3 chunks
	context = "\n\n".join([doc.page_content for doc in results[:3]])

	# Create messages
	system_msg = SystemMessage(content=f"""Answer based on this context. If not in context, say so.

Context:
{context}""")

	conversation_history.append(HumanMessage(content=query))

	# Get AI response
	response = model.invoke([system_msg] + conversation_history)
	conversation_history.append(response)

	print(f"🤖 AI: {response.content}\n")



























































 
