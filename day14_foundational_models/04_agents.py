"""
LangChain Academy - Module 1 - Lesson 1.1: Foundational Models
Creating and using agents instead of models directly
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

# Create an agent (can use model name directly)
agent = create_agent("gpt-4o-mini")

# Invoke with HumanMessage
response = agent.invoke(
    {"messages": [HumanMessage(content="What's the capital of the Moon?")]}
)

# Print full response
print("=== Full Response ===")
pprint(response)

# Print just the AI's message content
print("\n=== AI Response Content ===")
print(response['messages'][-1].content)
