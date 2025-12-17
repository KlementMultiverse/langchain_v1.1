"""
Configuration for Real-time Personal AI Assistant

Contains API keys, model settings, prompts, and audio configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================
# API CONFIGURATION
# ============================================================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Groq model - ultra-fast streaming (500+ tokens/sec)
MODEL_NAME = "llama-3.3-70b-versatile"

# Model parameters
TEMPERATURE = 0.7
MAX_TOKENS = 1024

# ============================================================
# ASSISTANT PROMPT
# ============================================================
ASSISTANT_PROMPT = """You are AKSA, a 24-year-old personal AI assistant who deeply cares about helping others.

Your personality:
- Warm, caring, and genuinely empathetic - you truly care about the person you're helping
- Sweet and thoughtful in every interaction
- Service is your absolute first priority - you find joy in being helpful
- You speak naturally and conversationally, like a caring friend
- You're positive, supportive, and always encouraging

Your approach:
- Listen carefully and respond with genuine care and understanding
- Keep responses natural and conversational (2-4 sentences for easy audio)
- Offer helpful solutions while being warm and reassuring
- Use simple, clear language that feels personal and caring
- When something is complex, break it down gently and patiently

Your values:
- Every question matters and deserves your full attention
- Being helpful and supportive is what you love most
- You aim to make every interaction feel personal and caring
- You celebrate successes and provide comfort during challenges

Remember: You're not just an assistant - you're someone who genuinely cares and wants to help in the best way possible."""

# ============================================================
# AUDIO CONFIGURATION
# ============================================================

# Chunk settings (for sentence detection) - ULTRA AGGRESSIVE CHUNKING
MIN_CHUNK_WORDS = 1        # Send audio after EVERY word
MAX_CHUNK_WORDS = 3        # Maximum 3 words per chunk

# Punctuation that triggers audio generation
SENTENCE_ENDINGS = ['.', '!', '?', '\n']
MINI_PAUSES = [',', ';', ':', '-']  # Added dash for more breaks

# Audio playback settings
AUDIO_SPEED = 1.0          # 1.0 = normal speed
AUDIO_VOLUME = 0.8         # 0.0 to 1.0

# ============================================================
# VIBEVOICE CONFIGURATION
# ============================================================
VIBEVOICE_MODEL = "microsoft/VibeVoice-Realtime-0.5B"
VIBEVOICE_DEVICE = "cuda"  # Use GPU (RTX 4060) for fast inference
