# Day 12: Agents with LangChain 1.2

**Date**: December 23, 2025
**Focus**: Autonomous agents with tool calling and memory
**Tech Stack**: LangChain 1.2, Groq API, create_agent()

---

## 🎯 What You'll Learn

Agents are the pinnacle of LangChain - they combine:
- **LLM Brain**: Thinks and makes decisions
- **Tools**: Can perform actions (calculate, search, etc.)
- **Loop**: Automatically chains tools until task is complete
- **Memory**: Remembers conversation history

**Key Concept**: Unlike manual tool calling (Day 4), agents **decide autonomously** which tools to use and when!

---

## 📁 Programs

### **12_01_basic_agent.py** - Basic Agent with Tools
**Concepts**: Agent creation, tool calling, multi-step reasoning

**What it does**:
- Creates 3 tools: multiply, add, get_word_length
- Agent automatically decides which tool to use
- Handles multi-step tasks (e.g., "calculate 25 × 47, then add 100")

**Key Learning**: Agent = LLM + Tools + Autonomous Loop

```python
from langchain.agents import create_agent

agent = create_agent(
    model=model,
    tools=[multiply, add, get_word_length],
    system_prompt="You are a helpful assistant."
)

result = agent.invoke({"messages": [("user", "What is 25 times 47?")]})
```

**Output**:
```
🔧 Tool: multiply(25, 47)
✅ Answer: The result is 1,175
```

---

### **12_02_agent_with_memory.py** - Agent with Conversation Memory
**Concepts**: Agent + memory, context retention, multi-turn conversations

**What it does**:
- Agent remembers your name across turns
- References previous calculations ("add 50 to that result")
- Maintains conversation context
- Personalizes responses

**Key Learning**: Memory = Pass conversation_history list to agent

```python
conversation_history = []

# Turn 1
conversation_history.append(("user", "My name is Klement"))
result = agent.invoke({"messages": conversation_history})
conversation_history.append(("assistant", result['messages'][-1].content))

# Turn 2 - Agent remembers!
conversation_history.append(("user", "What's my name?"))
result = agent.invoke({"messages": conversation_history})
# Agent responds: "Your name is Klement"
```

**Output**:
```
Turn 1: "Hi! My name is Klement"
Agent: "Hello Klement! I've saved your name..."

Turn 2: "What's 15 times 8?"
Agent: "120, Klement" ← Uses your name!

Turn 3: "Add 50 to that result"
Agent: "120 + 50 = 170" ← Remembers 120!

Turn 4: "What's my name?"
Agent: "Klement" ← From Turn 1!
```

---

## 🔑 Key Concepts

### **1. What is an Agent?**
```
Regular LLM: Can only talk (answers from knowledge)
Agent: Can talk AND use tools (calculator, search, database, etc.)
```

**Example**:
- Question: "What's 25 × 47?"
- Regular LLM: Guesses (might be wrong)
- **Agent**: Uses multiply tool → Gets exact answer (1,175)

### **2. Agent Components**
```
Agent = LLM + Tools + Loop

- LLM: The "brain" that thinks
- Tools: The "hands" that perform actions
- Loop: The workflow that chains tools
```

### **3. ReAct Pattern** (Reason + Act)
```
1. REASON: Agent reads question, decides what to do
2. ACT: Agent calls appropriate tool
3. OBSERVE: Agent gets tool result
4. RESPOND: Agent answers user
```

### **4. Agent vs Manual Tool Calling**

**Day 4 (Manual)**:
```python
if "multiply" in question:
    result = multiply_tool.invoke(...)
```
**YOU** decide when to use tools.

**Day 12 (Agent)**:
```python
agent.invoke({"messages": [("user", question)]})
```
**AGENT** decides automatically!

### **5. Memory Pattern**
```python
# Memory = List of all messages
conversation_history = []

# Every turn:
conversation_history.append(("user", message))
result = agent.invoke({"messages": conversation_history})
conversation_history.append(("assistant", response))
```

---

## 🎓 Learning Progression

**Day 4**: Tools (manual calling)
↓
**Day 5**: Memory (conversation history)
↓
**Day 12**: **Agents** (autonomous tool use + memory)

---

## 🚀 Running the Programs

```bash
# Navigate to directory
cd /home/intruder/langchain_learning/examples

# Activate virtual environment
source ../venv_langchain_dec2025/bin/activate

# Run basic agent
export PYTHONPATH=/home/intruder/langchain_learning/examples:$PYTHONPATH
python day12_agents/12_01_basic_agent.py

# Run agent with memory
python day12_agents/12_02_agent_with_memory.py
```

---

## 📊 Expected Output

### Program 1: Basic Agent
- ✅ Multiply 25 × 47 = 1,175
- ✅ Multi-step: 25 × 47, then + 100 = 1,275
- ✅ Different tool: Word length of "LangChain" = 9

### Program 2: Agent with Memory
- ✅ Saves name "Klement"
- ✅ Uses name in responses
- ✅ References previous calculation
- ✅ Recalls name after 4 turns

---

## 🔥 Production Use Cases

**1. Customer Support Agent**
- Remembers customer info
- Searches knowledge base
- Calculates refunds/credits
- Multi-turn conversations

**2. Research Assistant**
- Searches documents (RAG)
- Performs calculations
- Cites sources
- Remembers context

**3. Data Analyst Agent**
- Queries databases
- Performs statistical calculations
- Generates visualizations
- Multi-step analysis

---

## 💡 Key Takeaways

1. **Agents are autonomous** - They decide which tools to use
2. **create_agent()** - One function handles everything
3. **Docstrings matter** - Agent reads them to decide when to use tools
4. **Memory is simple** - Just pass conversation_history list
5. **Multi-step works automatically** - Agent chains tools as needed

---

## 🎯 What's Next?

**Day 13**: Error Handling & Resilience
- Try/except patterns
- Retry mechanisms
- Graceful degradation
- Production error handling

---

## 📚 Resources

- **LangChain Agents Docs**: https://python.langchain.com/docs/modules/agents/
- **create_agent API**: https://python.langchain.com/api_reference/langchain/agents/
- **Groq API**: https://console.groq.com/

---

**Author**: Klement
**Repository**: https://github.com/KlementMultiverse/langchain_v1.1
**Learning Journey**: 3-Week LangChain Production Mastery
