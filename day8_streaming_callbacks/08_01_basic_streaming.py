from langchain_ollama import ChatOllama

"""
  Day 8 - Program 1: Basic Streaming

  See LLM responses appear token-by-token (like ChatGPT)
"""
print("=" * 60)
print("BASIC STREAMING - Token by Token")
print("=" * 60)

# Create LLM
model = ChatOllama(model="qwen3:4b", temperature=0.7)

# ============================================================
# PART 1: WITHOUT Streaming (Traditional Way)
# ============================================================
print("\n📦 WITHOUT STREAMING:")
print("-" * 60)

response=model.invoke("write a short poem about coding")
print(response.content)

print("\n⏱️  You waited for the ENTIRE response")

# ============================================================
# PART 2: WITH Streaming (Modern Way)
# ============================================================
print("\n" + "=" * 60)
print("\n✨ WITH STREAMING:")
print("-" * 60)

for chunk in model.stream("write a short peom about coding"):
	print(chunk.content,end="",flush=True)

print("\n")
print("\n⚡ Tokens appeared immediately!")

# ============================================================
# PART 3: Understanding Chunks
# ============================================================
print("\n" + "=" * 60)
print("\n🔍 UNDERSTANDING CHUNKS")
print("-" * 60)

for i,chunk in enumerate(model.stream("Say: Hello World!"),start=1):
	print(f" chunk {1}: '{chunk.content}'")

print("\n" + "=" * 60)
print("✅ STREAMING COMPLETE!")
print("=" * 60)

