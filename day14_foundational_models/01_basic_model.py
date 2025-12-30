"""
LangChain Academy - Module 1 - Lesson 1.1: Foundational Models
Basic model initialization and invocation
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

# Initialize a chat model
model = init_chat_model(model="gpt-4o-mini")

# Invoke the model with a simple question
response = model.invoke("What's the capital of the Moon?")

# Print the response
print(response.content)

# Print response metadata (tokens, model info, etc.)
from pprint import pprint
print("\n=== Response Metadata ===")
pprint(response.response_metadata)
