"""
LangChain Academy - Module 1 - Project: Personal Chef
Complete agent combining tools + memory + system prompt
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from typing import Dict, Any
from tavily import TavilyClient

# Initialize Tavily
tavily_client = TavilyClient()

# Web search tool
@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

# System prompt defining chef personality
system_prompt = """
You are a personal chef. The user will give you a list of ingredients they have left over in their house.

Using the web search tool, search the web for recipes that can be made with the ingredients they have.

Return recipe suggestions and eventually the recipe instructions to the user, if requested.
"""

# Create agent with tools, memory, and system prompt
checkpointer = InMemorySaver()

agent = create_agent(
    model="gpt-5-nano",
    tools=[web_search],
    system_prompt=system_prompt,
    checkpointer=checkpointer
)

# Conversation configuration
config = {"configurable": {"thread_id": "chef_session_1"}}

# Interactive conversation
print("=== Personal Chef Agent ===")
print("Tell me what ingredients you have!\n")

# Example conversation
conversations = [
    "I have chicken, tomatoes, and pasta",
    "What about the second recipe?",
    "Can you give me the full instructions for that one?"
]

for user_input in conversations:
    print(f"User: {user_input}")

    response = agent.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )

    print(f"Chef: {response['messages'][-1].content}\n")
    print("-" * 80 + "\n")
