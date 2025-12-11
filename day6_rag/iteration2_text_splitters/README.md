# Day 6 - Iteration 2: Text Splitters + Keyword Search

> **"Don't send the whole book. Send only the relevant pages."**

---

## 🎯 What You'll Learn

- ✅ **RecursiveCharacterTextSplitter** - Split documents intelligently
- ✅ **Chunking strategies** - chunk_size and chunk_overlap
- ✅ **Keyword-based search** - Find relevant chunks
- ✅ **Token optimization** - Send only what's needed
- ✅ **Chunk transparency** - Show which chunks were used

**Time needed**: 30 minutes

---

## 📋 What You Already Have

From Iteration 1:
- ✅ Document loading with TextLoader
- ✅ Basic RAG + Memory pattern
- ✅ langchain-community installed

---

## 🆕 What's New

**New package**: `langchain-text-splitters`

```bash
pip install langchain-text-splitters
```

**New concepts**:
- Text splitting (chunking)
- Keyword search across chunks
- Chunk metadata tracking

---

## 📖 How Text Splitting Works

### **The Problem (Iteration 1)**:
```
Document: 10,000 words
Question: "What is RAG?"
Iteration 1: Sends ALL 10,000 words ❌
```

### **The Solution (Iteration 2)**:
```
Document: 10,000 words → Split into 20 chunks of 500 words each
Question: "What is RAG?"
Search: Find 3 relevant chunks (1,500 words total)
Send: Only those 3 chunks ✅
```

**Savings**: 10,000 words → 1,500 words (85% reduction!)

---

## 🔧 RecursiveCharacterTextSplitter

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # Target size per chunk
    chunk_overlap=50       # Overlap between chunks
)

chunks = text_splitter.split_documents(docs)
```

### **Parameters**:

**chunk_size=500**:
- Target: 500 characters per chunk
- Actual: May be less (splits at natural boundaries)

**chunk_overlap=50**:
- Last 50 chars of chunk N = First 50 chars of chunk N+1
- Prevents losing context at boundaries

### **Why "Recursive"?**:

Tries to split at natural boundaries in this order:
1. Double newlines (paragraphs)
2. Single newlines (sentences)
3. Spaces (words)
4. Characters (last resort)

**Result**: Readable, meaningful chunks!

---

## 🔍 Keyword Search Pattern

```python
# Extract keywords from question
question_words = question.lower().split()

# Find chunks containing keywords
relevant_chunks = []
for idx, chunk in enumerate(chunks):
    chunk_text = chunk.page_content.lower()
    if any(word in chunk_text for word in question_words):
        relevant_chunks.append((idx, chunk.page_content))

# Take top 3
top_3 = relevant_chunks[:3]
```

**How it works**:
1. Split question into words: "What is RAG?" → ["what", "is", "rag"]
2. Check each chunk for ANY of those words
3. Collect matching chunks
4. Take first 3

---

## 🚀 How to Run

### **Setup**:
```bash
cd day6_rag/iteration2_text_splitters

# Copy test file
cp ../test_data/langchain_1000_lines.txt .

# Or copy smaller file for quick test
cp ../test_data/day6_RAG_knowledge.txt .

# Activate venv
source ../../venv/bin/activate

# Install if needed
pip install langchain-text-splitters
```

### **Run**:
```bash
python day6_02_text_splitters.py
```

### **When prompted**:
```
Enter the filename: langchain_1000_lines.txt
```

---

## 📊 Expected Output

```
============================================================
Iteration 2: Text Splitters and basic Chunk search
============================================================

 Enter the filename : langchain_1000_lines.txt

 Loading 'langchain_1000_lines.txt'....

  Characters count : 105632
 words count : 11589

============================================================
 Splitting the document into chunks
============================================================

 Document split into 297 chunks!
 Original size is 105632 characters
 Each chunk is 500 characters

 Model Loading....
 Model Loaded Successfully

============================================================
 Ask Questions
AI will remember conversations and search chunks
============================================================
 Type 'exit' to quit

 You: What is RAG?

 Searching 297 chunks!...

 Found 89 relevant chunks!
 Using 3 chunks: [12, 45, 78]
 Total context: 1425 chars

 📄 Selected Chunks Preview:
   Chunk #12: RAG stands for Retrieval-Augmented Generation...
   Chunk #45: Vector databases store embeddings...
   Chunk #78: Semantic search finds similar meaning...

 AI: RAG stands for Retrieval-Augmented Generation. It combines...
```

---

## 💡 Key Improvements Over Iteration 1

| Aspect | Iteration 1 | Iteration 2 |
|--------|-------------|-------------|
| **Context sent** | Entire document | Only 3 chunks |
| **Token cost** | 10,000+ tokens | ~400 tokens |
| **Speed** | Slow (large context) | Fast (small context) |
| **Scalability** | Breaks on large docs | Works with any size |
| **Transparency** | No idea what was used | Shows chunk numbers |

---

## 🔍 Limitations (Why We Need Iteration 3)

**Problem with keyword search**:

```
Question: "What is RAG?"
Keyword: "rag"

False positives found:
- "storage systems" (contains "rag")
- "fragmentation" (contains "rag")
- "SkyAGI framework" (contains "rag")
```

**Solution**: Iteration 3 (semantic search with embeddings)
- Understands MEANING, not just keywords
- "What is RAG?" finds chunks about "Retrieval-Augmented Generation"
- Even if the exact word "RAG" isn't present!

---

## 🎯 Practice Exercises

### **Exercise 1: Adjust Chunk Size**
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Larger chunks
    chunk_overlap=100
)
```

Test with different sizes: 200, 500, 1000, 2000

**Observe**: How does it affect chunk count and answer quality?

---

### **Exercise 2: Take More Chunks**
```python
# Instead of top 3, take top 5
top_chunks = relevant_chunks[:5]
```

**Question**: Does more context always improve answers?

---

### **Exercise 3: Add Relevance Scoring**
```python
# Count how many keywords each chunk contains
scored_chunks = []
for idx, chunk in enumerate(chunks):
    score = sum(1 for word in question_words if word in chunk.page_content.lower())
    if score > 0:
        scored_chunks.append((score, idx, chunk.page_content))

# Sort by score (highest first)
scored_chunks.sort(reverse=True)

# Take top 3
top_chunks = scored_chunks[:3]
```

---

## 📚 What You Learned

✅ **Text splitting** - Break documents into manageable chunks
✅ **RecursiveCharacterTextSplitter** - Smart, boundary-aware splitting
✅ **Chunk parameters** - chunk_size and chunk_overlap
✅ **Keyword search** - Simple but effective retrieval
✅ **Token optimization** - Only send relevant chunks
✅ **Limitations** - Why semantic search is better

---

## ⏭️ What's Next?

**Iteration 3: Vector Embeddings + ChromaDB**

The production-ready approach:
- **nomic-embed-text** - Convert text to 768-dim vectors
- **ChromaDB** - Store and search vectors efficiently
- **Semantic search** - Understand meaning, not just keywords
- **HNSW index** - Fast similarity search
- **Persistent storage** - Save embeddings to disk

**Setup needed**:
- `chromadb` package
- Understanding of embeddings

```bash
cd ../iteration3_vector_embeddings
cat README.md
```

---

**"Collaborative Learning - The Next Genesis Learning"**

*From keywords to meaning. From simple to semantic.* 🔥
