# Day 22: Model Context Protocol (MCP)

**Module 2, Lesson 1 - LangChain Academy Foundations**

---

## 🧠 What is MCP? (The Big Picture)

Imagine you have a super smart AI assistant (like an LLM), but it's locked in a room with no phone, no internet, no tools. It can think, but it can't **DO** anything.

**MCP (Model Context Protocol)** is like giving your AI assistant:
- 📞 A phone to call external services
- 🔧 Tools to perform actions
- 📚 Access to documents and resources
- 📝 Pre-written scripts (prompts) to follow

**In simple terms**: MCP is a **standardized way** for AI agents to connect to external tools, data sources, and services.

---

## 📂 Files in This Lesson

### **File 1: `resources/mcp_server.py`** (THE SERVER - The Toolbox)
- **What it is**: A Python file that **provides tools/resources** to the AI
- **Think of it as**: A toolbox full of tools that the AI can borrow

### **File 2: `mcp_client.ipynb`** (THE CLIENT - The AI Agent)
- **What it is**: A Jupyter notebook where the AI **uses those tools**
- **Think of it as**: The AI agent that connects to the toolbox and uses the tools

---

## 🔧 Part 1: The MCP Server (`resources/mcp_server.py`)

### What Does the Server Do?

The server provides **3 types of capabilities**:

1. **TOOLS**: Actions the AI can perform (like searching the web)
2. **RESOURCES**: Data/documents the AI can read (like GitHub files)
3. **PROMPTS**: Instructions that tell the AI how to behave

### Breaking Down the Server Code

#### Step 1: Import Libraries

```python
from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from typing import Dict, Any
from requests import get
```

**What's happening**:
- `load_dotenv()`: Loads API keys from `.env` file
- `FastMCP`: Framework for creating MCP servers
- `TavilyClient`: Web search API (like Google but for AI)
- `requests.get`: To fetch data from URLs

#### Step 2: Create the MCP Server

```python
mcp = FastMCP("mcp_server")
tavily_client = TavilyClient()
```

**What's happening**:
- Creates a new MCP server named "mcp_server"
- Initializes Tavily for web searching

#### Step 3: Define a TOOL (Web Search)

```python
@mcp.tool()
def search_web(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    results = tavily_client.search(query)
    return results
```

**Breaking it down**:
- `@mcp.tool()`: Decorator that tells MCP "this is a TOOL"
- `search_web(query)`: Function that takes a search query
- `tavily_client.search(query)`: Actually searches the web
- `return results`: Returns search results

**In human terms**:
When the AI wants to search the internet, it calls this function!

#### Step 4: Define a RESOURCE (GitHub File)

```python
@mcp.resource("github://langchain-ai/langchain-mcp-adapters/blob/main/README.md")
def github_file():
    """Resource for accessing langchain-ai/langchain-mcp-adapters/README.md file"""
    url = "https://raw.githubusercontent.com/langchain-ai/langchain-mcp-adapters/blob/main/README.md"
    try:
        resp = get(url)
        return resp.text
    except Exception as e:
        return f"Error: {str(e)}"
```

**Breaking it down**:
- `@mcp.resource(...)`: Tells MCP "this is a RESOURCE (document)"
- `get(url)`: Fetches the README file from GitHub
- `return resp.text`: Returns the content

**What's the difference between TOOL and RESOURCE?**
- **TOOL**: An action the AI can **perform** (like search_web)
- **RESOURCE**: Data/documents the AI can **read** (like a README)

#### Step 5: Define a PROMPT (AI Instructions)

```python
@mcp.prompt()
def prompt():
    """Analyze data from a langchain-ai repo file with comprehensive insights"""
    return """
    You are a helpful assistant that answers user questions about LangChain, LangGraph and LangSmith.

    You can use the following tools/resources to answer user questions:
    - search_web: Search the web for information
    - github_file: Access the langchain-ai repo files

    If the user asks a question that is not related to LangChain, LangGraph or LangSmith,
    you should say "I'm sorry, I can only answer questions about LangChain, LangGraph and LangSmith."

    You may try multiple tool and resource calls to answer the user's question.
    You may also ask clarifying questions to the user to better understand their question.
    """
```

**What this does**: Defines instructions (a system prompt) for the AI agent

**Think of it as**: A rulebook the AI follows

#### Step 6: Run the Server

