"""
Common Configuration for All LangChain Programs

Import this file to get consistent model settings across all programs.

Usage:
    from common_config import get_model

    model = get_model()  # Uses Groq by default
    response = model.invoke("Hello!")
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables from .env file
load_dotenv()

def get_model(temperature=0.7, model_name=None):
    """
    Get configured LLM model (Groq by default for better reliability)

    Args:
        temperature: Controls randomness (0.0 = deterministic, 1.0 = creative)
        model_name: Override default model

    Returns:
        ChatGroq instance ready to use
    """
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY not found in .env file!")

    # Use provided model or default
    model = model_name or os.getenv("DEFAULT_MODEL", "llama-3.3-70b-versatile")

    return ChatGroq(
        api_key=api_key,
        model=model,
        temperature=temperature
    )

# Quick test if run directly
if __name__ == "__main__":
    print("Testing common config...")
    model = get_model()
    response = model.invoke("Say: Config working!")
    print(f"✅ {response.content}")
