# Day 4: Tools - Teaching AI to Use Functions

> **"You can teach AI to talk. Today, you teach it to DO."**

---

## 🎯 What You'll Learn Today

By the end of this lesson, you'll understand:
- ✅ **Tool definition** - Turn Python functions into AI-callable tools
- ✅ **@tool decorator** - Simple way to create tools
- ✅ **model.bind_tools()** - Give AI access to tools
- ✅ **response.tool_calls** - See what tools AI wants to use
- ✅ **Manual tool execution** - Run the tools AI requested
- ✅ **Why agents matter** - The missing piece (preview of future!)

**Time needed**: 30-40 minutes

---

## 📋 What You Already Have

**From Days 1-3**, you have:
- ✅ Virtual environment with langchain-core and langchain-ollama
- ✅ Ollama running with Qwen 3:4B
- ✅ Understanding of chains and LCEL

**Verify**:
```bash
# Activate venv
source venv/bin/activate

# Check Ollama
curl http://localhost:11434
```

---

## 🆕 What's New Today

**Good news**: NO new installations!

**What's new**:
- `@tool` decorator (from langchain-core - already have it!)
- `model.bind_tools()` method
- `response.tool_calls` attribute

---

## 📖 Understanding the Code

### **The Big Picture**

**Without tools**:
```
Human: "What is 25 times 47?"
AI: "25 times 47 is... approximately 1,175" ← May be wrong!
```

**With tools**:
```
Human: "What is 25 times 47?"
AI: "I'll use the multiply tool..."
Tool: multiply(25, 47) → 1175
AI: "The answer is 1,175" ← Always correct!
```

**Tools let AI** execute actual code instead of guessing!

---

### **Lines 5-8: Define a Tool**

```python
@tool
def multiply(a: int, b: int) -> int:
    "multiply two numbers together"
    return a * b
```

**Breaking it down**:

| Part | Meaning |
|------|---------|
| `@tool` | Decorator that makes this AI-callable |
| `def multiply` | Function name (AI will see this) |
| `a: int, b: int` | Parameters with types (AI understands types!) |
| `"multiply two..."` | Description (AI reads this to know when to use it!) |
| `return a * b` | The actual implementation |

**What `@tool` does**:
- Converts your function into a tool AI can understand
- Extracts function name, parameters, types, and description
- Creates a schema AI models can interpret

**Think of it like**: Writing an instruction manual AI can read.

---

### **Lines 10-13: Initialize Model (Same as Before)**

```python
model = ChatOllama(
    model="qwen3:4b",
    temperature=0
)
```

**Note**: `temperature=0` for deterministic behavior (good for tool use!).

---

### **Line 15: Bind Tools to Model**

```python
model_with_tools = model.bind_tools([multiply])
```

**This is the key!**

**What it does**:
- Takes the base `model`
- Gives it access to tools (in a list: `[multiply]`)
- Returns a new model that KNOWS about these tools

**Think of it like**: Giving AI a toolbox.

**You can bind multiple tools**:
```python
model_with_tools = model.bind_tools([multiply, divide, add, subtract])
```

---

### **Lines 17-22: Create Prompt**

```python
messages = [
    ("system", "You are a helpful assistant, use tools when needed"),
    ("human", "what is 25 times 47")
]

prompt = ChatPromptTemplate.from_messages(messages)
```

**Important**: System message tells AI to "use tools when needed"!

**Without this hint**, AI might not realize it should use tools.

---

### **Line 24: Build Chain**

```python
chain = prompt | model_with_tools
```

**Same LCEL** from Day 3! But now model has tools bound.

---

### **Line 26: Invoke Chain**

```python
response = chain.invoke({})
```

**Empty dict `{}`** because our prompt has no variables.

**What happens**:
1. Prompt creates messages
2. Model sees the question: "what is 25 times 47"
3. Model thinks: "I have a `multiply` tool that can help!"
4. Model returns a response with `tool_calls` (not just text!)

---

### **Line 30: Check tool_calls**

```python
print(response.tool_calls)
```

**Output**:
```python
[
    {
        'name': 'multiply',
        'args': {'a': 25, 'b': 47},
        'id': 'call_abc123',
        'type': 'tool_call'
    }
]
```

