# Day 6 - Iteration 3: Vector Embeddings + ChromaDB

> **"Keyword search finds words. Semantic search understands meaning."**

---

## 🎯 What You'll Learn

- ✅ **What embeddings are** - Text → numbers (vectors)
- ✅ **nomic-embed-text** - Local 768-dimensional embedding model
- ✅ **ChromaDB** - Vector database with persistent storage
- ✅ **Semantic search** - Find chunks by meaning, not keywords
- ✅ **HNSW index** - Fast similarity search algorithm
- ✅ **Production RAG** - The approach used in real systems

**Time needed**: 45-60 minutes (includes understanding embeddings)

---

## 📋 What You Already Have

From Iterations 1-2:
- ✅ Document loading
- ✅ Text splitting
- ✅ RAG + Memory pattern

---

## 🆕 What's New

**New package**: `chromadb`

```bash
pip install chromadb
```

**New concepts**:
- Vector embeddings
- Semantic similarity
- Vector databases
- Persistent storage

---

## 📖 Understanding Embeddings

### **What Are Embeddings?**

**Simple**: Converting text to numbers so computers can understand meaning.

**Technical**: Text → 768-dimensional vector (list of 768 numbers)

### **Example**:

```python
Text: "What is RAG?"
Embedding: [0.234, -0.567, 0.123, ..., 0.891]  # 768 numbers
```

### **Why It Works**:

**Similar meanings** → **Similar vectors**

```
"What is RAG?" → [0.234, -0.567, ...]
"Explain RAG" → [0.241, -0.562, ...]  # Close to above!
"Pizza recipe" → [-0.891, 0.234, ...] # Far from above!
```

**Math**: Calculate distance between vectors
- Small distance = similar meaning
- Large distance = different meaning

---

## 🔧 The Embedding Pipeline

```
Text → Tokenization → Token Embeddings → Mean Pooling → Final Vector (768-dim)
```

**1. Tokenization**: "What is RAG?" → ["What", "is", "RAG", "?"]

**2. Token Embeddings**: Each token → vector

**3. Mean Pooling**: Average all token vectors

**4. Final Vector**: One 768-dimensional vector for the entire text

---

## 💾 ChromaDB Structure

**Each stored item has**:

```python
{
    "id": "chunk_0",                          # Unique identifier
    "document": "RAG stands for...",          # The chunk text
    "embedding": [0.234, -0.567, ...],        # 768-dim vector
    "metadata": {                             # Extra info
        "source": "langchain_1000_lines.txt",
        "chunk_index": 0,
        "chunk_size": 439
    }
}
```

---

## 🔍 How Semantic Search Works

**Traditional keyword search (Iteration 2)**:
```
Query: "What is RAG?"
Search: Find chunks containing "what", "is", or "rag"
Problem: Finds "storage", "fragmentation", etc.
```

**Semantic search (Iteration 3)**:
```
Query: "What is RAG?"
1. Embed query → [0.234, -0.567, ...]
2. Compare with all chunk embeddings
3. Find closest matches (smallest distances)
4. Return top 3 chunks

Result: Finds chunks about "Retrieval-Augmented Generation"
Even if exact words differ!
```

---

## 🚀 How to Run

### **Step 1: Install ChromaDB**
```bash
cd day6_rag/iteration3_vector_embeddings
source ../../venv/bin/activate
pip install chromadb
```

### **Step 2: Delete Old Database (if exists)**
```bash
rm -rf chroma_db
```

### **Step 3: Copy Test File**
```bash
cp ../test_data/langchain_1000_lines.txt .
```

### **Step 4: Verify Ollama + nomic-embed-text**
```bash
# Check Ollama running
curl http://localhost:11434

# Check nomic-embed-text is available
ollama list | grep nomic

# If not available, download (3GB)
ollama pull nomic-embed-text
```

### **Step 5: Run Program**
```bash
python day6_03_vector_embeddings.py
```

**When prompted**:
```
Enter the filename : langchain_1000_lines.txt
```

**First run takes 30-60 seconds** (embedding 297 chunks)
**Subsequent queries are instant!**

---

## 📊 Expected Output

```
 Imports loaded
 Langchain Components ready!
 Chromadb ready

 Enter the filename : langchain_1000_lines.txt

 file loaded successfully
 length of the file : 105632
 Total words in the file : 11589

 Splitting up the file into chunks

============================================================
STEP 3: Initializing embedding model...
============================================================
✅ Embedding model: nomic-embed-text
   - Dimensions: 768
   - Context length: 8192 tokens
   - Runs locally (free!)

🧪 Test embedding:
   Text: 'How does RAG work?'
   Vector length: 768 dimensions
   First 5 values: [0.234, -0.567, 0.123, -0.891, 0.456]

============================================================
STEP 4: Creating ChromaDB vector store...
============================================================
✅ ChromaDB client created
   Storage path: ./chroma_db
   Collection: langchain_docs

============================================================
STEP 5: Embedding and storing all chunks...
============================================================
📦 Preparing 297 chunks for embedding...
🔄 Embedding chunks... (this may take a moment)
✅ Generated 297 embeddings
   Each embedding: 768 dimensions

💾 Storing in ChromaDB...
✅ Stored 297 chunks in vector database!
   HNSW index built automatically for fast search

============================================================
STEP 6: Testing semantic search...
============================================================
🔍 Test query: 'What is RAG?'
🔄 Embedding query with nomic-embed-text...
✅ Query embedded: 768 dimensions

📊 Top 3 most relevant chunks:

Rank 1:
  ID: chunk_12
  Source: langchain_1000_lines.txt
  Chunk Index: 12
  Similarity Score: 0.876 (closer to 1 = more similar)
  Preview: RAG stands for Retrieval-Augmented Generation...

[Ranks 2 and 3...]

============================================================
 Building RAG and memory Chatbot
============================================================
✅ RAG chatbot ready!
   - Semantic search with nomic-embed-text
   - Conversation memory enabled
   - ChromaDB persistent storage (./chroma_db)
   - Chat model: qwen3:4b

Type 'exit' to quit
============================================================

You : What is RAG?

 Searching 297 chunks with vector similarity...
   Found top 3 chunks: [12, 45, 78]

📊 Similarity scores:
   Chunk #12: 0.876
   Chunk #45: 0.823
   Chunk #78: 0.801
   Total context: 1425 chars

AI: RAG stands for Retrieval-Augmented Generation...

📚 [Used 3 chunks from semantic search]
------------------------------------------------------------
```

