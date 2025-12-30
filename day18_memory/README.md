# Day 18: Memory

**LangChain Academy - Module 1, Lesson 1.3**

## 📚 What You'll Learn

- Problem: Agents have amnesia between calls
- Solution: InMemorySaver checkpointer
- thread_id for conversation isolation
- Production vs development memory

## 🗂️ Files

1. **01_memory_demo.py** - Using InMemorySaver for conversation memory

## 🎯 Key Concepts

### The Amnesia Problem
```python
agent.invoke({"messages": [HumanMessage("My name is Alice")]})
agent.invoke({"messages": [HumanMessage("What's my name?")]})
# AI doesn't remember! Each invoke() is isolated
```

### Solution: Checkpointer
```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
agent = create_agent(model="gpt-4o-mini", checkpointer=checkpointer)

config = {"configurable": {"thread_id": "user_123"}}
agent.invoke({"messages": [...]}, config=config)
```

### thread_id
- Conversation identifier
- Same thread_id = shared memory
- Different thread_id = isolated conversations
- Like different chat sessions

### InMemorySaver vs Production
- **InMemorySaver**: RAM-based, lost on restart (development only)
- **PostgreSQLSaver**: Database-based, persistent (production)
- **RedisSaver**: Fast cache-based, scalable (production)

### Architecture
```
User Input
→ Agent Processing
→ checkpointer.save(thread_id, state)
→ [InMemory: RAM] or [PostgreSQL: Database]
```

## 🚀 How to Run

```bash
cd /home/intruder/langchain_v1.1/day18_memory
python 01_memory_demo.py
```

## ⚠️ Important
InMemorySaver is NOT production-ready!
- Lost on restart
- Not scalable
- Single-process only

Use PostgreSQL/Redis for production.
