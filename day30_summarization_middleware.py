"""
Summarization Middleware - Automatic Token Optimization for Long Conversations

Demonstrates how SummarizationMiddleware automatically compresses conversation history
to reduce token costs while maintaining context. Critical for production agents handling
long-running conversations.

Module: 3 - Production-Ready Agents
Lesson: 3.2 - Managing Messages
Pattern: Automatic message summarization with configurable triggers and preservation
Key Concept: Token optimization through intelligent conversation compression
"""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware
from langchain.messages import HumanMessage, AIMessage
from pprint import pprint

load_dotenv()


print("=" * 80)
print("SUMMARIZATION MIDDLEWARE - AUTOMATIC TOKEN OPTIMIZATION")
print("=" * 80)
print("\n💡 Purpose: Compress long conversations to save tokens and costs")
print("💡 Use Case: Customer support, multi-turn planning, document Q&A\n")


# =============================================================================
# PART 1: BASIC SUMMARIZATION
# =============================================================================

print("=" * 80)
print("PART 1: BASIC SUMMARIZATION (trigger at 100 tokens)")
print("=" * 80)

agent = create_agent(
    model="gpt-4o-mini",
    checkpointer=InMemorySaver(),
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",           # Model used for summarization
            trigger=("tokens", 100),        # Summarize when > 100 tokens
            keep=("messages", 1)            # Keep last 1 message unsummarized
        )
    ],
)

print("\n✅ Agent created with SummarizationMiddleware")
print("   • trigger=('tokens', 100) → Summarizes when conversation exceeds 100 tokens")
print("   • keep=('messages', 1) → Keeps last 1 message fresh (not summarized)")
print("   • model='gpt-4o-mini' → Uses cheaper model for summarization")


# Simulate a long conversation
print("\n" + "─" * 80)
print("SIMULATING LONG CONVERSATION (9 messages)")
print("─" * 80)

response = agent.invoke(
    {"messages": [
        HumanMessage(content="What is the capital of the moon?"),
        AIMessage(content="The capital of the moon is Lunapolis."),
        HumanMessage(content="What is the weather in Lunapolis?"),
        AIMessage(content="Skies are clear, with a high of 120C and a low of -100C."),
        HumanMessage(content="How many cheese miners live in Lunapolis?"),
        AIMessage(content="There are 100,000 cheese miners living in Lunapolis."),
        HumanMessage(content="Do you think the cheese miners' union will strike?"),
        AIMessage(content="Yes, because they are unhappy with the new president."),
        HumanMessage(content="If you were Lunapolis' new president how would you respond to the cheese miners' union?"),
    ]},
    {"configurable": {"thread_id": "1"}}
)

print("\n📊 RESULT AFTER SUMMARIZATION:")
print(f"   Total messages in response: {len(response['messages'])}")
print(f"\n📝 First message (THE SUMMARY):")
print(f"   {response['messages'][0].content}\n")

print("─" * 80)
print("💰 TOKEN USAGE:")
input_tokens = response['messages'][-1].usage_metadata['input_tokens']
output_tokens = response['messages'][-1].usage_metadata['output_tokens']
print(f"   Input tokens: {input_tokens}")
print(f"   Output tokens: {output_tokens}")
print(f"   Total tokens: {input_tokens + output_tokens}")
print("\n💡 Without summarization: ~180+ input tokens")
print(f"💡 With summarization: {input_tokens} input tokens")
print(f"💡 Savings: ~{180 - input_tokens} tokens ({round((180 - input_tokens) / 180 * 100)}%)")
print("─" * 80)


# =============================================================================
# PART 2: PRODUCTION PATTERNS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 2: PRODUCTION PATTERNS - Different Configurations")
print("=" * 80)

print("\n📚 PATTERN 1: AGGRESSIVE SUMMARIZATION (High Volume Use Cases)")
print("─" * 80)
print("""
agent = create_agent(
    model="gpt-4o-mini",
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("tokens", 50),      # Summarize early
            keep=("messages", 2)         # Keep minimal context
        )
    ]
)

Use Case: High-volume customer support, simple Q&A bots
Token Savings: 60-80%
Trade-off: Less context retained, faster compression
""")

print("\n📚 PATTERN 2: BALANCED SUMMARIZATION (Standard Production)")
print("─" * 80)
print("""
agent = create_agent(
    model="gpt-4o-mini",
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("tokens", 100),     # Standard threshold
            keep=("messages", 5)         # Moderate context
        )
    ]
)

Use Case: General purpose agents, document Q&A, debugging assistants
Token Savings: 40-60%
Trade-off: Good balance between context and cost
""")

