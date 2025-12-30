"""
LangChain Academy - Module 1 - Lesson 1.2: Tools
Using tools with agents
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5

# Create agent with tools
agent = create_agent(
    model="gpt-5-nano",
    tools=[square_root],
    system_prompt="You are an arithmetic wizard. Use your tools to calculate the square root and square of any number."
)

question = HumanMessage(content="What is the square root of 467?")

response = agent.invoke({"messages": [question]})

# Print AI's final answer
print("=== AI Response ===")
print(response['messages'][-1].content)

# Print full message flow to see tool call
print("\n=== Full Message Flow ===")
pprint(response['messages'])

# Print tool call details
print("\n=== Tool Call Details ===")
print(response["messages"][1].tool_calls)
