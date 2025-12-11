# Day 3: Chains & LCEL - Building Reusable AI Workflows

> **"Stop writing the same prompts over and over. Build chains once, use them forever."**

---

## 🎯 What You'll Learn Today

By the end of this lesson, you'll understand:
- ✅ **Prompt Templates** - Reusable prompts with variables
- ✅ **The Pipe Operator** `|` - Chain components together
- ✅ **LCEL** (LangChain Expression Language) - The elegant way to build workflows
- ✅ **Output Parsers** - Get clean string output instead of Message objects
- ✅ **chain.invoke()** - Run complete workflows with one call

**Programs**: 2 (`day3_simple_chain.py` and `day3_parser_chain.py`)
**Time needed**: 45 minutes

---

## 📋 What You Already Have

**From Days 1 & 2**, you have:
- ✅ Virtual environment setup
- ✅ `langchain-core` installed
- ✅ `langchain-ollama` installed
- ✅ Ollama running with Qwen 3:4B model
- ✅ Understanding of Messages and model.invoke()

**Verify**:
```bash
# Activate venv
source venv/bin/activate

# Check Ollama is running
curl http://localhost:11434

# Should return: "Ollama is running"
```

---

## 🆕 What's New Today

**Good news**: NO new installations needed!

**What's new** is HOW we use what we have:
- `ChatPromptTemplate` (from langchain-core - already installed!)
- `StrOutputParser` (from langchain-core - already installed!)
- The `|` pipe operator (LCEL syntax)

---

## 📖 Program 1: Simple Chain (day3_simple_chain.py)

### **The Problem This Solves**

**Without chains** (Day 2 way):
```python
# Want to ask about Python with funny style
messages = [
    SystemMessage(content="you are helpful, be funny"),
    HumanMessage(content="tell me about Python")
]
response = model.invoke(messages)

# Want to ask about JavaScript with serious style
# Ugh, have to rewrite everything!
messages = [
    SystemMessage(content="you are helpful, be serious"),
    HumanMessage(content="tell me about JavaScript")
]
response = model.invoke(messages)
# Repetitive and error-prone!
```

**With chains** (Day 3 way):
```python
# Define template ONCE
prompt = ChatPromptTemplate.from_messages([
    ("system", "you are helpful, be {style}"),
    ("human", "tell me about {topic}")
])

chain = prompt | model

# Use it MANY times
response1 = chain.invoke({"topic": "Python", "style": "funny"})
response2 = chain.invoke({"topic": "JavaScript", "style": "serious"})
response3 = chain.invoke({"topic": "Rust", "style": "poetic"})
# Clean, reusable, beautiful!
```

---

### **Understanding the Code Line by Line**

#### **Line 1: Import ChatPromptTemplate**
```python
from langchain_core.prompts import ChatPromptTemplate
```

**What it is**: A template for creating messages with variable placeholders.

---

#### **Lines 4-7: Initialize Model (Same as Day 2)**
```python
model = ChatOllama(
    model="qwen3:4b",
    temperature=0.7
)
```

**You already know this!** Same model initialization from Day 2.

---

#### **Lines 9-12: Create Prompt Template**
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a helpful assistant, Be {style} while responding"),
    ("human", "tell me about {topic}")
])
```

**Breaking it down**:

| Part | Meaning |
|------|---------|
| `("system", "...")` | Creates a SystemMessage |
| `("human", "...")` | Creates a HumanMessage |
| `{style}` | Variable placeholder - will be replaced |
| `{topic}` | Another variable placeholder |

**Think of it like**: A template with blanks to fill in later.

**Template**:
```
System: "Be {style}"
Human: "Tell me about {topic}"
```

**After filling in** `{style: "funny", topic: "Python"}`:
```
System: "Be funny"
Human: "Tell me about Python"
```

---

#### **Line 14: The Magic Pipe Operator**
```python
chain = prompt | model
```

**This is LCEL** (LangChain Expression Language)!

**What `|` does**: Connects components in a sequence.

**Read it as**: "Take `prompt`, THEN pass output to `model`"

**Visualize**:
```
Input (dict) → prompt → messages → model → AIMessage
             ↑ pipe!            ↑ pipe!
