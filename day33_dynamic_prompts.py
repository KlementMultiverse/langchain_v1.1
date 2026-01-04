"""
Dynamic Prompts - Wrap the Model Instance for Runtime Adaptation

Demonstrates how to change system prompts dynamically based on user context
using @dynamic_prompt middleware. One agent adapts to multiple users, languages,
roles, and contexts - at runtime, not deploy time.

Module: 3 - Production-Ready Agents
Lesson: 3.4 - Dynamic Prompts
Pattern: Wrap-style middleware that intercepts ModelRequest
Key Concept: One agent, infinite behaviors through runtime context
"""

from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.agents.middleware import dynamic_prompt, ModelRequest
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

load_dotenv()


print("=" * 80)
print("DYNAMIC PROMPTS - ONE AGENT, 10,000 USERS")
print("=" * 80)
print("\n💡 Purpose: Adapt system prompts at runtime based on user context")
print("💡 Use Case: Multilingual agents, role-based personas, compliance\n")


# =============================================================================
# PART 1: THE PRODUCTION PROBLEM
# =============================================================================

print("=" * 80)
print("PART 1: THE PRODUCTION PROBLEM")
print("=" * 80)

print("""
MVP approach (BROKEN at scale):
────────────────────────────────

agent = create_agent(
    model="gpt-4o-mini",
    prompt="You are a helpful assistant. Respond in English."
)

Problems:
• Spanish user arrives → Stuck in English
• CEO logs in → Gets junior-level responses
• EU customer → No GDPR compliance
• Simple question → Uses expensive model
• 10,000 users → All get same experience

One-size-fits-all BREAKS in production.
""")


# =============================================================================
# PART 2: DEFINE CONTEXT SCHEMA
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: DEFINE CONTEXT SCHEMA")
print("=" * 80)

@dataclass
class LanguageContext:
    """Context schema for user language preferences"""
    user_language: str = "English"


print("\n✅ LanguageContext defined")
print("   • Similar to AgentState (but for context, not state)")
print("   • user_language: str with default 'English'")
print("   • This gets passed in agent.invoke(..., context={...})")


# =============================================================================
# PART 3: CREATE DYNAMIC PROMPT MIDDLEWARE
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 3: CREATE DYNAMIC PROMPT MIDDLEWARE")
print("=" * 80)

@dynamic_prompt
def user_language_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user language."""
    # Access user context from ModelRequest
    user_language = request.runtime.context.user_language

    # Base prompt for all users
    base_prompt = "You are a helpful assistant."

    # Adapt prompt based on language
    if user_language != "English":
        return f"{base_prompt} Only respond in {user_language}."
    elif user_language == "English":
        return base_prompt


print("\n✅ Dynamic prompt middleware created")
print("\n   @dynamic_prompt decorator:")
print("   • Wraps the model instance (not before/after)")
print("   • Runs INSIDE every model call")
print("   • Intercepts ModelRequest object")
print("\n   ModelRequest contains:")
print("   • Foundation model (GPT-4, Claude, etc.)")
print("   • System prompt (what we're changing)")
print("   • Available tools")
print("   • User context (language, role, permissions)")
print("   • Conversation state")
print("   • Runtime config")
print("\n   The function:")
print("   • Reads user_language from request.runtime.context")
print("   • Returns different prompt based on language")
print("   • This becomes the system prompt for THIS call only")


# =============================================================================
# PART 4: CREATE AGENT WITH DYNAMIC MIDDLEWARE
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 4: CREATE AGENT WITH DYNAMIC MIDDLEWARE")
print("=" * 80)

agent = create_agent(
    model="gpt-4o-mini",
    context_schema=LanguageContext,  # Define context schema
    middleware=[user_language_prompt]  # Add dynamic prompt middleware
)

print("\n✅ Agent created with dynamic prompt middleware")
print("   • context_schema=LanguageContext → Defines context structure")
print("   • middleware=[user_language_prompt] → Wraps model calls")
print("   • ONE agent that adapts to EVERY user")


# =============================================================================
# PART 5: TEST WITH DIFFERENT LANGUAGES
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 5: TEST WITH DIFFERENT LANGUAGES")
print("=" * 80)

print("\n" + "─" * 80)
print("TEST 1: SPANISH USER")
print("─" * 80)

response_spanish = agent.invoke(
    {"messages": [HumanMessage(content="Hello, how are you?")]},
    context=LanguageContext(user_language="Spanish")
)

print("\n📧 User input: 'Hello, how are you?'")
print("🌍 Context: user_language='Spanish'")
print("🔧 Middleware generates prompt: 'You are a helpful assistant. Only respond in Spanish.'")
print(f"\n🤖 Agent response:")
print(f"   {response_spanish['messages'][-1].content}\n")


print("─" * 80)
print("TEST 2: FRENCH USER")
print("─" * 80)

response_french = agent.invoke(
    {"messages": [HumanMessage(content="Hello, how are you?")]},
    context=LanguageContext(user_language="French")
)

print("\n📧 User input: 'Hello, how are you?'")
print("🌍 Context: user_language='French'")
print("🔧 Middleware generates prompt: 'You are a helpful assistant. Only respond in French.'")
print(f"\n🤖 Agent response:")
print(f"   {response_french['messages'][-1].content}\n")


print("─" * 80)
print("TEST 3: IRISH USER")
print("─" * 80)

response_irish = agent.invoke(
    {"messages": [HumanMessage(content="Hello, how are you?")]},
    context=LanguageContext(user_language="Irish")
)

print("\n📧 User input: 'Hello, how are you?'")
print("🌍 Context: user_language='Irish'")
print("🔧 Middleware generates prompt: 'You are a helpful assistant. Only respond in Irish.'")
print(f"\n🤖 Agent response:")
print(f"   {response_irish['messages'][-1].content}\n")


print("─" * 80)
print("TEST 4: ENGLISH USER (default)")
print("─" * 80)

response_english = agent.invoke(
    {"messages": [HumanMessage(content="Hello, how are you?")]},
    context=LanguageContext(user_language="English")
)

print("\n📧 User input: 'Hello, how are you?'")
print("🌍 Context: user_language='English'")
print("🔧 Middleware generates prompt: 'You are a helpful assistant.'")
print(f"\n🤖 Agent response:")
print(f"   {response_english['messages'][-1].content}\n")


# =============================================================================
# PART 6: THE MAGIC - WHAT JUST HAPPENED?
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 6: THE MAGIC - WHAT JUST HAPPENED?")
print("=" * 80)

print("""
EXECUTION FLOW:
───────────────

