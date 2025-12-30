"""
LangChain Academy - Module 1 - Lesson 1.1: Foundational Models
Passing conversation history to agents
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage, AIMessage
from pprint import pprint

agent = create_agent("gpt-4o-mini")

# Simulate a conversation with history
response = agent.invoke({
    "messages": [
        HumanMessage(content="What's the capital of the Moon?"),
        AIMessage(content="The capital of the Moon is Luna City."),
        HumanMessage(content="Interesting, tell me more about Luna City")
    ]
})

print("=== AI Response ===")
print(response['messages'][-1].content)
