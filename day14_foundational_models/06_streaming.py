"""
LangChain Academy - Module 1 - Lesson 1.1: Foundational Models
Streaming output word-by-word in real-time
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.messages import HumanMessage

agent = create_agent("gpt-4o-mini")

print("Streaming response:\n")

# Stream the response token by token
for token, metadata in agent.stream(
    {"messages": [HumanMessage(content="Tell me about the Moon in 2 sentences")]},
    stream_mode="messages"
):
    # Print each token as it arrives
    if token.content:
        print(token.content, end="", flush=True)

print("\n\nStreaming complete!")