```python
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**What this does**:
- Starts the MCP server when you run the file
- `transport="stdio"`: Communicates via standard input/output (command line)

---

## 🤖 Part 2: The MCP Client (`mcp_client.ipynb`)

### What Does the Client Do?

The client:
1. Connects to the MCP server
2. Gets tools/resources/prompts from the server
3. Creates an AI agent with those capabilities
4. Sends questions to the agent

### Breaking Down the Client Code

#### Cell 1: Load Environment Variables

```python
from dotenv import load_dotenv
load_dotenv()
```

Loads your API keys (OPENAI_API_KEY, TAVILY_API_KEY, etc.)

#### Cell 2: Create MCP Client (Connect to Server)

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "local_server": {
            "transport": "stdio",
            "command": "python",
            "args": ["resources/mcp_server.py"],
        }
    }
)
```

**🔥 This is the magic**:

- `MultiServerMCPClient`: A client that connects to MCP servers
- `"local_server"`: Name of the server (you can name it anything)
- `"transport": "stdio"`: How to communicate (standard input/output)
- `"command": "python"`: What program to run
- `"args": ["resources/mcp_server.py"]`: Which file to run

**What's happening behind the scenes?**

The client launches the server like this:
```bash
python resources/mcp_server.py
```

#### Cell 3: Get Tools, Resources, and Prompts

```python
# Get tools from the server
tools = await client.get_tools()

# Get resources from the server
resources = await client.get_resources("local_server")

# Get prompts from the server
prompt = await client.get_prompt("local_server", "prompt")
prompt = prompt[0].content
```

**Breaking it down**:

1. `tools = await client.get_tools()`
   - Asks server: "What tools do you have?"
   - Server responds: "I have `search_web`!"

2. `resources = await client.get_resources("local_server")`
   - Asks server: "What resources do you have?"
   - Server responds: "I have `github_file`!"

3. `prompt = await client.get_prompt("local_server", "prompt")`
   - Asks server: "Give me the prompt"
   - Server responds with the instructions

**Why `await`?**
- These operations take time (server needs to respond)
- `await` means: "Wait for the server to respond"
- This is **asynchronous programming**

#### Cell 4: Create an Agent

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-5-nano",
    tools=tools,
    system_prompt=prompt
)
```

**Breaking it down**:

- `create_agent()`: Creates an AI agent
- `model="gpt-5-nano"`: Which AI model to use (cheap, fast OpenAI model)
- `tools=tools`: Give the agent the tools from the server
- `system_prompt=prompt`: Give the agent instructions

**What just happened?**

You created an AI agent that:
- Uses GPT-5-nano as its brain
- Has access to `search_web` tool
- Follows instructions from the server

#### Cell 5: Ask the Agent a Question

```python
from langchain.messages import HumanMessage

config = {"configurable": {"thread_id": "1"}}

response = await agent.ainvoke(
    {"messages": [HumanMessage(content="Tell me about the langchain-mcp-adapters library")]},
    config=config
)
```

**Breaking it down**:

- `HumanMessage(...)`: Your question to the AI
- `config`: Configuration (thread_id for conversation tracking)
- `await agent.ainvoke(...)`: Send the message and wait for response

**What happens when you run this?**

1. ✅ Agent receives your question
2. ✅ Reads the prompt (instructions)
3. ✅ Realizes it can use `github_file` resource
4. ✅ Fetches README from GitHub
5. ✅ Uses GPT-5-nano to generate an answer
6. ✅ Returns the response

#### Cell 6: Print the Response

```python
from pprint import pprint
pprint(response)
```

Pretty-prints the agent's response (`pprint` = "pretty print")

---

## 🌐 Part 3: Online MCP Server Example

The notebook also shows how to connect to an **online** MCP server (instead of a local file):

```python
client = MultiServerMCPClient(
    {
        "time": {
            "transport": "stdio",
            "command": "uvx",
            "args": [
                "mcp-server-time",
                "--local-timezone=America/New_York"
            ]
        }
    }
)

tools = await client.get_tools()
```

**What's different?**

- `"command": "uvx"`: Tool that downloads and runs packages instantly
- `"args": ["mcp-server-time", ...]`: Pre-built MCP server from the internet
- It provides time-related tools (like "get_current_time")

Then you create an agent and ask:

```python
agent = create_agent(model="gpt-5-nano", tools=tools)

