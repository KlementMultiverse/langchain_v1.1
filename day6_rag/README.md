# Day 6: Building RAG Systems from Scratch

> **"From loading a document to production-ready semantic search - the complete journey."**

---

## 🎯 What is Day 6?

Day 6 is a **progressive learning journey** through RAG (Retrieval-Augmented Generation) systems.

**You'll build 3 complete iterations**, each improving on the previous:

| Iteration | Focus | Status |
|-----------|-------|--------|
| **1** | Basic RAG (document loading + Q&A) | ✅ Complete |
| **2** | Text splitters + keyword search | ✅ Complete |
| **3** | Vector embeddings + semantic search | ✅ Complete |
| **4** | Multi-document (PDF/TXT/MD) | 🔜 Coming |
| **5** | Hybrid search (semantic + keyword) | 🔜 Coming |

---

## 📚 The Learning Path

### **Iteration 1: Basic RAG** (30 min)
**Folder**: `iteration1_basic_rag/`

**What you learn**:
- Document loading with TextLoader
- RAG concept (giving AI your documents)
- RAG + Memory combination
- The limitation (entire document as context)

**Code**: `day6_01_basic_rag.py`

**Key limitation**: Sends ENTIRE document every time → expensive, slow, hits token limits

---

### **Iteration 2: Text Splitters + Keyword Search** (30 min)
**Folder**: `iteration2_text_splitters/`

**What you learn**:
- RecursiveCharacterTextSplitter (smart chunking)
- chunk_size and chunk_overlap parameters
- Keyword-based chunk search
- Token optimization (only send relevant chunks)
- Chunk transparency (show what was used)

**Code**: `day6_02_text_splitters.py`

**Key improvement**: 10,000 words → 1,500 words (85% reduction!)

**Key limitation**: Keyword search = false positives ("rag" matches "storage", "fragmentation")

---

### **Iteration 3: Vector Embeddings + ChromaDB** (60 min)
**Folder**: `iteration3_vector_embeddings/`

**What you learn**:
- Vector embeddings (text → 768-dim numbers)
- nomic-embed-text (local embedding model)
- ChromaDB (vector database with persistence)
- Semantic search (understands meaning, not just keywords)
- HNSW index (fast similarity search)
- Production-ready RAG

**Code**: `day6_03_vector_embeddings.py`

**Key improvement**: Semantic understanding! Finds relevant chunks even with different words.

**This is production-ready** - used in real systems!

---

## 🚀 Quick Start Guide

### **If you're completely new**:
```bash
# Start with Iteration 1
cd iteration1_basic_rag
cat README.md
# Follow the instructions step by step
```

### **If you completed Iteration 1**:
```bash
# Move to Iteration 2
cd iteration2_text_splitters
cat README.md
```

### **If you completed Iteration 2**:
```bash
# Move to Iteration 3 (the best one!)
cd iteration3_vector_embeddings
cat README.md
```

---

## 📊 Comparison Table

| Feature | Iter 1 | Iter 2 | Iter 3 |
|---------|--------|--------|--------|
| **Document loading** | ✅ | ✅ | ✅ |
| **Text splitting** | ❌ | ✅ | ✅ |
| **Search method** | None | Keyword | Semantic |
| **Context sent** | Entire doc | 3 chunks | 3 chunks |
| **Token cost** | HIGH | Medium | Medium |
| **False positives** | N/A | Many | Very few |
| **Storage** | None | None | ChromaDB |
| **Persistence** | ❌ | ❌ | ✅ |
| **Production ready** | ❌ | ❌ | ✅ |
| **Best for** | Learning | Medium docs | Production |

---

## 🛠️ Tech Stack

| Component | Technology | Used In |
|-----------|------------|---------|
| **Document Loading** | TextLoader | All iterations |
| **Text Splitting** | RecursiveCharacterTextSplitter | Iter 2, 3 |
| **Chat Model** | Qwen 3:4B (Ollama) | All iterations |
| **Embeddings** | nomic-embed-text (Ollama) | Iter 3 |
| **Vector DB** | ChromaDB | Iter 3 |
| **Memory** | conversation_history list | All iterations |

---

## 📦 Installation Summary

### **Iteration 1 needs**:
```bash
pip install langchain-core langchain-ollama langchain-community
```

### **Iteration 2 adds**:
```bash
pip install langchain-text-splitters
```

### **Iteration 3 adds**:
```bash
pip install chromadb
ollama pull nomic-embed-text
```

---

## 📁 Test Data

**Location**: `test_data/` folder

**Files**:
- `day6_RAG_knowledge.txt` - Small file (5,814 chars) for quick testing
- `langchain_1000_lines.txt` - Large file (107KB, 11,589 words) for comprehensive testing

**Usage**:
```bash
# Copy to your iteration folder when needed
cp ../test_data/langchain_1000_lines.txt .
```

