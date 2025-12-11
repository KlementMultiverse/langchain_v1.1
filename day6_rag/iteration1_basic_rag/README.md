# Day 6 - Iteration 1: Basic RAG

> **"Give AI access to YOUR data, and it becomes YOUR expert."**

---

## 🎯 What You'll Learn

By the end of this iteration, you'll understand:
- ✅ **What RAG is** - Retrieval-Augmented Generation
- ✅ **Document loading** - Reading text files into LangChain
- ✅ **RAG + Memory** - Combining document knowledge with conversation context
- ✅ **The limitation** - Why this approach doesn't scale
- ✅ **Preview of iteration 2** - How we'll improve it

**Time needed**: 30 minutes

---

## 📋 What You Already Have

**From Days 1-5**, you have:
- ✅ Messages, model.invoke(), chains, tools
- ✅ Conversation memory pattern
- ✅ Ollama with Qwen 3:4B

---

## 🆕 What's New Today

**New package needed**: `langchain-community` (for document loaders)

### **Installation**:

```bash
# Activate venv
source ../../venv/bin/activate

# Install langchain-community
pip install langchain-community

# Verify
pip list | grep langchain-community
```

---

## 📖 What is RAG?

**RAG = Retrieval-Augmented Generation**

### **The Problem**:

**AI models have limitations**:
1. **Training cutoff** - Don't know recent events
2. **No access to YOUR data** - Can't answer about YOUR documents
3. **Hallucination** - Make up answers when unsure

**Example**:
```
You: "What did our company decide in the Q3 meeting?"
AI: "I don't have access to your company's internal documents."
```

---

### **The RAG Solution**:

**Give AI access to documents at query time!**

**Flow**:
```
1. User asks question
2. System retrieves relevant documents/chunks
3. System gives documents to AI as context
4. AI answers based on the documents
5. AI can cite sources!
```

**Same example with RAG**:
```
You: "What did our company decide in the Q3 meeting?"
[System loads Q3_meeting_notes.txt]
AI: "According to the Q3 meeting notes, the company decided to..."
```

**RAG = Memory for documents, not just conversation!**

---

## 📖 Understanding the Code

### **Line 1: Import Document Loader**

```python
from langchain_community.document_loaders import TextLoader
```

**TextLoader** - Loads .txt files into LangChain Document objects.

---

### **Lines 7-9: Load Document**

```python
loader = TextLoader("day6_RAG_knowledge.txt")
docs = loader.load()
```

**What happens**:
1. `TextLoader` opens the file
2. Reads all content
3. Returns a list of Document objects

**docs structure**:
```python
docs = [
    Document(
        page_content="What is RAG?\n\nRAG stands for...",  # The actual text
        metadata={"source": "day6_RAG_knowledge.txt"}      # File info
    )
]
```

**Usually just 1 document** for text files (unless very large).

---

### **Line 11: Access Document Content**

```python
print(f" Loaded document has {len(docs[0].page_content)} characters")
```

**docs[0]** - First (and usually only) document
**page_content** - The actual text content

---

### **Lines 19-20: The RAG Pattern**

```python
conversation_history = [
    SystemMessage(content=f"answer based on this document {docs[0].page_content}")
]
```

**This is the key!**

**What this does**:
- Puts ENTIRE document in SystemMessage
- Tells AI to answer based on this document
- AI now has access to the document content!

**SystemMessage structure**:
```
"answer based on this document [ENTIRE TEXT OF DOCUMENT HERE]"
```

**This is basic RAG** - giving AI the document as context.

---

### **Lines 27-41: Interactive Q&A Loop**

```python
while True:
    question = input("You: ")
    if question.lower() == 'exit':
        break

    conversation_history.append(HumanMessage(content=question))
    response = model.invoke(conversation_history)
    conversation_history.append(response)

    print(f"AI: {response.content} \n")
```

**This is the SAME pattern** from Day 5 (Memory)!

**Combination**:
- Memory (conversation_history)
- RAG (document in SystemMessage)

**Result**: AI that remembers conversation AND knows your document!

---

## 🚀 How to Run

### **Step 1: Navigate to Iteration 1 Folder**

```bash
cd day6_rag/iteration1_basic_rag
```

---

### **Step 2: Check Test Data Exists**

```bash
# The program expects day6_RAG_knowledge.txt in the current folder
# But we moved it to test_data!

# Option 1: Copy test file here (recommended for this iteration)
cp ../test_data/day6_RAG_knowledge.txt .

# Option 2: Modify line 8 in the code to point to test_data:
# loader = TextLoader("../test_data/day6_RAG_knowledge.txt")
```

---

### **Step 3: Verify Ollama**

```bash
curl http://localhost:11434
```

---

### **Step 4: Activate Virtual Environment**

```bash
source ../../venv/bin/activate
```

---

### **Step 5: Install langchain-community (First Time)**

```bash
pip install langchain-community
```

---

### **Step 6: Run the Program**

```bash
python day6_01_basic_rag.py
```

---

## 📊 Expected Output

```
Step 1: Loading document
 Loaded document has 5814 characters
 Preview What is RAG?

RAG stands for Retrieval-Augmented Generation....

Step 2: Loading AI model...
✅ Model loaded!

============================================================
RAG Chatbot - Ask questions about the document!
============================================================
Type 'exit' to quit

You: What is RAG?
AI: RAG stands for Retrieval-Augmented Generation. It's a technique that combines...

You: Why do we need it?
AI: We need RAG because AI models have limitations. They don't have access to...

You: exit

 Total messages in memory : 5
```

**Notice**: AI answers are based on the DOCUMENT, not general knowledge!

---

## 💡 Key Concepts Explained

### **1. Document Object Structure**

