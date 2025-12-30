"""
LangChain Academy - Module 1 - Lesson 1.1: Prompting
Using system prompts to control agent behavior
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage

# Define system prompt to give agent a role
system_prompt = "You are a science fiction writer, create a capital city at the users request."

scifi_agent = create_agent(
    model="gpt-4o-mini",
    system_prompt=system_prompt
)

question = HumanMessage(content="What's the capital of the moon?")

response = scifi_agent.invoke({"messages": [question]})

print(response['messages'][1].content)
