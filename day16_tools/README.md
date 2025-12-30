# Day 16: Tools

**LangChain Academy - Module 1, Lesson 1.2**

## 📚 What You'll Learn

- Create tools with `@tool` decorator
- Add tools to agents
- Understand tool execution flow
- See how AI decides when to use tools

## 🗂️ Files

1. **01_tool_definition.py** - Creating tools with @tool decorator
2. **02_tools_with_agents.py** - Using tools with agents

## 🎯 Key Concepts

### Tool Decorator
```python
@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5
```

**Key parts:**
- `@tool` - Converts function to AI-usable tool
- **Docstring** - AI's instruction manual (CRITICAL!)
- **Type hints** - Define parameter types
- **Return value** - What AI receives

### Tool Execution Flow
1. User asks question
2. AI reads available tools
3. AI decides which tool to call
4. Tool executes
5. AI reads result
6. AI responds to user

### Message Flow
```
HumanMessage → AIMessage(tool_call) → ToolMessage(result) → AIMessage(answer)
```

## 🚀 How to Run

```bash
cd /home/intruder/langchain_v1.1/day16_tools
python 01_tool_definition.py
python 02_tools_with_agents.py
```