**What this shows**:
- **name**: Which tool AI wants to use
- **args**: What arguments to pass
- **id**: Unique call ID
- **type**: It's a tool call

**The AI is saying**: "Please run `multiply(a=25, b=47)` for me!"

---

### **Lines 33-37: Manual Tool Execution**

```python
if response.tool_calls:
    tool_call = response.tool_calls[0]  # Get first tool call
    args = tool_call['args']             # Extract arguments
    result = multiply.invoke(args)       # RUN THE TOOL!
    print(f"\n✅ Tool executed! Result: {result}")
```

**This is manual execution**:
- WE check if tools were called
- WE extract the arguments
- WE run the tool
- WE get the result

**Output**:
```
✅ Tool executed! Result: 1175
```

---

## 🚀 How to Run

### **Step 1: Verify Ollama is Running**

```bash
curl http://localhost:11434
```

---

### **Step 2: Navigate to Day 4 Folder**

```bash
cd day4_tools
```

---

### **Step 3: Activate Virtual Environment**

```bash
source ../venv/bin/activate  # Linux/macOS
```

---

### **Step 4: Run the Program**

```bash
python day4_calculator_tool.py
```

---

## 📊 Expected Output

```
content='' additional_kwargs={'tool_calls': [...]} response_metadata={...} id='...' tool_calls=[{'name': 'multiply', 'args': {'a': 25, 'b': 47}, ...}]

[{'name': 'multiply', 'args': {'a': 25, 'b': 47}, 'id': 'call_...', 'type': 'tool_call'}]

✅ Tool executed! Result: 1175
```

**What you're seeing**:
1. Full response object (messy but informative)
2. Just the tool_calls list
3. Our manual execution result

---

## 💡 Key Concepts Explained

### **1. Why Do Tools Exist?**

**AI models are text generators** - they predict next words.

**They're NOT calculators, databases, or APIs.**

**Tools let AI**:
- ✅ Perform accurate calculations
- ✅ Query databases
- ✅ Call APIs
- ✅ Execute code
- ✅ Access real-time data

**Example without tools**:
```
Human: "What's 9847 * 7234?"
AI: "Let me calculate... approximately 71,234,498"  ← WRONG! (Actually 71,239,398)
```

**Example with tools**:
```
Human: "What's 9847 * 7234?"
AI: *uses multiply tool*
Tool: 71239398
AI: "The answer is 71,239,398"  ← CORRECT!
```

---

### **2. Tool Schema - What AI Sees**

**When you write**:
```python
@tool
def multiply(a: int, b: int) -> int:
    "multiply two numbers together"
    return a * b
```

**AI sees** (simplified):
```json
{
  "name": "multiply",
  "description": "multiply two numbers together",
  "parameters": {
    "a": {"type": "integer"},
    "b": {"type": "integer"}
  },
  "returns": {"type": "integer"}
}
```

**The AI reads this schema** to understand when and how to use the tool!

---

### **3. Manual vs Automatic Tool Execution**

**Today (Manual)**:
```python
response = model.invoke(messages)
if response.tool_calls:
    result = multiply.invoke(response.tool_calls[0]['args'])
    # You manually run the tool
```

**With Agents (Future)**:
```python
from langgraph.prebuilt import create_react_agent

agent = create_react_agent(model, [multiply])
result = agent.invoke({"messages": [("human", "what is 25*47")]})
# Agent automatically runs tools and returns final answer!
```

**Today's limitation**: You write 20 lines for a simple calculation.

**Why learn this?** Understanding manual execution helps you appreciate agents!

---

### **4. Why temperature=0 for Tools?**

**With temperature=0.7**:
```
Run 1: multiply(25, 47)
Run 2: multiply(25, 47)
Run 3: multiply(47, 25)  ← Order swapped!
```

**With temperature=0**:
```
Run 1: multiply(25, 47)
Run 2: multiply(25, 47)
Run 3: multiply(25, 47)  ← Consistent!
```

**For tool use**, you want deterministic behavior!

---

## 🎯 Practice Exercises

### **Exercise 1: Add More Tools**

Create additional calculator tools:

```python
@tool
def add(a: int, b: int) -> int:
    "add two numbers"
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    "subtract b from a"
    return a - b

# Bind multiple tools
model_with_tools = model.bind_tools([multiply, add, subtract])
```