---

## 🎯 Learning Outcomes

**After completing all 3 iterations**, you will:

✅ Understand what RAG is and why it's critical
✅ Load and process documents with LangChain
✅ Split large documents into manageable chunks
✅ Implement keyword-based search
✅ Understand vector embeddings and semantic similarity
✅ Use ChromaDB for persistent vector storage
✅ Build production-ready RAG systems
✅ Combine RAG with conversation memory
✅ Optimize token usage and costs
✅ Debug common RAG issues

**You'll have mastered** the #1 production pattern for LLM applications!

---

## 💡 Why RAG Matters

**RAG solves these critical problems**:

1. **AI doesn't know YOUR data**
   - Your company docs
   - Your research papers
   - Your customer data
   - Your codebase

2. **AI training cutoff**
   - Models don't know recent events
   - Can't answer about new products
   - Miss latest updates

3. **Hallucination**
   - AI makes up answers when unsure
   - RAG grounds responses in real documents
   - Provides source citations

4. **Context window limits**
   - Can't send entire knowledge base
   - RAG retrieves only relevant chunks
   - Scales to millions of documents

---

## 🏗️ Real-World Applications

**RAG powers**:

- 📚 **Document Q&A** - Ask questions about PDFs, manuals, contracts
- 🎓 **Educational tutors** - Teach from textbooks and courses
- 💼 **Customer support** - Answer from knowledge bases
- ⚖️ **Legal research** - Search case law and regulations
- 🏥 **Medical diagnosis** - Reference medical literature
- 🔬 **Research assistants** - Navigate scientific papers
- 💻 **Code search** - Find relevant code in large repos
- 📰 **News analysis** - Query news archives

**If you see "AI that knows your documents"** → It's RAG!

---

## 🎓 The RAG Progression

### **Why 3 Iterations?**

**Learning philosophy**: Build → Identify limitation → Improve → Repeat

**Iteration 1**: "Here's the document, AI!"
- ✅ Simple and intuitive
- ❌ Doesn't scale

**Iteration 2**: "Here are the relevant parts, AI!"
- ✅ Scales to large documents
- ❌ Keyword search is primitive

**Iteration 3**: "Here are the semantically similar parts, AI!"
- ✅ Understands meaning
- ✅ Production-ready
- ✅ This is what companies use!

**Each iteration teaches a lesson** - by the end, you understand WHY production RAG works the way it does.

---

## ⏱️ Time Commitment

| Iteration | Time | Cumulative |
|-----------|------|------------|
| Iteration 1 | 30 min | 30 min |
| Iteration 2 | 30 min | 1 hour |
| Iteration 3 | 60 min | 2 hours |
| **Total** | **2 hours** | **Complete RAG mastery!** |

**Worth it?** Absolutely. RAG is THE most important production pattern.

---

## 🔮 What's Coming (Iterations 4-5)

### **Iteration 4: Multi-Document RAG**
- Load PDFs, Markdown, HTML, CSVs
- Multiple documents in one system
- Source citations ("According to document X...")
- Metadata filtering

### **Iteration 5: Hybrid Search**
- Combine semantic + keyword search
- Best of both worlds
- Re-ranking strategies
- Production optimization

**These will be added** as the learning journey continues!

---

## 🐛 Common Issues Across All Iterations

### **"Ollama not running"**
```bash
ollama serve &
curl http://localhost:11434
```

### **"Model not found"**
```bash
ollama pull qwen3:4b
ollama pull nomic-embed-text  # For Iteration 3
```

### **"File not found"**
```bash
# Copy from test_data
cp ../test_data/langchain_1000_lines.txt .
```

### **"No module named X"**
```bash
source ../../venv/bin/activate
pip install <missing-package>
```

**For detailed troubleshooting**: See `../../TROUBLESHOOTING.md`

---

## 📚 Recommended Order

1. **Complete Days 1-5 first** (if you haven't)
   - You need Messages, Chains, and Memory concepts

2. **Do iterations in order** (1 → 2 → 3)
   - Each builds on the previous
   - Understanding limitations is key

3. **Type the code yourself**
   - Don't copy-paste
   - Muscle memory matters

4. **Experiment between iterations**
   - Try different chunk sizes
   - Test with your own documents
   - Break things and fix them

---

## 🎉 Congratulations!

If you completed all 3 iterations, you now understand:

🔥 **RAG at a production level**
🔥 **Vector databases and semantic search**
🔥 **Document processing pipelines**
🔥 **Token optimization strategies**

**You're ready** to build real RAG applications!

---

**Next Steps**:
- Build a RAG system for YOUR documents
- Explore iterations 4-5 (when available)
- Learn LangGraph for multi-agent systems
- Deploy your RAG system to production

---

**"Collaborative Learning - The Next Genesis Learning"**

*From documents to knowledge. From knowledge to intelligence.* 🔥
