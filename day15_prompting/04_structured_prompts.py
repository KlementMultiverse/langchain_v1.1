"""
LangChain Academy - Module 1 - Lesson 1.1: Prompting
Structured prompts: Define exact output format in text
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage

# System prompt with structured output format
system_prompt = """
You are a science fiction writer, create a space capital city at the users request.

Please keep to the below structure.

Name: The name of the capital city

Location: Where it is based

Vibe: 2-3 words to describe its vibe

Economy: Main industries
"""

scifi_agent = create_agent(
    model="gpt-5-nano",
    system_prompt=system_prompt
)

question = HumanMessage(content="What's the capital of the moon?")

response = scifi_agent.invoke({"messages": [question]})

print(response['messages'][1].content)
