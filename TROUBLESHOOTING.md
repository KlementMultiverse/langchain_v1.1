# 🔧 Troubleshooting Guide

Common issues and solutions across all programs in this learning journey.

---

## 🚨 Setup Issues

### **Issue: "python: command not found"**

**Solution**:
```bash
# Try python3
python3 --version

# If not installed:
# Ubuntu/Debian
sudo apt install python3 python3-pip python3-venv

# macOS
brew install python3

# Windows
# Download from python.org
```

---

### **Issue: "No module named 'langchain_core'"**

**Cause**: Package not installed or venv not activated.

**Solution**:
```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# You should see (venv) in your prompt

# 2. Install the package
pip install langchain-core

# 3. Verify
pip list | grep langchain
```

---

### **Issue: Virtual environment not activating**

**Symptoms**: No `(venv)` in prompt

**Solution**:
```bash
# Make sure you're in the right directory
cd langchain_v1.1

# Create venv if it doesn't exist
python3 -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify
which python  # Should show path with /venv/
```

---

## 🤖 Ollama Issues

### **Issue: "Connection refused to localhost:11434"**

**Cause**: Ollama not running.

**Solution**:
```bash
# Start Ollama
ollama serve &

# Verify it's running
curl http://localhost:11434
# Should return: "Ollama is running"

# Check process
ps aux | grep ollama
```

---

### **Issue: "Model 'qwen3:4b' not found"**

**Solution**:
```bash
# Download the model (4GB)
ollama pull qwen3:4b

# Verify
ollama list
# Should show qwen3:4b

# Test it
ollama run qwen3:4b
>>> Hello
# (AI should respond)
# Ctrl+D to exit
```

---

### **Issue: "Model 'nomic-embed-text' not found"** (Day 6 Iteration 3)

**Solution**:
```bash
# Download embedding model (3GB)
ollama pull nomic-embed-text

# Verify
ollama list | grep nomic
```

---

### **Issue: Ollama uses too much RAM**

**Symptoms**: Computer slows down

**Solution**:
```bash
# Unload model from memory
ollama stop qwen3:4b

# Use smaller model
ollama pull qwen3:1.5b  # Smaller, uses less RAM

# Modify code to use smaller model:
model = ChatOllama(model="qwen3:1.5b")
```

---

## 📁 File Issues

### **Issue: "FileNotFoundError: day6_RAG_knowledge.txt"**

**Cause**: File not in current directory.

**Solution**:
```bash
# Check current directory
pwd

# List files
ls -la

# Copy test file from test_data
cp ../test_data/day6_RAG_knowledge.txt .

# Or use full path in code:
loader = TextLoader("../test_data/day6_RAG_knowledge.txt")
```

---

### **Issue: "PermissionError" when reading file**

**Solution**:
```bash
# Check file permissions
ls -l filename.txt

# Make readable
chmod +r filename.txt

# If it's a directory issue
cd /correct/path/
```

---

## 💾 ChromaDB Issues (Day 6 Iteration 3)

### **Issue: "Collection expecting embedding with dimension of 768, got 384"**

**Cause**: Using `query_texts` instead of `query_embeddings`

**Solution**:
```python
# ❌ WRONG (uses ChromaDB's default 384-dim embeddings)
results = collection.query(query_texts=[question])

# ✅ CORRECT (uses your 768-dim embeddings)
question_embedding = embeddings.embed_query(question)
results = collection.query(query_embeddings=[question_embedding])
```

**If error persists**:
```bash
# Delete old database
rm -rf chroma_db

# Re-run program
python day6_03_vector_embeddings.py
```

---

### **Issue: ChromaDB is slow on first run**

**This is expected!** Embedding 297 chunks takes 30-60 seconds.

**Why**: Each chunk needs to be converted to a 768-dimensional vector.

**After first run**: Embeddings are saved to disk, queries are instant!

---

### **Issue: ChromaDB folder keeps growing**

**Cause**: Multiple runs create duplicate data.

**Solution**:
```bash
# Delete old data before running
rm -rf chroma_db

# Or use get_or_create with upsert logic
```

---

## 🔤 Import / Module Issues

### **Issue: "ImportError: cannot import name 'X'"**

**Possible causes**:
1. Package version mismatch
2. Typo in import statement
3. Package not installed

**Solution**:
```bash
# Update packages
pip install --upgrade langchain-core langchain-ollama

# Verify versions
pip list | grep langchain

# Reinstall if needed
pip uninstall langchain-core
pip install langchain-core
```

---

### **Issue: "ModuleNotFoundError: No module named 'chromadb'"**

**Solution**:
```bash
pip install chromadb
```

---

## 🧠 Memory / Context Issues

### **Issue: AI doesn't remember previous conversation**

**Cause**: Forgetting to append AI response to conversation_history.