**When you load a document**:
```python
docs = loader.load()
# docs[0] = Document object

# Access text:
text = docs[0].page_content

# Access metadata:
source = docs[0].metadata['source']
```

**Metadata** can include:
- source (file path)
- page number (for PDFs)
- created date
- custom fields

---

### **2. RAG vs. Fine-Tuning**

**Common confusion**: "Why not fine-tune the model on my data?"

| Approach | When to Use | Pros | Cons |
|----------|-------------|------|------|
| **Fine-Tuning** | Change model behavior | Permanent knowledge | Expensive, slow, can't update easily |
| **RAG** | Add knowledge at query time | Cheap, fast, easy to update | Needs good retrieval |

**RAG is usually better** for:
- Frequently changing data
- Large knowledge bases
- Cost-sensitive applications
- Quick prototypes

---

### **3. Why This is "Basic" RAG**

**What this iteration does**:
```
[Entire Document] → SystemMessage → AI
```

**Problems**:
1. **Token limits** - Large documents exceed context window
2. **Expensive** - Sending entire doc costs many tokens
3. **Slow** - Processing large context takes time
4. **Irrelevant info** - AI sees everything, even unrelated parts

**Example**:
```
Document: 100-page manual (50,000 words)
Question: "What is the warranty period?"
Problem: AI reads ALL 100 pages to find 1 sentence about warranty!
```

**Solution**: Iteration 2 (tomorrow) - split into chunks, send only relevant ones!

---

### **4. RAG + Memory Combination**

**conversation_history structure**:
```python
[
    SystemMessage(content="answer based on [DOCUMENT]"),  # RAG
    HumanMessage(content="What is RAG?"),                  # Turn 1
    AIMessage(content="RAG is..."),
    HumanMessage(content="Why use it?"),                   # Turn 2
    AIMessage(content="Because...")
]
```

**AI sees**:
- Document (from SystemMessage) ✅
- Previous conversation (from messages list) ✅

**Result**: Contextual answers based on YOUR data!

---

## 🎯 Practice Exercises

### **Exercise 1: Use Your Own Document**

Create a new text file with information about YOUR topic:

```bash
# Create a file about your hobby, project, or interest
echo "My Project Information

Project Name: MyApp
Purpose: Helps users organize tasks
Tech Stack: Python, React
..." > my_document.txt

# Modify line 8 in the code:
loader = TextLoader("my_document.txt")
```

**Ask questions** about YOUR document!

---

### **Exercise 2: Add Document Stats**

After loading, show more stats:

```python
docs = loader.load()

content = docs[0].page_content
char_count = len(content)
word_count = len(content.split())
line_count = content.count('\n') + 1

print(f"📊 Document Stats:")
print(f"  Characters: {char_count}")
print(f"  Words: {word_count}")
print(f"  Lines: {line_count}")
```

---

### **Exercise 3: Try Multiple Documents**

Load and combine multiple files:

```python
from langchain_community.document_loaders import TextLoader

# Load multiple documents
loaders = [
    TextLoader("doc1.txt"),
    TextLoader("doc2.txt"),
    TextLoader("doc3.txt")
]

all_docs = []
for loader in loaders:
    all_docs.extend(loader.load())

# Combine all content
combined_content = "\n\n".join([doc.page_content for doc in all_docs])

# Use in SystemMessage
conversation_history = [
    SystemMessage(content=f"answer based on these documents:\n{combined_content}")
]
```

---

## 🔍 Common Issues & Solutions

### **Issue 1: "FileNotFoundError: day6_RAG_knowledge.txt"**

**Cause**: File not in current directory.

**Solution**:
```bash
# Copy test file
cp ../test_data/day6_RAG_knowledge.txt .

# Or modify code to use full path
loader = TextLoader("../test_data/day6_RAG_knowledge.txt")
```

---

### **Issue 2: "No module named 'langchain_community'"**

**Solution**:
```bash
pip install langchain-community
```

---

### **Issue 3: AI gives wrong answers**

**Possible causes**:
1. Document doesn't contain the information
2. AI is using its general knowledge (add "ONLY use the document" to SystemMessage)
3. Document is too large (wait for Iteration 2!)

---

## 📚 What You Learned

By completing Iteration 1, you now understand:

✅ **What RAG is** - Giving AI access to YOUR documents
✅ **Document loading** - TextLoader for .txt files
✅ **Basic RAG pattern** - Document in SystemMessage
✅ **RAG + Memory** - Combining two powerful patterns
✅ **The limitations** - Why we need iteration 2

---

## 🎓 Real-World Applications

**This basic RAG approach works for**:
- ✅ Small documents (< 5,000 words)
- ✅ Quick prototypes
- ✅ Learning and experimentation

**Production systems need** (coming in iterations 2-3):
- Chunking for large documents
- Semantic search (vector databases)
- Multiple document formats (PDF, HTML, MD)
- Source citations
- Hybrid retrieval

---

## ⏭️ What's Next?

**Iteration 2: Text Splitters + Keyword Search**

You'll learn:
- **RecursiveCharacterTextSplitter** - Split documents intelligently
- **Chunk-based search** - Find relevant chunks (not entire doc)
- **Token optimization** - Send only what's needed
- **Chunk tracking** - Show which parts were used

**Problem we'll solve**:
```
❌ Iteration 1: Send entire 10,000-word document
✅ Iteration 2: Send only 3 relevant 500-word chunks
```

**Setup needed**:
- `langchain-text-splitters` (we'll install)

---

**Ready for Iteration 2?** Navigate to the folder:

```bash
cd ../iteration2_text_splitters
cat README.md
```

---

**"Collaborative Learning - The Next Genesis Learning"**

*From general AI to YOUR AI. From theory to practice.* 🔥
