"""
  Day 8 - Program 3: Cost Tracking Calculator

  Calculate real API costs based on token usage and pricing
"""

from langchain_ollama import ChatOllama
from langchain_core.callbacks import BaseCallbackHandler
from typing import Any, Dict, List

print("=" * 70)
print("COST TRACKING - Calculate API Costs")
print("=" * 70)

# ============================================================
# API PRICING (OpenAI GPT-4 as example)
# ============================================================
PRICING = {
    "gpt-4": {
        "input": 0.03,   # $0.03 per 1K tokens
        "output": 0.06,  # $0.06 per 1K tokens
    },
    "gpt-3.5-turbo": {
        "input": 0.0015,   # $0.0015 per 1K tokens
        "output": 0.002,   # $0.002 per 1K tokens
    },
    "qwen3:4b": {
        "input": 0.0,   # Free (local model)
        "output": 0.0,  # Free (local model)
    }
}

# ============================================================
# CALLBACK 1: Simple Cost Tracker
# ============================================================
class SimpleCostTracker(BaseCallbackHandler):
    """Basic cost calculation for a single request"""

    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name
        self.input_tokens = 0
        self.output_tokens = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        # Estimate input tokens (rough: 1 token ≈ 4 characters)
        prompt_text = prompts[0]
        self.input_tokens = len(prompt_text) // 4
        print(f"\n💰 Cost Tracker Started")
        print(f"   Model: {self.model_name}")
        print(f"   Estimated input tokens: {self.input_tokens}")

    def on_llm_new_token(self, token: str, **kwargs):
        # Count output tokens
        self.output_tokens += 1

    def on_llm_end(self, response, **kwargs):
        # Calculate cost
        pricing = PRICING.get(self.model_name, {"input": 0, "output": 0})

        input_cost = (self.input_tokens / 1000) * pricing["input"]
        output_cost = (self.output_tokens / 1000) * pricing["output"]
        total_cost = input_cost + output_cost

        print(f"\n💰 Cost Breakdown:")
        print(f"   Input:  {self.input_tokens} tokens × ${pricing['input']}/1K = ${input_cost:.6f}")
        print(f"   Output: {self.output_tokens} tokens × ${pricing['output']}/1K = ${output_cost:.6f}")
        print(f"   Total:  ${total_cost:.6f}")

# ============================================================
# CALLBACK 2: Per-Request Tracker
# ============================================================
class PerRequestCostTracker(BaseCallbackHandler):
    """Tracks cost for each individual request"""

    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name
        self.request_count = 0
        self.input_tokens = 0
        self.output_tokens = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        self.request_count += 1
        prompt_text = prompts[0]
        self.input_tokens = len(prompt_text) // 4
        self.output_tokens = 0

        print(f"\n📊 Request #{self.request_count}")
        print(f"   Prompt: '{prompts[0][:40]}...'")

    def on_llm_new_token(self, token: str, **kwargs):
        self.output_tokens += 1

    def on_llm_end(self, response, **kwargs):
        pricing = PRICING.get(self.model_name, {"input": 0, "output": 0})

        input_cost = (self.input_tokens / 1000) * pricing["input"]
        output_cost = (self.output_tokens / 1000) * pricing["output"]
        total_cost = input_cost + output_cost

        print(f"   Tokens: {self.input_tokens} in, {self.output_tokens} out")
        print(f"   Cost: ${total_cost:.6f}")

# ============================================================
# CALLBACK 3: Session Cost Tracker (Accumulative)
# ============================================================
class SessionCostTracker(BaseCallbackHandler):
    """Accumulates total cost across multiple requests"""

    def __init__(self, model_name="gpt-4"):
        self.model_name = model_name
        self.total_requests = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.current_input = 0
        self.current_output = 0

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs):
        self.total_requests += 1
        prompt_text = prompts[0]
        self.current_input = len(prompt_text) // 4
        self.current_output = 0

    def on_llm_new_token(self, token: str, **kwargs):
        self.current_output += 1

    def on_llm_end(self, response, **kwargs):
        # Accumulate totals
        self.total_input_tokens += self.current_input
        self.total_output_tokens += self.current_output

        # Calculate cost
        pricing = PRICING.get(self.model_name, {"input": 0, "output": 0})

        input_cost = (self.current_input / 1000) * pricing["input"]
        output_cost = (self.current_output / 1000) * pricing["output"]
        request_cost = input_cost + output_cost

        self.total_cost += request_cost

    def print_summary(self):
        """Print session summary"""
        print("\n" + "=" * 70)
        print("📊 SESSION COST SUMMARY")
        print("=" * 70)
        print(f"Model: {self.model_name}")
        print(f"Total Requests: {self.total_requests}")
        print(f"Total Input Tokens: {self.total_input_tokens}")
        print(f"Total Output Tokens: {self.total_output_tokens}")
        print(f"Total Tokens: {self.total_input_tokens + self.total_output_tokens}")
        print(f"\n💰 TOTAL COST: ${self.total_cost:.6f}")

        # Projections
        if self.total_requests > 0:
            avg_cost = self.total_cost / self.total_requests
            print(f"\n📈 Projections:")
            print(f"   Average per request: ${avg_cost:.6f}")
            print(f"   If 1,000 requests/day: ${avg_cost * 1000:.2f}/day")
            print(f"   If 1,000 requests/day: ${avg_cost * 1000 * 30:.2f}/month")
        print("=" * 70)

# ============================================================
# EXAMPLES: Testing Cost Trackers
# ============================================================

# Create model
model = ChatOllama(model="qwen3:4b", temperature=0.7)

# EXAMPLE 1: Simple Cost Tracker
print("\n" + "=" * 70)
print("EXAMPLE 1: Simple Cost Calculation")
print("=" * 70)

cost_tracker = SimpleCostTracker(model_name="qwen3:4b")
for chunk in model.stream(
    "Explain machine learning in one sentence",
    config={"callbacks": [cost_tracker]}
):
    print(chunk.content, end="", flush=True)
print()

# EXAMPLE 2: Per-Request Tracking
print("\n" + "=" * 70)
print("EXAMPLE 2: Per-Request Cost Tracking")
print("=" * 70)
print("Making 3 different requests...")

per_request_tracker = PerRequestCostTracker(model_name="gpt-4")

requests = [
    "What is Python?",
    "Explain REST APIs",
    "What is Docker?"
]

for prompt in requests:
    # Reset token counts for each request
    response = model.invoke(prompt, config={"callbacks": [per_request_tracker]})

# EXAMPLE 3: Session Cost Tracker
print("\n" + "=" * 70)
print("EXAMPLE 3: Session Cost Accumulation")
print("=" * 70)

session_tracker = SessionCostTracker(model_name="gpt-3.5-turbo")

print("Simulating 5 API calls...")

prompts = [
    "Hello",
    "What is AI?",
    "Explain neural networks",
    "What is deep learning?",
    "Tell me about transformers"
]

for i, prompt in enumerate(prompts, 1):
    print(f"\n[{i}/5] Processing: '{prompt}'")
    response = model.invoke(prompt, config={"callbacks": [session_tracker]})

# Print final summary
session_tracker.print_summary()

print("\n" + "=" * 70)
print("✅ COST TRACKING COMPLETE!")
print("=" * 70)
print("\n💡 Track API costs to avoid unexpected bills.")
print("Use SessionCostTracker in production to monitor spending.")