**Check your code**:
```python
# ✅ CORRECT
conversation_history.append(HumanMessage(content=user_input))
response = model.invoke(conversation_history)
conversation_history.append(response)  # Don't forget this!

# ❌ WRONG (missing append)
conversation_history.append(HumanMessage(content=user_input))
response = model.invoke(conversation_history)
# AI response not added - no memory!
```

---

### **Issue: "Context length exceeded" error**

**Cause**: Too many messages in conversation_history.

**Solution**:
```python
# Truncate to last 10 messages
if len(conversation_history) > 10:
    conversation_history = conversation_history[-10:]
```

---

## 🛠️ Tool Issues (Day 4)

### **Issue: AI doesn't use tools**

**Possible causes**:
1. Tool description unclear
2. System message doesn't mention tools
3. Question doesn't need the tool

**Solution**:
```python
# ✅ Good tool description
@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers together. Use this for multiplication questions."""
    return a * b

# ✅ Clear system message
("system", "You are helpful. When asked math questions, use the available tools.")

# ✅ Explicit question
"Use the multiply tool to calculate 25 times 47"
```

---

### **Issue: "tool_calls is empty"**

**Cause**: AI decided not to use tools.

**Debug**:
```python
print(f"AI response: {response}")
print(f"Tool calls: {response.tool_calls}")

# Check if AI tried to answer directly
if not response.tool_calls:
    print("AI didn't use any tools. Response:", response.content)
```

---

## ⚡ Performance Issues

### **Issue: Program runs slowly**

**Possible causes**:

1. **Large document** - Use text splitters (Day 6 Iter 2)
2. **Many chunks** - Reduce chunk count or increase chunk_size
3. **Ollama CPU mode** - GPU would be faster
4. **First embedding run** - Expected, subsequent runs are fast

**Solutions**:
```python
# Larger chunks = fewer embeddings
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Increase from 500
    chunk_overlap=100
)

# Reduce results
results = collection.query(query_embeddings=[emb], n_results=2)  # Instead of 3
```

---

## 🐛 Runtime Errors

### **Issue: "KeyError: 'topic'"**

**Cause**: Variable name mismatch in chain.

**Solution**:
```python
# Template uses {topic}
prompt = ChatPromptTemplate.from_messages([
    ("human", "Tell me about {topic}")
])

# invoke MUST use same variable name
chain.invoke({"topic": "Python"})  # ✅ CORRECT
chain.invoke({"subject": "Python"})  # ❌ WRONG
```

---

### **Issue: "AttributeError: 'AIMessage' object has no attribute 'X'"**

**Check the attribute name**:
```python
# ✅ CORRECT
response.content  # The text
response.tool_calls  # List of tool calls

# ❌ WRONG
response.text  # Doesn't exist
response.tools  # Doesn't exist
```

---

## 📊 Output Issues

### **Issue: AI gives wrong/strange answers**

**Possible causes**:
1. Temperature too high (try 0.0 for factual)
2. Context doesn't contain answer
3. Prompt needs improvement

**Solutions**:
```python
# Lower temperature for factual answers
model = ChatOllama(model="qwen3:4b", temperature=0.0)

# Better system message
SystemMessage(content="Answer ONLY based on the provided context. If unsure, say 'I don't know'.")

# Check what context AI is seeing
print(f"Context sent to AI:\n{context}")
```

---

## 🔄 Git / GitHub Issues

### **Issue: "Permission denied (publickey)"**

**Cause**: SSH key not configured.

**Solution**:
```bash
# Use HTTPS instead
git remote set-url origin https://github.com/USERNAME/REPO.git

# Or set up SSH key (advanced)
```

---

### **Issue: "Changes not showing on GitHub"**

**Solution**:
```bash
# Check status
git status

# Add all changes
git add .

# Commit
git commit -m "Description"

# Push
git push origin main

# Verify
git log -1  # Check last commit
```

---

## 🆘 Getting Help

**If you're still stuck**:

1. **Check the specific day's README** - Has detailed instructions
2. **Read error messages carefully** - They often tell you exactly what's wrong
3. **Verify your setup**:
   ```bash
   # Is venv activated?
   which python

   # Are packages installed?
   pip list

   # Is Ollama running?
   curl http://localhost:11434

   # Are models available?
   ollama list
   ```

4. **Start fresh**:
   ```bash
   # Deactivate and reactivate venv
   deactivate
   source venv/bin/activate

   # Restart Ollama
   pkill ollama
   ollama serve &
   ```

5. **Isolate the problem**:
   - Does Day 1 work? (Tests basic setup)
   - Does Day 2 work? (Tests Ollama)
   - Which specific line causes the error?

---

## ✅ Verification Checklist

**Before running any program**:

- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] Required packages installed (`pip list`)
- [ ] Ollama running (`curl http://localhost:11434`)
- [ ] Models downloaded (`ollama list`)
- [ ] In correct directory (`pwd`, `ls`)
- [ ] Test files accessible (`ls test_data/`)

---

**"Most issues have simple solutions. Read error messages. Check the basics first."** 🔧
