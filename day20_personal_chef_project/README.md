# Day 20: Personal Chef Project

**LangChain Academy - Module 1, Project 1.5**

## 📚 Complete Agent Project

This project combines everything from Module 1:
- ✅ Tools (@tool decorator + web_search)
- ✅ Memory (InMemorySaver + thread_id)
- ✅ System Prompt (chef personality)
- ✅ Agent (autonomous decision-making)

## 🗂️ Files

1. **personal_chef.py** - Complete personal chef agent

## 🎯 What It Does

1. User provides ingredients
2. Agent searches web for recipes
3. Agent suggests recipes
4. User asks for more details
5. Agent remembers conversation
6. Agent provides full instructions

## 🔥 Key Features

### Tools
```python
@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)
```

### System Prompt
```python
system_prompt = """
You are a personal chef. The user will give you a list of ingredients...
Using the web search tool, search the web for recipes...
"""
```

### Memory
```python
checkpointer = InMemorySaver()
config = {"configurable": {"thread_id": "chef_session_1"}}
```

### Complete Agent
```python
agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
    system_prompt=system_prompt,
    checkpointer=checkpointer
)
```

## 🚀 How to Run

```bash
cd /home/intruder/langchain_v1.1/day20_personal_chef_project
python personal_chef.py
```

## 📖 Learning Points

### Autonomous Behavior
- Agent decides when to search web
- Agent reads and understands results
- Agent formats clean responses
- Agent remembers conversation context

### Tool Execution Flow
```
User: "I have chicken and pasta"
→ Agent thinks: "I should search for recipes"
→ Agent calls: web_search("chicken pasta recipes")
→ Agent reads: Search results
→ Agent responds: "Here are 3 recipes..."
```

### Memory Flow
```
Turn 1: User provides ingredients
Turn 2: User asks "What about the second recipe?"
         Agent remembers previous recipes mentioned
Turn 3: User asks for instructions
         Agent remembers which recipe was selected
```

## 🎉 Module 1 Complete!

You've learned:
- Foundational models
- Prompting techniques
- Tools creation
- Web search integration
- Memory management
- Multimodal messages
- Complete agent projects

**Next:** Module 2 - Advanced Agents (MCP, Multi-Agent Systems)
