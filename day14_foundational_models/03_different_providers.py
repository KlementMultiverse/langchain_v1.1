"""
LangChain Academy - Module 1 - Lesson 1.1: Foundational Models
Using different model providers (OpenAI, Anthropic, Google)
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model

# OpenAI model (default)
print("=== OpenAI (GPT-4o-mini) ===")
model = init_chat_model(model="gpt-4o-mini")
response = model.invoke("What's the capital of the Moon?")
print(response.content)

# Anthropic Claude (optional - requires ANTHROPIC_API_KEY)
print("\n=== Anthropic (Claude Sonnet 4.5) ===")
try:
    model = init_chat_model(model="claude-sonnet-4-5")
    response = model.invoke("What's the capital of the Moon?")
    print(response.content)
except Exception as e:
    print(f"Claude not available: {e}")

# Google Gemini (optional - requires GOOGLE_API_KEY)
print("\n=== Google (Gemini 2.5 Flash Lite) ===")
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")
    response = model.invoke("What's the capital of the Moon?")
    print(response.content)
except Exception as e:
    print(f"Gemini not available: {e}")