---

## 💡 Key Improvements

| Aspect | Iteration 2 (Keyword) | Iteration 3 (Semantic) |
|--------|----------------------|------------------------|
| **Search method** | Keyword matching | Vector similarity |
| **Understands meaning** | ❌ No | ✅ Yes |
| **False positives** | Many | Very few |
| **Storage** | None | ChromaDB (persistent) |
| **Speed (first run)** | Instant | 30-60s (embedding) |
| **Speed (after)** | Instant | Instant |
| **Production ready** | No | Yes |

---

## 🔧 Key Code Sections

### **1. Embedding Model Setup**
```python
from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)
```

### **2. ChromaDB Client**
```python
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")
collection = client.get_or_create_collection(name="langchain_docs")
```

### **3. Embedding & Storing**
```python
# Embed all chunks
chunk_embeddings = embeddings.embed_documents(chunk_texts)

# Store in ChromaDB
collection.add(
    ids=chunk_ids,
    documents=chunk_texts,
    embeddings=chunk_embeddings,
    metadatas=chunk_metadatas
)
```

### **4. Semantic Search**
```python
# Embed query
question_embedding = embeddings.embed_query(question)

# Search for similar chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3
)
```

---

## ⚠️ Important: Embedding Consistency

**CRITICAL RULE**: Query embeddings MUST match stored embeddings!

**✅ Correct**:
```python
# Store with nomic-embed-text (768-dim)
chunk_embeddings = embeddings.embed_documents(texts)

# Query with nomic-embed-text (768-dim)
query_embedding = embeddings.embed_query(question)
```

**❌ Wrong** (dimension mismatch error):
```python
# Store with nomic-embed-text (768-dim)
chunk_embeddings = embeddings.embed_documents(texts)

# Query with ChromaDB's default (384-dim)
results = collection.query(query_texts=[question])  # ERROR!
```

**If you get "dimension mismatch" error**:
1. Delete `chroma_db` folder
2. Run program again

---

## 🎯 Practice Exercises

### **Exercise 1: Test Semantic Understanding**

Ask questions using DIFFERENT words than in the document:

```
Document says: "RAG combines retrieval with generation"
Ask: "How does RAG work?" (different words!)

Semantic search will still find it! ✅
```

### **Exercise 2: Adjust Similarity Threshold**

```python
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=5  # Get top 5 instead of 3
)

# Filter by similarity score
filtered = [
    (chunk, meta, dist)
    for chunk, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0])
    if (1 - dist) > 0.7  # Only chunks with >70% similarity
]
```

### **Exercise 3: Metadata Filtering**

```python
# Only search specific chunks
results = collection.query(
    query_embeddings=[question_embedding],
    n_results=3,
    where={"chunk_index": {"$lt": 50}}  # Only first 50 chunks
)
```

---

## 🔍 Common Issues

### **Issue: "dimension mismatch 768 vs 384"**

**Cause**: Using `query_texts` instead of `query_embeddings`

**Solution**: Always embed queries yourself:
```python
question_embedding = embeddings.embed_query(question)
results = collection.query(query_embeddings=[question_embedding])
```

### **Issue: First run is slow**

**Expected!** Embedding 297 chunks takes 30-60 seconds.

**After that**: Embeddings are saved in `./chroma_db`, instant!

### **Issue: ChromaDB persists old data**

**Solution**: Delete and recreate:
```bash
rm -rf chroma_db
python day6_03_vector_embeddings.py
```

---

## 📚 What You Learned

✅ **Vector embeddings** - Text → meaningful numbers
✅ **Semantic similarity** - Understanding meaning, not keywords
✅ **ChromaDB** - Vector database with persistence
✅ **HNSW index** - Fast approximate nearest neighbor search
✅ **Production RAG** - The approach used in real systems
✅ **Embedding consistency** - Query and store must match

---

## 🎓 This is Production-Ready RAG!

**What you built** is used by:
- ChatGPT plugins (document Q&A)
- Customer support bots
- Internal knowledge bases
- Legal document analysis
- Medical record search
- Research paper discovery

**You now understand** the core technology behind modern RAG systems!

---

## ⏭️ What's Next?

**Iteration 4**: Multi-document RAG (coming soon)
- Load PDF, TXT, MD files
- Multiple documents in one system
- Source citations

**Iteration 5**: Hybrid search (coming soon)
- Combine semantic + keyword search
- Best of both worlds

**For now**: You've mastered the foundation! 🎉

---

**"Collaborative Learning - The Next Genesis Learning"**

*From keywords to vectors. From simple to production.* 🔥
