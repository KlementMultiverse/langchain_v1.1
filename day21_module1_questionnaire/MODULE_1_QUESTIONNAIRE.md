# MODULE 1 COMPREHENSIVE QUESTIONNAIRE
## LangChain Academy - Foundation to Mastery

**Total Questions:** 100
**Your Score:** 70/100 (Mastery Proven)
**Date:** December 28, 2025

---

# 📝 SECTION 1: IMPORTS & SETUP (10 Questions)

---

## Question 1: Load Environment Variables

**Task:** Write the import statement to load environment variables from a `.env` file.

**Answer:**
```python
from dotenv import load_dotenv
load_dotenv()
```

**Explanation:**
- Imports `load_dotenv` function from dotenv package
- Calls it to read `.env` file and load API keys into environment variables

---

## Question 2: Import Chat Model Function

**Task:** Write the import statement to create a chat model in LangChain.

**Answer:**
```python
from langchain.chat_models import init_chat_model
```

**Explanation:**
- Imports `init_chat_model` function
- Used to initialize models from multiple providers (OpenAI, Anthropic, Google, etc.)
- Module is `chat_models` (plural), not `models`

---

## Question 3: Import Agent Creator

**Task:** Write the import statement to create an agent.

**Answer:**
```python
from langchain.agents import create_agent
```

**Explanation:**
- Imports `create_agent` function from agents module
- Used to create agents with tools, memory, and system prompts
- Agents are more powerful than basic models

---

## Question 4: Import Message Classes

**Task:** Write the import statement to use HumanMessage and AIMessage classes.

**Answer:**
```python
from langchain.messages import HumanMessage, AIMessage
```

**Explanation:**
- `HumanMessage` - Represents user messages
- `AIMessage` - Represents AI responses
- Used for creating message objects in conversations

---

## Question 5: Import Tool Decorator

**Task:** Write the import statement to use the `@tool` decorator.

**Answer:**
```python
from langchain.tools import tool
```

**Explanation:**
- Imports the `@tool` decorator
- Used to convert Python functions into AI-usable tools
- Example: `@tool` above a function makes it available to agents

---

## Question 6: Import Type Hints

**Task:** Write the import statement for type hints (Dict, Any).

**Answer:**
```python
from typing import Dict, Any
```

**Explanation:**
- `Dict` - Type hint for dictionary (e.g., `Dict[str, Any]`)
- `Any` - Type hint for "any type"
- Used in function signatures: `def search(query: str) -> Dict[str, Any]:`

---

## Question 7: Import Tavily Client

**Task:** Write the import statement to use Tavily's web search client.

**Answer:**
```python
from tavily import TavilyClient
```

**Explanation:**
- Imports TavilyClient for web search functionality
- Create instance: `tavily_client = TavilyClient()`
- Automatically uses TAVILY_API_KEY from environment

---

## Question 8: Import Memory Saver

**Task:** Write the import statement to use InMemorySaver for agent memory.

**Answer:**
```python
from langgraph.checkpoint.memory import InMemorySaver
```

**Explanation:**
- Imports InMemorySaver for conversation memory (RAM-based)
- Used in agents: `checkpointer=InMemorySaver()`
- Note: It's from `langgraph` not `langchain`!

---

## Question 9: Import BaseModel

**Task:** Write the import statement to use Pydantic's BaseModel.

**Answer:**
```python
from pydantic import BaseModel
```

**Explanation:**
- Imports BaseModel for creating structured data schemas
- Used to define classes for structured outputs
- Enables `response_format=ClassName` in agents

---

## Question 10: Import Base64

**Task:** Write the import statement for base64 encoding.

**Answer:**
```python
import base64
```

**Explanation:**
- Python's built-in base64 module
- Used for multimodal: `base64.b64encode(image_bytes).decode("utf-8")`
- Converts binary data → text string for JSON APIs

---

# 🧠 SECTION 2: FOUNDATIONAL CONCEPTS (22 Questions)

---

## Question 11: Create Chat Model

**Task:** Create a simple chat model using `init_chat_model`.

**Answer:**
```python
model = init_chat_model(model="gpt-4o-mini")
```

**Explanation:**
- Creates a chat model instance using GPT-4o-mini
- Optional: Add `temperature=0.7` for creativity control
- 0 = deterministic, 1 = creative

---

## Question 12: Create HumanMessage

**Task:** Create a HumanMessage with content "What is AI?"

**Answer:**
```python
message = HumanMessage(content="What is AI?")
```

**Explanation:**
- Creates HumanMessage object representing user input
- `content` parameter holds the message text
- Used with `model.invoke(message)` or in agent message lists

---

## Question 13: Invoke Model

**Task:** Send a message to a model and get response.

**Answer:**
```python
response = model.invoke(message)
```

**Explanation:**
- For MODELS (not agents): Direct message parameter
- Returns response object with AI's answer
- Access content with: `response.content`

---

## Question 14: Print Response Content

**Task:** Print only the content (text) from the AI's response.

**Answer:**
```python
print(response.content)
```

**Explanation:**
- Accesses `.content` attribute of response
- Gets just the text message from AI
- Note: Use `.content` not `['content']`

---

## Question 15: Create Agent

**Task:** Create an agent with model "gpt-4o-mini".

**Answer:**
```python
agent = create_agent(model="gpt-4o-mini")
```

**Explanation:**
- Creates agent (not just model)
- Basic agent with no tools, memory, or system prompt
- Can add: `tools=[]`, `system_prompt=""`, `checkpointer=`

---

## Question 16: Invoke Agent

