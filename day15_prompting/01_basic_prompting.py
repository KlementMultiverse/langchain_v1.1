"""
LangChain Academy - Module 1 - Lesson 1.1: Prompting
Basic prompting without system prompt
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage

# Agent without system prompt
agent = create_agent(model="gpt-4o-mini")

question = HumanMessage(content="What's the capital of the moon?")

response = agent.invoke({"messages": [question]})

print(response['messages'][1].content)
