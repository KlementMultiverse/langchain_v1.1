"""
LangChain Academy - Module 1 - Lesson 1.1: Prompting
Few-shot learning: Teaching AI by providing examples
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage

# System prompt with few-shot examples
system_prompt = """
You are a science fiction writer, create a space capital city at the users request.

User: What is the capital of mars?
Scifi Writer: Marsialis

User: What is the capital of Venus?
Scifi Writer: Venusovia
"""

scifi_agent = create_agent(
    model="gpt-4o-mini",
    system_prompt=system_prompt
)

question = HumanMessage(content="What's the capital of the moon?")

response = scifi_agent.invoke({"messages": [question]})

print(response['messages'][1].content)
