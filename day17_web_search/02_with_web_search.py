"""
LangChain Academy - Module 1 - Lesson 1.2: Web Search
AI with web search - real-time information
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from typing import Dict, Any
from tavily import TavilyClient
from pprint import pprint

# Initialize Tavily client
tavily_client = TavilyClient()

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

# Test tool directly
print("=== Testing Web Search Tool ===")
result = web_search.invoke("Who is the current mayor of San Francisco?")
pprint(result)

# Create agent with web search
agent = create_agent(
    model="gpt-4o-mini",
    tools=[web_search]
)

question = HumanMessage(content="Who is the current mayor of San Francisco?")

response = agent.invoke({"messages": [question]})

# Print final answer
print("\n=== AI Response ===")
print(response['messages'][-1].content)

# Print message flow
print("\n=== Message Flow ===")
for i, msg in enumerate(response['messages']):
    print(f"\n[{i}] {type(msg).__name__}")
    if hasattr(msg, 'content') and msg.content:
        print(f"Content: {msg.content[:200]}...")
