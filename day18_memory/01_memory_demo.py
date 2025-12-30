"""
LangChain Academy - Module 1 - Lesson 1.3: Memory
Using InMemorySaver for conversation memory
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver

# Create checkpointer (memory)
checkpointer = InMemorySaver()

# Create agent with memory
agent = create_agent(
    model="gpt-4o-mini",
    checkpointer=checkpointer
)

# Configuration with thread_id
config = {"configurable": {"thread_id": "user_123"}}

# First conversation turn
print("=== Turn 1 ===")
response = agent.invoke(
    {"messages": [HumanMessage(content="My name is Alice")]},
    config=config
)
print(response['messages'][-1].content)

# Second conversation turn (should remember Alice)
print("\n=== Turn 2 ===")
response = agent.invoke(
    {"messages": [HumanMessage(content="What's my name?")]},
    config=config
)
print(response['messages'][-1].content)

# Different thread_id (should NOT remember)
print("\n=== Turn 3 (Different Thread) ===")
config2 = {"configurable": {"thread_id": "user_456"}}
response = agent.invoke(
    {"messages": [HumanMessage(content="What's my name?")]},
    config2
)
print(response['messages'][-1].content)
