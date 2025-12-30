"""
LangChain Academy - Module 1 - Lesson 1.2: Web Search
AI without web search - outdated knowledge
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage

# Agent without web search
agent = create_agent(model="gpt-4o-mini")

question = HumanMessage(content="How up to date is your training knowledge?")

response = agent.invoke({"messages": [question]})

print(response['messages'][-1].content)
