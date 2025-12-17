"""
  Day 8 - Program 2: Callback Handlers

  Track LLM events (start, tokens, end, timing) - foundation of observability!
"""

from langchain_ollama import ChatOllama
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List
import time

print("=" * 70)
print("CALLBACK HANDLERS - Track Everything!")
print("=" * 70)

# ============================================================
# CALLBACK 1: Simple Event Tracker
# ============================================================
class SimpleCallback(BaseCallbackHandler):
    """Prints when LLM starts and ends"""

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        print("\n🚀 LLM STARTED!")
        print(f"Prompt: '{prompts[0][:50]}...'")

    def on_llm_end(self, response, **kwargs):
        print("\n✅ LLM FINISHED!")

# ============================================================
# CALLBACK 2: Token Counter
# ============================================================
class TokenCounterCallback(BaseCallbackHandler):
    """Counts tokens generated during streaming"""

    def __init__(self):
        self.token_count = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        self.token_count = 0  # Reset counter

    def on_llm_new_token(self, token: str, **kwargs):
        self.token_count += 1

    def on_llm_end(self, response, **kwargs):
        print(f"\n📊 Total tokens generated: {self.token_count}")

# ============================================================
# CALLBACK 3: Timer Callback
# ============================================================
class TimerCallback(BaseCallbackHandler):
    """Measures LLM execution time"""

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        self.start_time = time.time()
        print(f"\n⏱️  Started at: {time.strftime('%H:%M:%S', time.localtime(self.start_time))}")

    def on_llm_end(self, response, **kwargs):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"⏱️  Ended at: {time.strftime('%H:%M:%S', time.localtime(self.end_time))}")
        print(f"⏱️  Duration: {duration:.2f} seconds")

# ============================================================
# CALLBACK 4: Complete Observability (Production-Like)
# ============================================================
class ObservabilityCallback(BaseCallbackHandler):
    """Combines all tracking (like LangSmith!)"""

    def __init__(self):
        self.start_time = None
        self.token_count = 0
        self.prompts = []
        self.responses = []

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        self.start_time = time.time()
        self.token_count = 0
        self.prompts = prompts
        print("\n" + "=" * 70)
        print("📋 LLM EXECUTION LOG")
        print("=" * 70)
        print(f"🔹 Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Get model name - works for all LLM providers
        model_name = (
            serialized.get('kwargs', {}).get('model') or
            serialized.get('name', 'unknown')
        )
        print(f"🔹 Model: {model_name}")
        print(f"🔹 Input: '{prompts[0][:60]}...'")

    def on_llm_new_token(self, token: str, **kwargs):
        self.token_count += 1

    def on_llm_end(self, response, **kwargs):
        duration = time.time() - self.start_time
        output = response.generations[0][0].text[:100]

        print(f"\n🔹 Response: '{output}...'")
        print(f"🔹 Tokens: {self.token_count}")
        print(f"🔹 Duration: {duration:.2f}s")
        print(f"🔹 Speed: {self.token_count/duration:.1f} tokens/sec")
        print("=" * 70)

    def on_llm_error(self, error: Exception, **kwargs):
        print(f"\n❌ ERROR: {error}")

# ============================================================
# EXAMPLES: Testing All Callbacks
# ============================================================

# Create model
model = ChatOllama(model="qwen3:4b", temperature=0.7)

# EXAMPLE 1: Simple Callback
print("\n" + "=" * 70)
print("EXAMPLE 1: Simple Event Tracking")
print("=" * 70)

simple_cb = SimpleCallback()
response = model.invoke(
    "Say: Hello World!",
    config={"callbacks": [simple_cb]}
)
print(f"Response: {response.content}")

# EXAMPLE 2: Token Counter with Streaming
print("\n" + "=" * 70)
print("EXAMPLE 2: Token Counting")
print("=" * 70)

token_cb = TokenCounterCallback()
print("\nStreaming response: ", end="", flush=True)
for chunk in model.stream(
    "Count from 1 to 5",
    config={"callbacks": [token_cb]}
):
    print(chunk.content, end="", flush=True)
print()  # New line after streaming

# EXAMPLE 3: Timer Callback
print("\n" + "=" * 70)
print("EXAMPLE 3: Performance Timing")
print("=" * 70)

timer_cb = TimerCallback()
response = model.invoke(
    "Write one sentence about Python",
    config={"callbacks": [timer_cb]}
)
print(f"\nResponse: {response.content}")

# EXAMPLE 4: Complete Observability
print("\n" + "=" * 70)
print("EXAMPLE 4: Production Observability System")
print("=" * 70)

obs_cb = ObservabilityCallback()
for chunk in model.stream(
    "Explain callbacks in one sentence",
    config={"callbacks": [obs_cb]}
):
    print(chunk.content, end="", flush=True)
print()

print("\n" + "=" * 70)
print("✅ CALLBACK HANDLERS COMPLETE!")
print("=" * 70)
print("\n💡 Callbacks enable observability by tracking LLM execution metrics.")
print("Production tools like LangSmith and LangFuse use this pattern.")