response = await agent.ainvoke(
    {"messages": [HumanMessage(content="What time is it?")]}
)
```

The agent will use the time tool to get the current time!

---

## 🎨 How They Work Together

```
┌─────────────────────────────────────────────────────────────┐
│                    YOUR JUPYTER NOTEBOOK                     │
│                     (mcp_client.ipynb)                      │
│                                                             │
│  Step 1: Create MCP Client                                 │
│  Step 2: Launch Server (python resources/mcp_server.py)    │
│  Step 3: Get Tools, Resources, Prompts                     │
│  Step 4: Create Agent                                      │
│  Step 5: Ask Question                                      │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ Communication via stdio
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              MCP SERVER (resources/mcp_server.py)           │
│                                                             │
│  TOOLS:      - search_web(query)                           │
│  RESOURCES:  - github_file() → README.md                   │
│  PROMPTS:    - Instructions for the AI                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Execution Flow (When You Ask a Question)

1. **YOU**: "Tell me about langchain-mcp-adapters"
2. **CLIENT**: Sends message to Agent
3. **AGENT**: "I need to look this up..."
   - Checks available tools/resources
   - Decides to use "github_file" resource
4. **CLIENT**: Calls server → "Give me github_file resource"
5. **SERVER**: Fetches README from GitHub
6. **SERVER**: Returns README content to client
7. **AGENT**: Receives README content
   - Sends README + question to GPT-5-nano
8. **GPT-5-nano**: Generates answer based on README
9. **AGENT**: Returns final answer to you
10. **YOU**: See the response!

---

## 📋 Key Concepts Summary

### 1. MCP Server (resources/mcp_server.py)
- Provides capabilities to AI agents
- Can provide:
  - **TOOLS**: Actions the AI can perform
  - **RESOURCES**: Data the AI can read
  - **PROMPTS**: Instructions for the AI

### 2. MCP Client (mcp_client.ipynb)
- Connects to one or more MCP servers
- Gets tools/resources/prompts from servers
- Creates an AI agent with those capabilities
- Sends questions to the agent

### 3. Local vs Online Servers
- **LOCAL**: Your own Python file (like `mcp_server.py`)
- **ONLINE**: Pre-built servers from internet (like `mcp-server-time`)

### 4. Key Terms
- **`@mcp.tool()`**: Decorator to define a tool
- **`@mcp.resource()`**: Decorator to define a resource
- **`@mcp.prompt()`**: Decorator to define a prompt
- **`MultiServerMCPClient`**: Client that connects to servers
- **`create_agent()`**: Creates an AI agent with tools
- **`ainvoke()`**: Sends a message to the agent (async)
- **`await`**: Waits for async operations to complete

---

## 🚀 Installation & Setup

### Prerequisites

```bash
# Make sure you're in the langchain_v1.1 virtual environment
cd /home/intruder/langchain_learning
source venv_langchain_dec2025/bin/activate
```

### Install Required Packages

```bash
pip install langchain-mcp-adapters
pip install fastmcp
pip install tavily-python
pip install requests
```

### Setup .env File

Make sure your `.env` file has:

```bash
OPENAI_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

---

## 📖 How to Run

### Step 1: Start Jupyter

```bash
cd /home/intruder/langchain_v1.1/day22_mcp_model_context_protocol
jupyter notebook
```

### Step 2: Open the Notebook

Open `mcp_client.ipynb`

### Step 3: Run the Cells

Run each cell sequentially and observe the output!

---

## 🎯 Practice Exercises

1. **What would happen if you removed the `search_web` tool from the server?**
   - The agent wouldn't be able to search the web!

2. **How would you add a NEW tool to the server (like "get_weather")?**
   ```python
   @mcp.tool()
   def get_weather(city: str) -> str:
       """Get weather for a city"""
       # Your weather API logic here
       return f"Weather in {city}: Sunny, 75°F"
   ```

3. **Can one client connect to BOTH local and online servers at the same time?**
   - YES! That's what "MultiServerMCPClient" is for:
   ```python
   client = MultiServerMCPClient({
       "local_server": {...},
       "time_server": {...}
   })
   ```

---

## 🔗 Related Resources

- [MCP Official Docs](https://modelcontextprotocol.io/)
- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Tavily Search API](https://tavily.com)

---

## 🎓 What's Next?

In **Day 23 (Module 2, Lesson 2)**, we'll learn about:
- **Runtime Context**: How to pass context to agents
- **State Management**: How agents maintain state across conversations

---

**Happy Learning! 🚀**