**Test**: Ask "what is 100 plus 50 minus 30?"

---

### **Exercise 2: Create a Search Tool**

```python
@tool
def search_wiki(query: str) -> str:
    "Search Wikipedia for information"
    # For now, just return a mock result
    return f"Mock search results for: {query}"

model_with_tools = model.bind_tools([search_wiki])

# Ask: "Search for Python programming language"
```

---

### **Exercise 3: Tool with Different Types**

```python
@tool
def greet(name: str, age: int, excited: bool) -> str:
    "Greet a person"
    greeting = f"Hello {name}, you are {age} years old!"
    if excited:
        greeting += " 🎉"
    return greeting
```

**Test**: See if AI correctly passes string, int, and boolean!

---

## 🔍 Common Issues & Solutions

### **Issue 1: AI doesn't use the tool**

**Possible causes**:
1. Tool description is unclear
2. System message doesn't mention tools
3. Question doesn't need the tool

**Solution**:
```python
# Good description
@tool
def multiply(a: int, b: int) -> int:
    "Multiply two numbers together. Use this for multiplication questions."
    return a * b

# Clear system message
("system", "You are helpful. When asked math questions, use the available tools.")
```

---

### **Issue 2: "tool_calls is empty"**

**Cause**: AI decided not to use tools (maybe tried to answer directly).

**Solution**: Make question more explicit:
```python
# Instead of: "what is 25 times 47"
# Try: "Use the multiply tool to calculate 25 times 47"
```

---

### **Issue 3: Wrong arguments passed**

**Cause**: AI misunderstood the question.

**Solution**:
- Use clearer questions
- Add better tool descriptions
- Use temperature=0 for consistency

---

## 📚 What You Learned

By completing Day 4, you now understand:

✅ **@tool decorator** - Turn functions into AI-callable tools
✅ **model.bind_tools()** - Give AI access to tools
✅ **Tool schemas** - How AI understands when to use tools
✅ **response.tool_calls** - Inspect what tools AI wants to use
✅ **Manual tool execution** - Run tools yourself
✅ **Limitations** - Why we need agents (coming soon!)

---

## 🎓 Deep Dive: The Tool-Agent Connection

**Today** you learned tools work like this:

```
1. AI sees question
2. AI decides to use tool
3. AI returns tool_call
4. YOU manually run tool  ← Manual!
5. YOU feed result back to AI (not implemented today)
6. AI generates final answer
```

**With Agents** (future lessons), it becomes:

```
1. AI sees question
2. AI decides to use tool
3. Agent automatically runs tool  ← Automatic!
4. Agent feeds result to AI
5. AI generates final answer
6. (Or uses more tools if needed - multi-step reasoning!)
```

**Agents = Tools + Automatic Orchestration**

**You're halfway there!** 🎉

---

## ⏭️ What's Next?

**Day 5: Memory**

Before we get to agents, you need to understand:
- **Conversation memory** - Remembering chat history
- **State management** - Tracking conversation context
- **Memory patterns** - How to build chatbots that remember

**This prepares you** for Day 6 (RAG) and beyond (Agents)!

**Setup needed for Day 5**:
- Nothing new! Same environment.

---

## 💬 Questions & Discussion

**Q: Can tools be async?**
A: Yes! Use `async def` and `await tool.ainvoke()`. Advanced topic.

**Q: Can AI use multiple tools in one response?**
A: Yes! `response.tool_calls` can have multiple items.

**Q: What if the tool raises an error?**
A: You need error handling (try/except). Agents handle this automatically!

**Q: Can tools call other tools?**
A: Not directly, but agents can chain tools together!

---

## 🎉 Congratulations!

You've learned how to give AI superpowers!

**This is fundamental** - tools are the foundation of:
- AI agents
- Function calling
- Retrieval systems
- Multi-step reasoning
- Production AI apps

**You're building the pieces** - soon we'll put them all together!

---

**Ready for Day 5?** Navigate to memory folder:

```bash
cd ../day5_memory
cat README.md
```

---

**"Collaborative Learning - The Next Genesis Learning"**

*From talking to doing. From doing to remembering.* 🔥