1. User invokes agent with context:
   agent.invoke({...}, context={"user_language": "Spanish"})

2. @dynamic_prompt middleware intercepts:
   • Before model is called
   • Wraps the ModelRequest object
   • This is f(x) wrapping at the model layer

3. Middleware reads context:
   user_language = request.runtime.context.user_language
   # Returns: "Spanish"

4. Middleware generates dynamic prompt:
   return "You are a helpful assistant. Only respond in Spanish."

5. Model receives THIS prompt (not the default):
   • Same agent
   • Different prompt
   • Every single call

6. Agent responds in Spanish

SAME AGENT. DIFFERENT USER. DIFFERENT PROMPT. RUNTIME ADAPTATION.
""")


# =============================================================================
# PART 7: ADVANCED PATTERNS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 7: ADVANCED PRODUCTION PATTERNS")
print("=" * 80)

print("""
📚 PATTERN 1: ROLE-BASED PROMPTS
─────────────────────────────────

@dataclass
class UserContext:
    language: str = "English"
    role: str = "customer"

@dynamic_prompt
def role_based_prompt(request: ModelRequest) -> str:
    lang = request.runtime.context.language
    role = request.runtime.context.role

    if role == "CEO":
        return f"Be concise. High-level summaries only. Respond in {lang}."
    elif role == "engineer":
        return f"Be technical. Include code examples. Respond in {lang}."
    elif role == "support":
        return f"Be empathetic. Customer-focused. Respond in {lang}."
    else:
        return f"You are a helpful assistant. Respond in {lang}."

Use Case: Enterprise agents serving different roles
Result: CEO gets summaries, engineers get code, support gets empathy


📚 PATTERN 2: COMPLIANCE-DRIVEN PROMPTS
───────────────────────────────────────

@dataclass
class ComplianceContext:
    region: str = "US"
    language: str = "English"

@dynamic_prompt
def compliance_prompt(request: ModelRequest) -> str:
    region = request.runtime.context.region
    lang = request.runtime.context.language

    base = f"You are a helpful assistant. Respond in {lang}."

    if region == "EU":
        return f"{base} Include GDPR disclaimers. Data privacy is critical."
    elif region == "US":
        return f"{base} Include standard legal disclaimers."
    elif region == "APAC":
        return f"{base} Follow local data regulations."
    else:
        return base

Use Case: Legal compliance, data privacy requirements
Result: Automatic regional compliance without duplicate agents