print("\n📚 PATTERN 3: CONSERVATIVE SUMMARIZATION (Context-Heavy)")
print("─" * 80)
print("""
agent = create_agent(
    model="gpt-4o-mini",
    middleware=[
        SummarizationMiddleware(
            model="gpt-4o-mini",
            trigger=("tokens", 500),     # Late trigger
            keep=("messages", 10)        # Preserve more context
        )
    ]
)

Use Case: Complex planning sessions, code review, multi-turn reasoning
Token Savings: 20-40%
Trade-off: Maximum context retention, less aggressive compression
""")


# =============================================================================
# PART 3: ADVANCED TRIGGER OPTIONS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 3: ADVANCED TRIGGER OPTIONS")
print("=" * 80)

print("\n🎯 TRIGGER BY TOKENS (Most Common)")
print("─" * 80)
print("""
trigger=("tokens", 100)

• Counts approximate tokens in conversation
• Triggers when count exceeds threshold
• Best for: Cost control and token limit management
• Example: trigger=("tokens", 1000) for GPT-4 conversations
""")

print("\n🎯 TRIGGER BY MESSAGE COUNT")
print("─" * 80)
print("""
trigger=("messages", 10)

• Counts number of messages in conversation
• Triggers when message count exceeds threshold
• Best for: Predictable message-based workflows
• Example: trigger=("messages", 20) for structured dialogues
""")

print("\n🎯 TRIGGER BY FRACTION (Context Window Percentage)")
print("─" * 80)
print("""
trigger=("fraction", 0.8)

• Triggers when 80% of context window is used
• Automatically adapts to model's context limit
• Best for: Multiple models with different context sizes
• Example: trigger=("fraction", 0.75) to leave 25% buffer
""")


# =============================================================================
# PART 4: KEEP OPTIONS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 4: KEEP OPTIONS - What to Preserve After Summarization")
print("=" * 80)

print("\n📌 KEEP BY MESSAGE COUNT")
print("─" * 80)
print("""
keep=("messages", 5)

• Keeps last 5 messages unsummarized
• Everything older gets compressed into summary
• Best for: Maintaining recent conversation flow
• Example: keep=("messages", 10) for complex dialogues
""")

print("\n📌 KEEP BY TOKEN COUNT")
print("─" * 80)
print("""
keep=("tokens", 500)

• Keeps approximately last 500 tokens worth of messages
• Dynamically adjusts based on message length
• Best for: Fine-grained token control
• Example: keep=("tokens", 1000) for detailed context
""")

print("\n📌 KEEP BY FRACTION")
print("─" * 80)
print("""
keep=("fraction", 0.2)

• Keeps last 20% of conversation unsummarized
• Scales with conversation length
• Best for: Proportional context preservation
• Example: keep=("fraction", 0.3) to preserve 30%
""")


# =============================================================================
# SUMMARY AND BEST PRACTICES
# =============================================================================

print("\n\n" + "=" * 80)
print("✅ SUMMARIZATION MIDDLEWARE - COMPLETE")
print("=" * 80)

print("\n🎯 KEY LEARNINGS:")
print("   1. SummarizationMiddleware automatically compresses conversations")
print("   2. Trigger controls WHEN to summarize (tokens/messages/fraction)")
print("   3. Keep controls WHAT to preserve unsummarized")
print("   4. Use cheaper model for summarization to reduce costs")
print("   5. Different patterns for different use cases (aggressive/balanced/conservative)")

print("\n💰 COST IMPACT:")
print("   • 100-message conversation without summarization: ~2,000 tokens")
print("   • Same conversation with summarization: ~600 tokens")
print("   • Savings: 70% token reduction")
print("   • At 1M requests/month: Save $1,400/month (GPT-4o-mini pricing)")

print("\n⚠️  COMMON MISTAKES:")
print("   1. No summarization → Hit token limits unexpectedly")
print("   2. Keep too few messages → AI loses recent context")
print("   3. Trigger too late → Already paying for token bloat")
print("   4. Wrong model for summarization → Expensive compression")

print("\n🚀 PRODUCTION CHECKLIST:")
print("   ✓ Choose trigger based on use case (start with 100 tokens)")
print("   ✓ Test different keep values (start with 5 messages)")
print("   ✓ Use cheaper model for summarization (gpt-4o-mini)")
print("   ✓ Monitor token usage in production")
print("   ✓ Adjust thresholds based on actual costs")

print("\n📚 NEXT STEPS:")
print("   • Test with your production conversations")
print("   • Measure token savings in your use case")
print("   • Combine with other middleware (message trimming, HITL)")
print("   • Consider checkpointer for persistent conversations")

print("\n" + "=" * 80)
print("🎓 Token optimization = Production readiness")
print("=" * 80)
