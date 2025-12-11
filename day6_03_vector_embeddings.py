from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
from chromadb.config import Settings

print(" Imports loaded \n Langhcain Components ready! \n Chromadb ready \n")



try:
	filename = input(" \n Enter the filename : ").strip()
	loader = TextLoader(filename)
	docs = loader.load()

	print("\n file loaded successfully")

	char_count = len(docs[0].page_content)
	word_count = len(docs[0].page_content.split())

	print(f" \n length of the file : {char_count}")
	print(f"\n Total words in the file : {word_count}")
	print(f" \n Preview : {docs[0].page_content[:100]}.......")

except (FileNotFoundError, RuntimeError) :
	print(f"Error loading {filename}:")
	print(" Check the filename and path")
	exit()


print("\n Splitting up the file into chunks")
text_splitter = RecursiveCharacterTextSplitter( chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)


print("=" * 60)
print("STEP 3: Initializing embedding model...")
print("=" * 60)

# Use Nomic Embed (local, free, 768 dimensions)
embeddings = OllamaEmbeddings(
      model="nomic-embed-text",
      base_url="http://localhost:11434"
  )

print("✅ Embedding model: nomic-embed-text")
print("   - Dimensions: 768")
print("   - Context length: 8192 tokens")
print("   - Runs locally (free!)")
print()

# Test embedding
test_text = "How does RAG work?"
test_embedding = embeddings.embed_query(test_text)
print(f"🧪 Test embedding:")
print(f"   Text: '{test_text}'")
print(f"   Vector length: {len(test_embedding)} dimensions")
print(f"   First 5 values: {test_embedding[:5]}")
print()

print("=" * 60)
print("STEP 4: Creating ChromaDB vector store...")
print("=" * 60)

# Create persistent client (saves to disk)
client = chromadb.PersistentClient(path="./chroma_db")

# Create or get collection
collection = client.get_or_create_collection(
    name="langchain_docs",
    metadata={"description": "LangChain documentation chunks"}
)

print(f"✅ ChromaDB client created")
print(f"   Storage path: ./chroma_db")
print(f"   Collection: langchain_docs")
print()

print("=" * 60)
print("STEP 5: Embedding and storing all chunks...")
print("=" * 60)

# Prepare data for ChromaDB
chunk_ids = []
chunk_texts = []
chunk_metadatas = []

for i, chunk in enumerate(chunks):
    chunk_ids.append(f"chunk_{i}")
    chunk_texts.append(chunk.page_content)
    chunk_metadatas.append({
        "source": filename,
        "chunk_index": i,
        "chunk_size": len(chunk.page_content)
    })

print(f"📦 Preparing {len(chunks)} chunks for embedding...")

# Embed all chunks at once (batch operation)
print(f"🔄 Embedding chunks... (this may take a moment)")
chunk_embeddings = embeddings.embed_documents(chunk_texts)

print(f"✅ Generated {len(chunk_embeddings)} embeddings")
print(f"   Each embedding: {len(chunk_embeddings[0])} dimensions")
print()

# Store in ChromaDB
print(f"💾 Storing in ChromaDB...")
collection.add(
    ids=chunk_ids,
    documents=chunk_texts,
    embeddings=chunk_embeddings,
    metadatas=chunk_metadatas
)

print(f"✅ Stored {len(chunk_ids)} chunks in vector database!")
print(f"   HNSW index built automatically for fast search")
print()

print("=" * 60)
print("STEP 6: Testing semantic search...")
print("=" * 60)

# Test query
test_query = "What is RAG?"
print(f"🔍 Test query: '{test_query}'")
print()

# Embed the query with OUR model (nomic-embed-text, 768 dim)
print(f"🔄 Embedding query with nomic-embed-text...")
query_embedding = embeddings.embed_query(test_query)
print(f"✅ Query embedded: {len(query_embedding)} dimensions")
print()

# Search for similar chunks using our embedding
results = collection.query(
    query_embeddings=[query_embedding],  # Use our 768-dim embedding!
    n_results=3
)

print(f"📊 Top 3 most relevant chunks:")
print()

for i in range(3):
    chunk_id = results['ids'][0][i]
    chunk_text = results['documents'][0][i]
    metadata = results['metadatas'][0][i]
    distance = results['distances'][0][i]

    print(f"Rank {i+1}:")
    print(f"  ID: {chunk_id}")
    print(f"  Source: {metadata['source']}")
    print(f"  Chunk Index: {metadata['chunk_index']}")
    print(f"  Similarity Score: {1 - distance:.3f} (closer to 1 = more similar)")
    print(f"  Preview: {chunk_text[:150]}...")
    print()


print("=" * 60)
print(" Building RAG and memory Chatbot")
print("=" * 60)

#initialise the chat model 

model = ChatOllama(model="qwen3:4b", temperature=0.7)

#conversation memory

conversation_history=[]

print("✅ RAG chatbot ready!")
print("   - Semantic search with nomic-embed-text")
print("   - Conversation memory enabled")
print("   - ChromaDB persistent storage (./chroma_db)")
print("   - Chat model: qwen3:4b")
print()
print("Type 'exit' to quit")
print("=" * 60)
print()

while True:

	question = input("You : ").strip()
	if question.lower()=='exit':
		print("\n Goodbye")
		print(f" Total messages in memory {len(conversation_history)}")
		print(f"vector databse saves in ./chromadb")
		break

	if not question:
		continue

	print(f" Searching {len(chunks)} chunks with vector similarity...")

	# Embed the question with OUR model (nomic-embed-text, 768 dim)
	question_embedding = embeddings.embed_query(question)

	search_results = collection.query(query_embeddings=[question_embedding], n_results=3)

	#extract relevant chunks
	relevant_chunks = search_results['documents'][0]
	relevant_metadata = search_results['metadatas'][0]
	distances = search_results['distances'][0]

	# Show which chunks were selected
	chunk_numbers = [meta['chunk_index'] for meta in relevant_metadata]
	print(f"   Found top 3 chunks: {chunk_numbers}")

	# Show similarity scores
	print(f"\n📊 Similarity scores:")
	for i, (meta, dist) in enumerate(zip(relevant_metadata, distances)):
		similarity = 1 - dist
		print(f"   Chunk #{meta['chunk_index']}: {similarity:.3f}")

	# Build context from relevant chunks
	context = "\n\n".join([
		f"[Chunk {meta['chunk_index']}]: {chunk}"
		for chunk, meta in zip(relevant_chunks, relevant_metadata)
	])

	total_context_chars = len(context)
	print(f"   Total context: {total_context_chars} chars")
	print()

	# STEP 2: Build messages with context
	# System message with context (recreated each time with new chunks)
	messages = [
          SystemMessage(content=f"""Answer ONLY using the following context.
    		Do not use your own knowledge. If the answer is not in the context, say 
  		'I don't know'.

  		Context:
  		{context}""")
      		]
	# Add previous conversation history
	messages.extend(conversation_history)
	# Add current question
	messages.append(HumanMessage(content=question))

	# STEP 3: Get AI response
	response = model.invoke(messages)

	# STEP 4: Save to conversation history
	conversation_history.append(HumanMessage(content=question))
	conversation_history.append(response)

	# Display response
	print(f"AI: {response.content}\n")
	print(f"📚 [Used {len(relevant_chunks)} chunks from semantic search]")
	print("-" * 60)
	print()



















