📚 PATTERN 3: MID-CONVERSATION LANGUAGE SWITCHING
─────────────────────────────────────────────────

# Message 1
agent.invoke({"messages": [...]}, context={"language": "English"})
# Agent responds in English

# Message 2 (same conversation, user switches)
agent.invoke({"messages": [...]}, context={"language": "Spanish"})
# Agent IMMEDIATELY switches to Spanish

# Message 3 (switches again)
agent.invoke({"messages": [...]}, context={"language": "French"})
# Agent switches to French

Use Case: Multilingual customer support
Result: Seamless language switching mid-conversation


📚 PATTERN 4: TIME-BASED PROMPTS
────────────────────────────────

from datetime import datetime

@dynamic_prompt
def time_based_prompt(request: ModelRequest) -> str:
    hour = datetime.now().hour
    lang = request.runtime.context.language

    if 0 <= hour < 6:
        tone = "Brief and urgent (user might be in crisis)"
    elif 6 <= hour < 12:
        tone = "Professional and energetic"
    elif 12 <= hour < 18:
        tone = "Helpful and patient"
    else:
        tone = "Casual and friendly"

    return f"You are a helpful assistant. {tone}. Respond in {lang}."

Use Case: 24/7 support with time-appropriate tone
Result: Different personality based on time of day
""")


# =============================================================================
# PART 8: THIS IS THE MODEL
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 8: THIS IS THE MODEL (Not Before/After)")
print("=" * 80)

print("""
BEFORE/AFTER HOOKS (Different):
────────────────────────────────

@before_agent → Runs OUTSIDE agent, before execution starts
@after_agent  → Runs OUTSIDE agent, after execution completes
@before_model → Runs OUTSIDE model, before model is called
@after_model  → Runs OUTSIDE model, after model responds

These run AROUND your agent/model.


WRAP-STYLE MIDDLEWARE (This):
──────────────────────────────

@dynamic_prompt  → Runs INSIDE model call, intercepts ModelRequest
@wrap_model_call → Runs INSIDE model call, full control

These run INSIDE your model.

You're not decorating the agent.
You're intercepting the model request itself.

f(x) wrapping at the model layer.

You can change:
• System prompt (this lesson)
• Available tools (next: dynamic tools)
• Foundation model (next: dynamic models)
• Context, state, config

FULL RUNTIME CONTROL.
""")


# =============================================================================
# SUMMARY AND BEST PRACTICES
# =============================================================================

print("\n\n" + "=" * 80)
print("✅ DYNAMIC PROMPTS - COMPLETE")
print("=" * 80)

print("\n🎯 KEY LEARNINGS:")
print("   1. @dynamic_prompt wraps the model instance (not before/after)")
print("   2. ModelRequest contains: model, prompt, tools, context, state")
print("   3. One agent adapts to infinite users via runtime context")
print("   4. Context drives behavior (not configuration files)")
print("   5. Works mid-conversation (language switching, role changes)")

print("\n💼 PRODUCTION USE CASES:")
print("   • Multilingual SaaS (1 agent, 47 languages)")
print("   • Enterprise agents (role-based personas)")
print("   • Compliance automation (EU GDPR, US legal, APAC regulations)")
print("   • Time-based personalities (24/7 support with appropriate tone)")
print("   • Cost optimization (combine with dynamic models)")

print("\n⚠️  COMMON MISTAKES:")
print("   1. Creating separate agents per language → Use dynamic prompts")
print("   2. Hardcoding prompts at deploy time → Use runtime context")
print("   3. Using @before_agent instead of @dynamic_prompt → Different purpose")
print("   4. Not defining context_schema → Agent won't know context structure")

print("\n🚀 PRODUCTION CHECKLIST:")
print("   ✓ Define context schema (@dataclass with user fields)")
print("   ✓ Create @dynamic_prompt function that reads request.runtime.context")
print("   ✓ Return different prompts based on context")
print("   ✓ Pass context in agent.invoke(..., context={...})")
print("   ✓ Test with different contexts (languages, roles, etc.)")
print("   ✓ Combine with dynamic tools and dynamic models for full control")

print("\n📚 NEXT STEPS:")
print("   • Dynamic Tools → Change available tools based on user role")
print("   • Dynamic Models → Switch foundation models based on complexity")
print("   • Combine all three → Full runtime agent adaptation")
print("   • Production deployment with user context from auth system")

print("\n" + "=" * 80)
print("🎓 One agent. 10,000 users. Infinite behaviors.")
print("=" * 80)