```

**Flow**:
1. You pass `{"topic": "Python", "style": "funny"}`
2. `prompt` fills in variables → creates messages
3. `|` pipes messages to `model`
4. `model` invokes AI → returns AIMessage

---

#### **Line 16: Invoke the Chain**
```python
response = chain.invoke({"topic": "Python", "style": "Funny"})
```

**What happens**:
1. Dictionary goes to `prompt`
2. `prompt` creates:
   ```python
   [
       SystemMessage(content="Be Funny while responding"),
       HumanMessage(content="tell me about Python")
   ]
   ```
3. Messages go to `model`
4. `model` returns AIMessage
5. `response` = that AIMessage

**One line does it all!** 🎉

---

#### **Line 18: Print Response**
```python
print("answer is: ", response.content)
```

**response.content** - The AI's generated text.

---

## 📖 Program 2: Parser Chain (day3_parser_chain.py)

### **The Problem This Solves**

**With simple chain** (Program 1):
```python
response = chain.invoke({"topic": "Python"})
print(type(response))  # <class 'langchain_core.messages.ai.AIMessage'>
print(response.content)  # Have to access .content
```

**With parser chain** (Program 2):
```python
response = chain.invoke({"topic": "Python"})
print(type(response))  # <class 'str'> ← Clean string!
print(response)  # Direct use, no .content needed
```

**Why this matters**: Often you just want the text, not the whole Message object.

---

### **Understanding the Code**

#### **Line 3: Import StrOutputParser**
```python
from langchain_core.output_parsers import StrOutputParser
```

**What it does**: Converts AIMessage → clean string

---

#### **Line 16: Create Parser**
```python
output_parser = StrOutputParser()
```

**This extracts** `message.content` automatically.

---

#### **Line 19: Three-Step Chain**
```python
chain = prompt | model | output_parser
```

**The triple pipe!**

**Flow**:
```
Input dict → prompt → messages → model → AIMessage → parser → string
          ↑ pipe 1           ↑ pipe 2             ↑ pipe 3
```

**Step by step**:
1. `{"question": "What is Python?"}` → `prompt`
2. `prompt` → `[SystemMessage(...), HumanMessage("What is Python?")]`
3. Messages → `model`
4. `model` → `AIMessage(content="Python is a programming language...")`
5. AIMessage → `output_parser`
6. `output_parser` → `"Python is a programming language..."` (just the string!)

---

#### **Line 22: Invoke Returns String**
```python
answer = chain.invoke({"question": "What is Python?"})
print(type(answer))  # <class 'str'>
print(answer)  # Direct string!
```

**No .content needed!** The parser handled it.

---

## 🚀 How to Run

### **Step 1: Verify Ollama is Running**
```bash
curl http://localhost:11434
```

---

### **Step 2: Navigate to Day 3 Folder**
```bash
cd day3_chains
```

---

### **Step 3: Activate Virtual Environment**
```bash
source ../venv/bin/activate  # Linux/macOS
# or
..\venv\Scripts\activate  # Windows
```

---

### **Step 4: Run Program 1 (Simple Chain)**
```bash
python day3_simple_chain.py
```

**Expected output**:
```
answer is: Why did the Python go to the party? Because it was a real "snake" in the grass! ...
[Funny explanation about Python programming language]
```

---

### **Step 5: Run Program 2 (Parser Chain)**
```bash
python day3_parser_chain.py
```

**Expected output**:
```
<class 'str'>
Python is a high-level, interpreted programming language known for its simplicity and readability.
```

**Notice**: Type is `str`, not `AIMessage`!

---

## 💡 Key Concepts Explained

### **1. What is LCEL?**

**LCEL** = LangChain Expression Language

**It's the `|` syntax** for chaining components.

**Benefits**:
- ✅ **Readable**: `prompt | model | parser` reads like English
- ✅ **Composable**: Mix and match components
- ✅ **Streaming support**: Can stream responses (advanced)
- ✅ **Async support**: Can run asynchronously (advanced)

**Compare**:

**Without LCEL** (verbose):
```python
messages = prompt.format(topic="Python", style="funny")
response = model.invoke(messages)
text = output_parser.parse(response)
```

**With LCEL** (elegant):
```python
chain = prompt | model | output_parser
text = chain.invoke({"topic": "Python", "style": "funny"})
```

---

### **2. Prompt Templates vs Manual Messages**

**Manual way** (Day 2):
```python
messages = [
    SystemMessage(content="Be helpful and funny"),
    HumanMessage(content="Tell me about Python")
]
```

**Template way** (Day 3):
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Be helpful and {style}"),
    ("human", "Tell me about {topic}")
])
```

**Why templates win**:
- ✅ **Reusable**: Define once, use many times
- ✅ **Variables**: Easy to swap values
- ✅ **Less error-prone**: No manual string formatting
- ✅ **Maintainable**: Change template in one place

---

### **3. When to Use Output Parsers?**

**Use StrOutputParser when**:
- ✅ You just want the text
- ✅ Integrating with other systems (APIs, databases)
- ✅ Building chatbot responses

**Don't use parser when**:
- ❌ You need message metadata
- ❌ You need to inspect message type
- ❌ You're building conversation history (need full AIMessage)

---

### **4. Chain Composition**

**Chains are composable** - you can build complex workflows:

```python
# 2-step chain
chain1 = prompt | model

# 3-step chain
chain2 = prompt | model | parser

# Could even chain chains! (advanced)
chain3 = chain1 | some_other_component
```

**You're building pipelines** for data flow!

---

## 🎯 Practice Exercises

### **Exercise 1: Add More Variables**

Modify `day3_simple_chain.py` to include a third variable:

