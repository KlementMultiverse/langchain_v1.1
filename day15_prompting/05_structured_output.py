"""
LangChain Academy - Module 1 - Lesson 1.1: Prompting
Structured output: Use Pydantic to get Python objects instead of text
PRODUCTION PATTERN - Most reliable way to get structured data
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pydantic import BaseModel

# Define output structure using Pydantic
class CapitalInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economy: str

# Create agent with response_format
agent = create_agent(
    model='gpt-5-nano',
    system_prompt="You are a science fiction writer, create a capital city at the users request.",
    response_format=CapitalInfo  # AI will return CapitalInfo object
)

question = HumanMessage(content="What is the capital of The Moon?")

response = agent.invoke({"messages": [question]})

# Get structured response as Python object
capital_info = response["structured_response"]

print(f"Name: {capital_info.name}")
print(f"Location: {capital_info.location}")
print(f"Vibe: {capital_info.vibe}")
print(f"Economy: {capital_info.economy}")

# Can access as attributes
print(f"\n{capital_info.name} is a city located at {capital_info.location}")
