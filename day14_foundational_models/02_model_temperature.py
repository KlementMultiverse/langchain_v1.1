"""
LangChain Academy - Module 1 - Lesson 1.1: Foundational Models
Customizing model with temperature parameter
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

# Initialize model with custom temperature
# temperature=0.0 → predictable/deterministic
# temperature=1.0 → creative/random
model = init_chat_model(
    model="gpt-4o-mini",
    temperature=1.0  # More creative responses
)

response = model.invoke("What's the capital of the Moon?")
print(response.content)