**Task:** Invoke agent with message "Hello".

**Answer:**
```python
response = agent.invoke({"messages": [HumanMessage(content="Hello")]})
```

**Explanation:**
- For AGENTS: Dictionary with "messages" key (plural!)
- Value is a list of message objects
- Different from model.invoke() syntax

---

## Question 17: Print Agent Response

**Task:** Print the AI's response from an agent.

**Answer:**
```python
print(response["messages"][-1].content)
```

**Explanation:**
- `response["messages"]` - accesses messages list
- `[-1]` - gets LAST message (AI's final response)
- `.content` - extracts text content

---

## Question 18: Model vs Agent Syntax

**Task:** Explain the difference between model.invoke() and agent.invoke().

**Answer:**
- **Model:** `model.invoke(message)` - Direct message parameter
- **Agent:** `agent.invoke({"messages": [message]})` - Dictionary with messages list

**Explanation:**
- Models process single messages
- Agents accept conversation history (list of messages)
- Agents support multi-turn conversations

---

## Question 19: Streaming

**Task:** Use streaming to get real-time word-by-word output.

**Answer:**
```python
for token, metadata in agent.stream(
    {"messages": [HumanMessage(content="Tell me a short story")]},
    stream_mode="messages"
):
    if token.content:
        print(token.content, end="", flush=True)
```

**Explanation:**
- `stream_mode="messages"` is parameter of `.stream()` method
- `end=""` prevents newlines
- `flush=True` shows text immediately
- `if token.content` checks for content before printing

---

## Question 20: Access Metadata

**Task:** Access token usage metadata from response.

**Answer:**
```python
print(response.response_metadata)
```

**Explanation:**
- Shows token_usage (prompt/completion tokens)
- Model name, finish reason, system fingerprint
- Useful for cost tracking and debugging

---

## Question 21: Pretty Print

**Task:** Pretty print a response object.

**Answer:**
```python
from pprint import pprint
pprint(response)
```

**Explanation:**
- `pprint` = "Pretty Print"
- Formats nested dictionaries with indentation
- Much better than regular print() for complex data

---

## Question 22: List Indexing

**Task:** Explain difference between `[1]` and `[-1]`.

**Answer:**
- `response['messages'][1]` - Second message (index 1)
- `response['messages'][-1]` - Last message (always)

**Explanation:**
- `[1]` only works with exactly 2+ messages
- `[-1]` is production-safe - always gets last message
- Use `[-1]` in real applications

---

## Question 23-32: Additional Foundational Questions

**Question 23:** What does temperature control?
**Answer:** Creativity level (0=deterministic, 1=creative)

**Question 24:** What's the difference between a model and an agent?
**Answer:** Model = AI brain only. Agent = AI + tools + memory + system prompt

**Question 25:** How do you access the first message in response?
**Answer:** `response['messages'][0]`

**Question 26:** What does `finish_reason` tell you?
**Answer:** Why the response ended (e.g., "stop", "length", "tool_calls")

**Question 27:** What are tokens?
**Answer:** Units of text (~0.75 words). What you pay for in API calls.

**Question 28:** What's the purpose of `flush=True` in streaming?
**Answer:** Forces immediate output display (doesn't wait for buffer)

**Question 29:** Can you use streaming with models or just agents?
**Answer:** Both! `model.stream()` and `agent.stream()` both work

**Question 30:** What does `additional_kwargs` contain?
**Answer:** Extra metadata like refusal reasons, audio tokens, etc.

**Question 31:** How do you calculate total tokens?
**Answer:** `prompt_tokens + completion_tokens = total_tokens`

**Question 32:** What's `system_fingerprint` used for?
**Answer:** Identifies exact model version for reproducibility

---

# 🎯 SECTION 3: SYSTEM PROMPTS (10 Questions)

---

## Question 33: Simple System Prompt

**Task:** Create a system prompt that makes AI act as a pirate.

**Answer:**
```python
system_prompt = """
You are a pirate. Talk like a pirate in all responses.
Use pirate language and expressions.
"""
```

**Explanation:**
- Uses triple quotes for multi-line strings
- Defines AI's role and behavior
- Clear instructions for personality

---

## Question 34: Agent with System Prompt

**Task:** Create agent with pirate system prompt.

**Answer:**
```python
agent = create_agent(
    model="gpt-4o-mini",
    system_prompt=system_prompt
)
```

**Explanation:**
- `system_prompt` parameter sets AI personality
- Agent will now respond as a pirate
- Combines model + personality

---

## Question 35: Few-Shot Examples

**Task:** Create system prompt with few-shot examples for sci-fi planet capitals.

**Answer:**
```python
system_prompt = """
You are a sci-fi writer creating fictional planet capitals.

Examples:
User: What is the capital of Venus?
AI: Venusekia

User: What is the capital of Mars?
AI: Marsekia
"""
```

**Explanation:**
- Shows AI the pattern through examples
- AI learns naming convention
- Will create similar names for other planets

---

## Question 36: Pydantic BaseModel

**Task:** Define BaseModel for structured output (CityInfo).

**Answer:**
```python
from pydantic import BaseModel

class CityInfo(BaseModel):
    name: str
    population: int
    country: str
```

**Explanation:**
- Creates data schema class
- Three typed fields
- Used with `response_format=CityInfo`

---

## Question 37: Agent with Structured Output

**Task:** Create agent that returns structured CityInfo.

**Answer:**
```python
agent = create_agent(
    model="gpt-4o-mini",
    response_format=CityInfo
)
```

**Explanation:**
- `response_format` enforces schema
- AI output validated against CityInfo fields
- Access: `response['structured_response'].name`

---

## Question 38: Access Structured Response

**Task:** Print the `name` field from structured response.

**Answer:**
```python
print(response['structured_response'].name)
```

**Explanation:**
- `response['structured_response']` gets Pydantic object
- `.name` accesses field from model
- Type-safe, validated data

---

## Question 39: Structured Prompt (Text)

**Task:** Create structured prompt for text formatting.

**Answer:**
```python
system_prompt = """
Follow this exact format:

Name: <city name>
Population: <number>
Country: <country>

No more, no less.
"""
```

**Explanation:**
- Text-based formatting instructions
- AI tries to follow format (not guaranteed)
- Less reliable than Pydantic BaseModel

---

## Question 40: Difference - Structured Prompt vs BaseModel

**Task:** What's the difference?

**Answer:**
- **Structured prompt:** AI tries to follow text format (not enforced)
- **BaseModel:** AI output is validated and enforced
- **Production:** Use BaseModel for reliability

---

## Question 41-42: Additional System Prompt Questions

**Question 41:** Can you combine system_prompt + response_format?
**Answer:** Yes! `create_agent(model="...", system_prompt="...", response_format=Class)`

**Question 42:** Do system prompts work with models or just agents?
**Answer:** Both! Models and agents both support system prompts.

---

# 🔧 SECTION 4: TOOLS (15 Questions)

---

## Question 43: Define Simple Tool

**Task:** Define tool that calculates square of a number.

**Answer:**
```python
from langchain.tools import tool

@tool
def square(x: float) -> float:
    """Calculates the square of a number"""
    return x * x
```

**Explanation:**
- `@tool` decorator makes function AI-usable
- Type hints: `x: float -> float`
- Docstring is CRITICAL - AI reads it to understand tool

---

## Question 44: Agent with Tool

**Task:** Create agent with square tool.

**Answer:**
```python
agent = create_agent(
    model="gpt-4o-mini",
    tools=[square]
)
```

**Explanation:**
- `tools` parameter takes a list
- Agent can now autonomously use square tool
- Can have multiple tools: `tools=[square, add, multiply]`

---

## Question 45: Invoke Agent with Tool

**Task:** Ask agent to calculate square of 7.

**Answer:**
```python
response = agent.invoke({
    "messages": [HumanMessage(content="What is the square of 7?")]
})
print(response['messages'][-1].content)
```

**Explanation:**
- Agent decides to use square tool
- Calls `square(7)` autonomously
- Returns formatted answer: "49"

---

## Question 46: Tool with Two Parameters

**Task:** Define tool that adds two numbers.

**Answer:**
```python
@tool
def add(x: float, y: float) -> float:
    """Adds two numbers"""
    return x + y
```

**Explanation:**
- Two parameters with type hints
- Docstring explains function
- Agent can call: `add(5, 3)`

---

## Question 47: Multiple Tools

**Task:** Create agent with add, multiply, divide tools.

**Answer:**
```python
@tool
def add(x: float, y: float) -> float:
    """Adds two numbers"""
    return x + y

@tool
def multiply(x: float, y: float) -> float:
    """Multiplies two numbers"""
    return x * y

@tool
def divide(x: float, y: float) -> float:
    """Divides two numbers"""
    if y == 0:
        return 0
    return x / y

agent = create_agent(
    model="gpt-4o-mini",
    tools=[add, multiply, divide]
)
```

**Explanation:**
- Three separate tools
- Agent can use all three
- Handles division by zero

---

## Question 48: Docstring Purpose

**Task:** What does the docstring do in a tool?

**Answer:**
The docstring tells the AI what the function does. AI reads it to decide when to call the tool.

**Explanation:**
- AI's instruction manual for the tool
- Clear docstring = AI uses tool correctly
- Without docstring = AI won't know when to use it

---

## Question 49: No Docstring Consequence

**Task:** What happens without a docstring?

**Answer:**
AI doesn't know what the tool does, so it won't use it. Tool exists but is never called.

**Explanation:**
- No description = blind to AI
- Tool is useless without docstring
- Always include clear docstrings

---

## Question 50: Web Search Tool

**Task:** Create web search tool using Tavily.

**Answer:**
```python
from tavily import TavilyClient
from typing import Dict, Any

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)
```

**Explanation:**
- TavilyClient() uses TAVILY_API_KEY from env
- Returns dictionary with search results
- `Dict[str, Any]` = flexible return type

---

## Question 51: Tool Execution Flow

**Task:** Explain the flow when agent uses a tool.

**Answer:**
1. User asks question
2. AI analyzes question and system prompt
3. AI decides to use tool
4. AI calls tool with parameters
5. Tool executes and returns result (ToolMessage)
6. AI reads result and formulates answer
7. AI responds to user

**Explanation:**
- Autonomous decision-making
- Can call multiple tools sequentially
- Each tool call creates ToolMessage

---

## Question 52: Sequential vs Parallel Tools

**Task:** What's the difference?

**Answer:**
- **Sequential:** Output of one tool needed as input for another (dependencies)
- **Parallel:** Multiple independent tools run simultaneously (no dependencies)

**Example:**
- Sequential: Calculate `10 + (5 * 8)` - multiply first, then add
- Parallel: Square of 5 AND cube of 3 - independent operations

---

## Question 53-57: Additional Tool Questions

**Question 53:** Can tools call other tools?
**Answer:** No. Only the AI agent can call tools. Tools execute independently.

**Question 54:** What if a tool returns wrong data?
**Answer:** AI uses it anyway - no validation layer. Validate inside tool function.

**Question 55:** Can you have tools without system_prompt?
**Answer:** Yes, but system_prompt helps AI know when to use tools.

**Question 56:** How many tools can an agent have?
**Answer:** Unlimited, but too many confuses AI. Keep it focused (3-10 tools ideal).

**Question 57:** Can tools access external APIs?
**Answer:** Yes! That's the point. Web search, databases, APIs - anything Python can do.

---

# 🌐 SECTION 5: WEB SEARCH (10 Questions)

---

## Question 58: Why Dict[str, Any]?

**Task:** Explain return type `Dict[str, Any]` for web_search.

**Answer:**
- `Dict` = dictionary
- `str` = keys are strings
- `Any` = values can be ANY type (str, list, None, float, etc.)

**Explanation:**
Web search returns unpredictable structure:
```python
{
    "query": "...",        # str
    "results": [...],      # list
    "answer": "...",       # str
    "response_time": 1.2   # float
}
```

---

## Question 59: Complete Personal Chef

**Task:** Build complete Personal Chef agent.

**Answer:**
```python
from langchain.agents import create_agent
from tavily import TavilyClient
from langgraph.checkpoint.memory import InMemorySaver
from langchain.tools import tool
from typing import Dict, Any

tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

system_prompt = """
You are a personal chef. The user will give you leftover ingredients.
Search the web for recipes using those ingredients.
Return recipe suggestions and instructions if requested.
"""

chef_agent = create_agent(
    model='gpt-4o-mini',
    tools=[web_search],
    system_prompt=system_prompt,
    checkpointer=InMemorySaver()
)
```

**Explanation:**
- Web search tool
- Chef personality
- Memory for conversation
- Complete production pattern

---

## Question 60-67: Additional Web Search Questions

**Question 60:** How does AI know when to search web?
**Answer:** AI reads docstring and decides based on question type.

**Question 61:** Can you search multiple times in one query?
**Answer:** Yes! AI can make multiple tool calls sequentially.

**Question 62:** Does AI read search results?
**Answer:** Yes! AI processes JSON and extracts relevant information.

**Question 63:** What's Tavily vs DuckDuckGo?
**Answer:** Tavily = Paid, fast, LLM-optimized. DuckDuckGo = Free, slower.

**Question 64:** How many free Tavily searches?
**Answer:** 1000 searches/month on free tier.

**Question 65:** Can you combine web search + structured output?
**Answer:** Yes! `response_format` + `tools=[web_search]` works together.

**Question 66:** What if web search fails?
**Answer:** AI gets error message, can tell user or try alternative.

**Question 67:** Can tools search specific websites?
**Answer:** Yes, modify search query: `f"site:reddit.com {query}"`

---

# 💾 SECTION 6: MEMORY (10 Questions)

---

## Question 68: Thread ID Purpose

**Task:** Explain what thread_id is used for.

**Answer:**
Thread ID tracks a conversation and identifies a user/session. Same thread_id = shared context. Different thread_id = isolated conversations.

**Explanation:**
```python
# User A
config_a = {"configurable": {"thread_id": "user_123"}}

# User B
config_b = {"configurable": {"thread_id": "user_456"}}

# Conversations are separate
```

---

## Question 69: Create Config

**Task:** Create config with thread_id "session_42".

**Answer:**
```python
config = {"configurable": {"thread_id": "session_42"}}
```

**Explanation:**
- Nested dictionary structure
- Used in: `agent.invoke({...}, config)`
- Conversation saved under "session_42"

---

## Question 70: Two Users Same Agent

**Task:** Show two separate conversations with same agent.

**Answer:**
```python
config_UserA = {"configurable": {"thread_id": "User_A"}}
config_UserB = {"configurable": {"thread_id": "User_B"}}

response_A = agent.invoke(
    {"messages": [HumanMessage(content="My name is Alice")]},
    config_UserA
)

response_B = agent.invoke(
    {"messages": [HumanMessage(content="My name is Bob")]},
    config_UserB
)
```

**Explanation:**
- Two configs = two isolated conversations
- User A asks "What's my name?" → "Alice"
- User B asks "What's my name?" → "Bob"

---

## Question 71: InMemorySaver vs Database

**Task:** What's the difference?

**Answer:**

| Feature | InMemorySaver | PostgreSQL/DB |
|---------|---------------|---------------|
| Storage | RAM | Database |
| Speed | Fast | Slower |
| Persistence | Lost on restart | Survives restarts |
| Scalability | Single server | Multiple servers |
| Production | Dev/test only | Production ready |

**Explanation:**
- InMemorySaver = Learning/testing
- Database = Real applications

---

## Question 72: Continue Conversation

**Task:** Send follow-up message using same thread_id.

**Answer:**
```python
config = {"configurable": {"thread_id": "chat_1"}}

# First message
response_1 = agent.invoke(
    {"messages": [HumanMessage(content="My name is Alice")]},
    config
)

# Follow-up - same config!
response_2 = agent.invoke(
    {"messages": [HumanMessage(content="What did I just tell you?")]},
    config
)
# Agent responds: "You told me your name is Alice"
```

**Explanation:**
- Same thread_id = agent remembers
- Loads previous history automatically

---

## Question 73: No Config Consequence

**Task:** What happens without config?

**Answer:**
Agent works but has no memory. Each invoke is isolated. Agent has amnesia between calls.

**Explanation:**
```python
# No config
agent.invoke({"messages": [HumanMessage(content="My name is Alice")]})
agent.invoke({"messages": [HumanMessage(content="What's my name?")]})
# Agent: "I don't know your name" ❌
```

---

## Question 74: Import InMemorySaver

**Task:** Import InMemorySaver.

**Answer:**
```python
from langgraph.checkpoint.memory import InMemorySaver
```

**Explanation:**
- From `langgraph` not `langchain`
- Used: `checkpointer=InMemorySaver()`

---

## Question 75-77: Additional Memory Questions

**Question 75:** Can you change thread_id mid-conversation?
**Answer:** Yes, but starts new conversation context.

**Question 76:** Are thread_ids encrypted?
**Answer:** No, just strings. Don't use sensitive data as thread_id.

**Question 77:** Can multiple agents share same checkpointer?
**Answer:** Yes! Same InMemorySaver instance can be shared.

---

# 🎨 SECTION 7: MULTIMODAL MESSAGES (15 Questions)

---

## Question 78: Two Text Inputs

**Task:** Create HumanMessage with two text pieces.

**Answer:**
```python
message = HumanMessage(content=[
    {"type": "text", "text": "What's in this image?"},
    {"type": "text", "text": "Be specific about colors"}
])
```

**Explanation:**
- Content is a LIST of dictionaries
- Multiple instructions in one message
- Both texts sent together

---

## Question 79: Add Image

**Task:** Create multimodal message with text + image.

**Answer:**
```python
message = HumanMessage(content=[
    {"type": "text", "text": "What's in this image?"},
    {"type": "image", "base64": img_b64, "mime_type": "image/png"}
])
```

**Explanation:**
- Image as second dictionary
- `base64` field contains encoded image
- `mime_type` specifies format

---

## Question 80: Bytes to Base64

**Task:** Convert image bytes to base64 string.

**Answer:**
```python
img_b64 = base64.b64encode(img_bytes).decode("utf-8")
```

**Explanation:**
- `b64encode()` converts bytes → base64 bytes
- `.decode("utf-8")` converts → string
- Result: text-safe for JSON

---

## Question 81: Image Upload Flow

**Task:** Complete flow from upload to base64.

**Answer:**
```python
from ipywidgets import FileUpload
from IPython.display import display
import base64

uploader = FileUpload(accept=".png", multiple=False)
display(uploader)

# After user uploads
uploaded_file = uploader.value[0]
content_mv = uploaded_file["content"]
img_bytes = bytes(content_mv)
img_b64 = base64.b64encode(img_bytes).decode("utf-8")
```

**Explanation:**
1. Create upload widget
2. Get first uploaded file `[0]`
3. Extract content (memoryview)
4. Convert to bytes
5. Encode to base64

---

## Question 82: Text + Image + Audio

**Task:** Create message with all three modalities.

**Answer:**
```python
message = HumanMessage(content=[
    {"type": "text", "text": "Analyze this data"},
    {"type": "image", "base64": img_b64, "mime_type": "image/png"},
    {"type": "audio", "base64": aud_b64, "mime_type": "audio/wav"}
])
```

**Explanation:**
- Three pieces of content in ONE message
- AI processes all together for complete context
- True multimodal processing

---

## Question 83: Audio Model

**Task:** Which model supports audio input?

**Answer:**
`gpt-4o-audio-preview` - Supports text + image + audio

**Explanation:**
- `gpt-4o-mini` - Text + image only (NO audio)
- `gpt-4o-audio-preview` - Full multimodal support

---

## Question 84: Record Audio

**Task:** Record 3 seconds of audio to WAV in memory.

**Answer:**
```python
import sounddevice as sd
import io
from scipy.io.wavfile import write

duration = 3
sample_rate = 44100

# Record
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()

# To WAV in memory
buf = io.BytesIO()
write(buf, sample_rate, audio)
wav_bytes = buf.getvalue()
```

**Explanation:**
- Records 3 seconds mono audio
- Writes to BytesIO (RAM, not disk)
- Gets WAV bytes for encoding

---

## Question 85: BytesIO Purpose

**Task:** What is BytesIO and why use it?

**Answer:**
BytesIO creates a virtual file in RAM (not disk). Used for temporary storage.

**Benefits:**
- Faster (RAM vs disk)
- Cleaner (no file management)
- No disk space used
- Automatic cleanup

---

## Question 86: Channels Meaning

**Task:** What does `channels=1` mean?

**Answer:**
- `channels=1` → Mono (single audio channel)
- `channels=2` → Stereo (left + right channels)

**Explanation:**
Mono is sufficient for LLM voice input. Smaller file size.

---

## Question 87: Sample Rate

**Task:** What does `sample_rate=44100` mean?

**Answer:**
44,100 measurements per second. CD quality audio standard.

**Calculation:**
- 5 seconds × 44,100 = 220,500 samples

---

## Question 88: Send Audio to Agent

**Task:** Send audio to AI agent.

**Answer:**
```python
response = agent.invoke({
    "messages": [HumanMessage(content=[
        {"type": "text", "text": "Describe what you hear"},
        {"type": "audio", "base64": aud_b64, "mime_type": "audio/wav"}
    ])]
})
```

**Explanation:**
- Text instruction + audio data
- AI transcribes and analyzes audio
- Returns description/transcription

---

## Question 89: Why Base64?

**Task:** Why use base64 encoding?

**Answer:**
Converts binary data (bytes) → text string for JSON API compatibility.

**Flow:**
```
Binary (bytes) → base64.b64encode() → base64 bytes → .decode("utf-8") → string → JSON ✅
```

**Explanation:**
- APIs don't accept raw binary
- Base64 = binary-to-text conversion

---

## Question 90: Model Comparison

**Task:** Difference between gpt-4o-mini and gpt-4o-audio-preview?

**Answer:**

| Model | Text | Image | Audio | Cost |
|-------|------|-------|-------|------|
| gpt-4o-mini | ✅ | ✅ | ❌ | Cheaper |
| gpt-4o-audio-preview | ✅ | ✅ | ✅ | More expensive |

---

## Question 91: Image Dictionary Structure

**Task:** Show complete image content structure.

**Answer:**
```python
{
    "type": "image",
    "base64": img_b64,
    "mime_type": "image/png"  # or "image/jpeg", etc.
}
```

**Explanation:**
- `type` identifies data type
- `base64` contains encoded image
- `mime_type` specifies format

---

## Question 92: Model Error Troubleshooting

**Task:** Error: "Model does not support audio input". Fix?

**Answer:**
Change model to `gpt-4o-audio-preview`:

```python
agent = create_agent(model='gpt-4o-audio-preview')
```

**Explanation:**
Model capabilities must match input types.

---

# 🚀 SECTION 8: INTEGRATION (38 Questions)

## Questions 93-100: Completed in Test (Questions 66-70)

**Question 93:** Build complete agent with all features
**Question 94:** Two-turn conversation with memory
**Question 95:** Personal Chef with structured output
**Question 96:** Access structured recipe data
**Question 97:** Build multimodal image agent

---

## Questions 71-100: BONUS QUESTIONS (Not tested, but important!)

---

## Question 98: Debug Broken Code

**Task:** What's wrong with this code?

```python
agent = create_agent(
    model='gpt-4o-mini',
    tools=web_search,  # Bug here
    system_prompt="You are helpful"
)
```

**Answer:**
`tools` must be a LIST: `tools=[web_search]`

---

## Question 99: Choose Right Model

**Task:** User wants text + image analysis. Which model?

**Answer:**
`gpt-4o-mini` - Cheaper, supports text + image

---

## Question 100: Production Checklist

**Task:** What to change for production?

**Answer:**
1. InMemorySaver → PostgreSQL checkpointer
2. Add error handling
3. Add logging
4. Add rate limiting
5. Secure API keys (environment variables)
6. Add input validation
7. Monitor costs
8. Add authentication

---

# 🎓 ADDITIONAL INTEGRATION SCENARIOS

---

## Question 101: Multi-User System

**Task:** Handle 1000 concurrent users.

**Answer:**
```python
# Production setup
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver(
    connection_string="postgresql://user:pass@localhost/db"
)

agent = create_agent(
    model='gpt-4o-mini',
    checkpointer=checkpointer
)

# Each user gets unique thread_id
user_config = {"configurable": {"thread_id": f"user_{user_id}"}}
```

**Explanation:**
- Database handles concurrent access
- Each user isolated by thread_id
- Scales horizontally

---

## Question 102: Cost Optimization

**Task:** Reduce API costs.

**Answer:**
1. Use `gpt-4o-mini` instead of `gpt-4`
2. Cache common responses
3. Limit conversation history length
4. Use streaming to stop early if needed
5. Implement user rate limits

---

## Question 103: Error Handling

**Task:** Handle API failures gracefully.

**Answer:**
```python
try:
    response = agent.invoke({"messages": [message]}, config)
except Exception as e:
    # Log error
    logger.error(f"Agent error: {e}")
    # Return fallback response
    return "I'm experiencing technical difficulties. Please try again."
```

---

## Question 104: Tool Validation

**Task:** Validate tool outputs before AI uses them.

**Answer:**
```python
@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web"""
    try:
        result = tavily_client.search(query)
        # Validate result structure
        if "results" not in result:
            return {"error": "Invalid search results"}
        return result
    except Exception as e:
        return {"error": str(e)}
```

---

## Question 105: Conversation History Limit

**Task:** Limit conversation to last 10 messages.

**Answer:**
```python
# Get conversation history
state = checkpointer.get(config)
messages = state["messages"]

# Keep only last 10
if len(messages) > 10:
    messages = messages[-10:]

# Continue with limited history
response = agent.invoke({"messages": messages}, config)
```

---

## Question 106: Structured + Tools + Memory

**Task:** Combine all three features.

**Answer:**
```python
from pydantic import BaseModel

class RecipeOutput(BaseModel):
    recipe_name: str
    ingredients: list[str]
    cook_time: int

agent = create_agent(
    model='gpt-4o-mini',
    tools=[web_search],
    system_prompt="You are a chef",
    response_format=RecipeOutput,
    checkpointer=InMemorySaver()
)
```

**Explanation:**
- Searches web for recipes
- Returns structured data
- Remembers conversation

---

## Question 107: Dynamic Tool Selection

**Task:** Give agent different tools based on user role.

**Answer:**
```python
def create_user_agent(user_role):
    if user_role == "admin":
        tools = [web_search, delete_data, create_user]
    else:
        tools = [web_search]

    return create_agent(
        model='gpt-4o-mini',
        tools=tools,
        system_prompt=f"You are a {user_role} assistant"
    )
```

---

## Question 108: Streaming with Progress

**Task:** Show progress while agent thinks.

**Answer:**
```python
print("Thinking...", end="", flush=True)
for i, (token, _) in enumerate(agent.stream(..., stream_mode="messages")):
    if i % 10 == 0:
        print(".", end="", flush=True)
    if token.content:
        print(f"\n{token.content}", end="", flush=True)
```

---

## Question 109: Multimodal + Memory

**Task:** Image analysis with conversation history.

**Answer:**
```python
config = {"configurable": {"thread_id": "image_session"}}

# First image
response1 = agent.invoke({
    "messages": [HumanMessage(content=[
        {"type": "text", "text": "What's in this image?"},
        {"type": "image", "base64": img1_b64, "mime_type": "image/png"}
    ])]
}, config)

# Compare with second image - agent remembers first!
response2 = agent.invoke({
    "messages": [HumanMessage(content=[
        {"type": "text", "text": "How does this compare to the previous image?"},
        {"type": "image", "base64": img2_b64, "mime_type": "image/png"}
    ])]
}, config)
```

---

## Question 110: Conditional System Prompts

**Task:** Change personality based on time of day.

**Answer:**
```python
from datetime import datetime

hour = datetime.now().hour

if 5 <= hour < 12:
    system_prompt = "You are a cheerful morning assistant"
elif 12 <= hour < 17:
    system_prompt = "You are a professional afternoon assistant"
else:
    system_prompt = "You are a relaxed evening assistant"

agent = create_agent(model='gpt-4o-mini', system_prompt=system_prompt)
```

---

## Question 111: Tool Chaining

**Task:** Force tools to run in sequence.

**Answer:**
```python
system_prompt = """
To answer user questions:
1. ALWAYS search web first
2. THEN analyze results
3. FINALLY format response

Use tools in this exact order.
"""
```

---

## Question 112: Parallel Tool Execution

**Task:** Call multiple tools simultaneously.

**Answer:**
AI does this automatically! Ask: "What's the square of 5 and cube of 3?"

Agent calls both tools in parallel if they're independent.

---

## Question 113: Custom Tool Errors

**Task:** Return helpful error messages.

**Answer:**
```python
@tool
def divide(x: float, y: float) -> str:
    """Divide two numbers"""
    if y == 0:
        return "Error: Cannot divide by zero. Please provide a non-zero divisor."
    return str(x / y)
```

---

## Question 114: Rate Limiting Users

**Task:** Limit user to 10 requests per minute.

**Answer:**
```python
from collections import defaultdict
from datetime import datetime, timedelta

user_requests = defaultdict(list)

def check_rate_limit(user_id):
    now = datetime.now()
    minute_ago = now - timedelta(minutes=1)

    # Remove old requests
    user_requests[user_id] = [
        t for t in user_requests[user_id] if t > minute_ago
    ]

    # Check limit
    if len(user_requests[user_id]) >= 10:
        return False

    user_requests[user_id].append(now)
    return True
```

---

## Question 115: Logging Agent Activity

**Task:** Log all agent interactions.

**Answer:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Before invoke
logger.info(f"User {user_id}: {message.content}")

response = agent.invoke({"messages": [message]}, config)

# After invoke
logger.info(f"Agent response: {response['messages'][-1].content}")
logger.info(f"Tokens used: {response.get('usage', {})}")
```

---

## Question 116: Fallback Models

**Task:** Try GPT-4o-mini, fallback to GPT-3.5 if it fails.

**Answer:**
```python
def invoke_with_fallback(message, config):
    try:
        agent = create_agent(model='gpt-4o-mini', ...)
        return agent.invoke({"messages": [message]}, config)
    except Exception as e:
        logger.warning(f"GPT-4o-mini failed: {e}, trying GPT-3.5")
        agent = create_agent(model='gpt-3.5-turbo', ...)
        return agent.invoke({"messages": [message]}, config)
```

---

## Question 117: Token Usage Tracking

**Task:** Track cumulative token usage per user.

**Answer:**
```python
user_tokens = defaultdict(int)

response = agent.invoke({"messages": [message]}, config)

# Track tokens
tokens_used = response['messages'][-1].usage_metadata['total_tokens']
user_tokens[user_id] += tokens_used

print(f"User {user_id} total tokens: {user_tokens[user_id]}")
```

---

## Question 118: Timeout Handling

**Task:** Timeout agent after 30 seconds.

**Answer:**
```python
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Agent took too long")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 second timeout

try:
    response = agent.invoke({"messages": [message]}, config)
    signal.alarm(0)  # Cancel timeout
except TimeoutError:
    return "Request timed out. Please try a simpler question."
```

---

## Question 119: Caching Responses

**Task:** Cache common questions.

**Answer:**
```python
import hashlib
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(question_hash):
    # This will be cached
    return agent.invoke({
        "messages": [HumanMessage(content=question)]
    }, config)

# Usage
question_hash = hashlib.md5(question.encode()).hexdigest()
response = get_cached_response(question_hash)
```

---

## Question 120: Detect Tool Abuse

**Task:** Detect if user is spamming tool calls.

**Answer:**
```python
response = agent.invoke({"messages": [message]}, config)

# Count tool calls
tool_calls = sum(
    1 for msg in response['messages']
    if hasattr(msg, 'tool_calls') and msg.tool_calls
)

if tool_calls > 10:
    logger.warning(f"User {user_id} triggered {tool_calls} tool calls")
    # Take action: rate limit, notify admin, etc.
```

---

## Question 121: Multi-Language Support

**Task:** Detect language and respond accordingly.

**Answer:**
```python
from langdetect import detect

user_message = "Bonjour, comment allez-vous?"
language = detect(user_message)

system_prompt = f"You are a helpful assistant. Respond in {language}."

agent = create_agent(model='gpt-4o-mini', system_prompt=system_prompt)
```

---

## Question 122: Sentiment Analysis

**Task:** Adjust tone based on user sentiment.

**Answer:**
```python
# Simplified sentiment detection
def detect_sentiment(text):
    negative_words = ['angry', 'frustrated', 'hate', 'terrible']
    if any(word in text.lower() for word in negative_words):
        return "negative"
    return "neutral"

sentiment = detect_sentiment(user_message)

if sentiment == "negative":
    system_prompt = "You are an empathetic, calming assistant"
else:
    system_prompt = "You are a helpful assistant"
```

---

## Question 123: A/B Testing

**Task:** Test two different system prompts.

**Answer:**
```python
import random

# 50/50 split
if random.random() < 0.5:
    system_prompt = "You are a professional assistant"  # Version A
    version = "A"
else:
    system_prompt = "You are a friendly assistant"  # Version B
    version = "B"

agent = create_agent(model='gpt-4o-mini', system_prompt=system_prompt)

# Log which version
logger.info(f"User {user_id} got version {version}")
```

---

## Question 124: Context Window Management

**Task:** Prevent context window overflow.

**Answer:**
```python
MAX_TOKENS = 8000  # Model limit

def truncate_history(messages):
    total_tokens = sum(len(m.content.split()) * 1.3 for m in messages)

    while total_tokens > MAX_TOKENS and len(messages) > 1:
        messages.pop(0)  # Remove oldest
        total_tokens = sum(len(m.content.split()) * 1.3 for m in messages)

    return messages
```

---

## Question 125: Webhook Integration

**Task:** Send agent response to webhook.

**Answer:**
```python
import requests

response = agent.invoke({"messages": [message]}, config)

# Send to webhook
webhook_url = "https://your-webhook.com/endpoint"
requests.post(webhook_url, json={
    "user_id": user_id,
    "question": message.content,
    "response": response['messages'][-1].content,
    "timestamp": datetime.now().isoformat()
})
```

---

## Question 126: Database Logging

**Task:** Save all conversations to database.

**Answer:**
```python
import sqlite3

conn = sqlite3.connect('conversations.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    message TEXT,
    response TEXT,
    timestamp DATETIME
)
''')

# After agent response
cursor.execute('''
INSERT INTO conversations (user_id, message, response, timestamp)
VALUES (?, ?, ?, ?)
''', (user_id, message.content, response['messages'][-1].content, datetime.now()))

conn.commit()
```

---

## Question 127: User Preferences

**Task:** Remember user preferences across sessions.

**Answer:**
```python
user_preferences = {
    "user_123": {"tone": "formal", "language": "en"},
    "user_456": {"tone": "casual", "language": "es"}
}

prefs = user_preferences.get(user_id, {"tone": "neutral", "language": "en"})

system_prompt = f"""
You are a {prefs['tone']} assistant.
Respond in {prefs['language']}.
"""

agent = create_agent(model='gpt-4o-mini', system_prompt=system_prompt)
```

---

## Question 128: Monitoring Costs

**Task:** Alert if costs exceed budget.

**Answer:**
```python
COST_PER_1K_TOKENS = 0.0015  # gpt-4o-mini pricing
DAILY_BUDGET = 10.00  # $10/day

daily_cost = 0

response = agent.invoke({"messages": [message]}, config)

tokens = response['messages'][-1].usage_metadata['total_tokens']
cost = (tokens / 1000) * COST_PER_1K_TOKENS
daily_cost += cost

if daily_cost > DAILY_BUDGET:
    logger.error(f"Daily budget exceeded: ${daily_cost:.2f}")
    # Take action: stop service, notify admin, etc.
```

---

## Question 129: Structured Logging

**Task:** Log in JSON format for analysis.

**Answer:**
```python
import json

log_entry = {
    "timestamp": datetime.now().isoformat(),
    "user_id": user_id,
    "thread_id": config["configurable"]["thread_id"],
    "message": message.content,
    "response": response['messages'][-1].content,
    "tokens": response['messages'][-1].usage_metadata,
    "model": "gpt-4o-mini"
}

logger.info(json.dumps(log_entry))
```

---

## Question 130: Health Check Endpoint

**Task:** Create health check for agent service.

**Answer:**
```python
def health_check():
    try:
        # Test simple query
        test_agent = create_agent(model='gpt-4o-mini')
        response = test_agent.invoke({
            "messages": [HumanMessage(content="test")]
        })
        return {"status": "healthy", "model": "gpt-4o-mini"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

# 🎓 FINAL SUMMARY

## What You've Mastered:

### ✅ **Core Skills:**
1. All LangChain imports memorized
2. Create models and agents from scratch
3. Build and attach tools
4. Implement memory systems
5. Handle multimodal inputs
6. Combine all features

### ✅ **Production Patterns:**
1. Error handling
2. Logging and monitoring
3. Cost optimization
4. User management
5. Rate limiting
6. Caching strategies

### ✅ **Integration Knowledge:**
1. Tools + Memory + System Prompts
2. Structured outputs + Web search
3. Multimodal + Memory
4. Database checkpointers
5. Production deployment

---

## 📊 Your Test Results:

- **Questions Completed:** 70/100
- **Mastery Level:** Expert
- **Ready for:** Module 2

---

## 🚀 Next Steps:

1. **Module 2:** MCP, Multi-agent systems, Advanced context
2. **Module 3:** Production deployment, HITL, Dynamic agents
3. **Projects:** Wedding Planner, Email Assistant

---

**You're ready to build production AI agents!** 💪

Save this document for quick reference anytime! 🎓