**Template**:
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "Be {style}, use {language} language level"),
    ("human", "Explain {topic}")
])
```

**Invoke with**:
```python
chain.invoke({
    "topic": "quantum physics",
    "style": "simple",
    "language": "5-year-old"
})
```

---

### **Exercise 2: Build a Translator Chain**

Create a chain that translates text:

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a translator. Translate from {from_lang} to {to_lang}"),
    ("human", "{text}")
])

chain = prompt | model | output_parser

result = chain.invoke({
    "from_lang": "English",
    "to_lang": "Spanish",
    "text": "Hello, how are you?"
})
print(result)  # Should print Spanish translation!
```

---

### **Exercise 3: Multi-Step Chain**

Build a chain that:
1. Takes a topic
2. Asks AI to write a poem (first chain)
3. Takes the poem and summarizes it (second chain)

**Hint**: Use the output of one chain as input to another!

---

### **Exercise 4: Different Temperatures**

Create 3 chains with different temperatures:
- `creative_chain` (temperature=1.0)
- `balanced_chain` (temperature=0.7)
- `factual_chain` (temperature=0.0)

Ask the same question with each - compare results!

---

## 🔍 Common Issues & Solutions

### **Issue 1: "KeyError: 'topic'"**

**Cause**: Variable name mismatch.

**Example**:
```python
# Template uses {topic}
prompt = ChatPromptTemplate.from_messages([
    ("human", "{topic}")
])

# But invoke uses different key!
chain.invoke({"subject": "Python"})  # ❌ Error!
```

**Solution**: Match variable names exactly:
```python
chain.invoke({"topic": "Python"})  # ✅ Correct
```

---

### **Issue 2: "Cannot pipe X to Y"**

**Cause**: Incompatible components.

**Rule**: Output of left side must match input of right side.

**Good**:
```python
prompt | model  # ✅ prompt outputs messages, model accepts messages
model | parser  # ✅ model outputs AIMessage, parser accepts AIMessage
```

**Bad**:
```python
model | prompt  # ❌ model outputs AIMessage, prompt expects dict
```

---

### **Issue 3: Parser returns None**

**Cause**: AI returned empty response (rare).

**Solution**: Check temperature or rephrase prompt.

---

## 📚 What You Learned

By completing Day 3, you now understand:

✅ **Prompt templates** - Reusable prompts with variables
✅ **The pipe operator `|`** - LCEL syntax for chaining
✅ **Chain composition** - prompt | model | parser
✅ **Output parsers** - Convert AIMessage → clean types
✅ **chain.invoke()** - Run entire workflows with one call

---

## 🎓 Deep Dive: Why Chains Matter

**Today** you learned to chain 2-3 components.

**But chains can be MUCH more complex**:

```python
# Production RAG chain (you'll build this in Day 6!)
chain = (
    question_rewriter
    | vector_db_retriever
    | context_builder
    | prompt_template
    | model
    | output_parser
    | response_formatter
)
```

**Each `|`** = one step in a complex AI workflow.

**Chains are the foundation** of:
- RAG systems (Day 6)
- Agents (Day 8+)
- Multi-step reasoning
- Tool-using AI
- Production applications

**You just learned** the core syntax that powers everything else in LangChain!

---

## 📊 Quick Comparison

| Aspect | Day 2 (Manual) | Day 3 (Chains) |
|--------|----------------|----------------|
| **Reusability** | Write messages every time | Define template once |
| **Variables** | Manual string formatting | {variable} placeholders |
| **Syntax** | Multiple lines | Single pipe chain |
| **Output** | AIMessage object | Can parse to string |
| **Maintainability** | Error-prone | Clean and clear |

---

## ⏭️ What's Next?

**Day 4: Tools**

Now that you can build efficient AI workflows, you'll learn:
- **Tool definition** - Let AI call Python functions
- **Tool binding** - Give AI access to tools
- **Tool execution** - AI decides WHEN to use tools
- **Function calling** - The foundation of AI agents

**Setup needed for Day 4**:
- Nothing new! Same environment.

---

## 💬 Questions & Discussion

**Q: Can I use multiple prompts in one chain?**
A: Not directly with `|`, but you can compose chains creatively. Advanced topic!

**Q: What other parsers exist besides StrOutputParser?**
A: Many! JSONOutputParser, CSVParser, etc. We'll explore in advanced lessons.

**Q: Can chains be async?**
A: Yes! Use `await chain.ainvoke()` - advanced topic.

**Q: What if I want to modify the prompt dynamically?**
A: Use partial variables or build prompt conditionally. Advanced patterns!

---

## 🎉 Congratulations!

You've mastered LCEL and chains!

**This is powerful** - you now know:
- How to build reusable AI workflows
- The elegant LCEL syntax
- How to compose components

**Every complex LangChain application** uses what you learned today.

---

**Ready for Day 4?** Navigate to tools folder:

```bash
cd ../day4_tools
cat README.md
```

---

**"Collaborative Learning - The Next Genesis Learning"**

*From prompts to chains. From chains to systems.* 🔥
