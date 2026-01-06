"""
Dynamic Tools - Runtime Tool Access Control Based on User Permissions

Demonstrates how to dynamically restrict which tools an agent can use based on
user context (role, permissions, etc.) using @wrap_model_call middleware.
One agent serves both internal and external users with different tool access.

Module: 3 - Production-Ready Agents
Lesson: 3.4 - Dynamic Tools
Pattern: Wrap-style middleware that modifies available tools at runtime
Key Concept: Security gates - control tool access based on user identity
"""

from dotenv import load_dotenv
from dataclasses import dataclass
from langchain.tools import tool
from typing import Dict, Any, Callable
from tavily import TavilyClient
from langchain_community.utilities import SQLDatabase
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.agents import create_agent
from langchain.messages import HumanMessage

load_dotenv()


print("=" * 80)
print("DYNAMIC TOOLS - RUNTIME PERMISSION-BASED TOOL ACCESS")
print("=" * 80)
print("\n💡 Purpose: Control which tools users can access based on their role")
print("💡 Use Case: Security, permissions, role-based access control (RBAC)\n")


# =============================================================================
# PART 1: THE SECURITY PROBLEM
# =============================================================================

print("=" * 80)
print("PART 1: THE SECURITY PROBLEM")
print("=" * 80)

print("""
Naive approach (INSECURE):
──────────────────────────

agent = create_agent(
    tools=[web_search, sql_query]  # Everyone gets ALL tools
)

Problems:
• External customers can query your production database
• Attackers can run: DROP TABLE users;
• No permission control
• One breach = Full system access
• Compliance nightmare (SOC2, GDPR, HIPAA)

You need DYNAMIC tool access based on user identity.
""")


# =============================================================================
# PART 2: CREATE TOOLS
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: CREATE TOOLS (Safe + Dangerous)")
print("=" * 80)

# Initialize external services
tavily_client = TavilyClient()
db = SQLDatabase.from_uri("sqlite:///Chinook.db")  # Music database

@tool
def web_search(query: str) -> Dict[str, Any]:
    """Search the web for information"""
    return tavily_client.search(query)

@tool
def sql_query(query: str) -> str:
    """Obtain information from the database using SQL queries"""
    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"


print("\n✅ Two tools created:")
print("\n1. web_search(query: str)")
print("   • SAFE - Anyone can search the web")
print("   • Uses Tavily API (like Google for AI)")
print("   • Returns: Web search results")

print("\n2. sql_query(query: str)")
print("   • DANGEROUS - Only internal users should access database")
print("   • Connects to SQLite database (music data)")
print("   • Returns: Query results or error")
print("   • Risk: DELETE, DROP, UPDATE commands")


# =============================================================================
# PART 3: DEFINE USER ROLE CONTEXT
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 3: DEFINE USER ROLE CONTEXT")
print("=" * 80)

@dataclass
class UserRole:
    """Context schema for user role/permissions"""
    user_role: str = "external"


print("\n✅ UserRole context schema defined")
print("   • Similar to LanguageContext from dynamic prompts")
print("   • user_role field with default 'external'")
print("\n   Possible values:")
print("   • 'external' → Customer/public user (limited access)")
print("   • 'internal' → Employee (full access)")
print("\n   This context is passed in agent.invoke(..., context={...})")


# =============================================================================
# PART 4: CREATE DYNAMIC TOOL MIDDLEWARE
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 4: CREATE DYNAMIC TOOL MIDDLEWARE")
print("=" * 80)

@wrap_model_call
def dynamic_tool_call(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Dynamically restrict tools based on the runtime context"""

    # Read user role from context
    user_role = request.runtime.context.user_role

    # Internal users: Full access (all tools)
    if user_role == "internal":
        pass  # Don't modify request - keep all tools

    # External users: Restricted access (safe tools only)
    else:
        tools = [web_search]  # Only web search, no database
        request = request.override(tools=tools)  # Modify request

    # Continue to model with (possibly modified) request
    return handler(request)


print("\n✅ Dynamic tool middleware created")
print("\n   @wrap_model_call decorator:")
print("   • Wraps the model instance (f(x) style)")
print("   • Intercepts ModelRequest before model call")
print("   • Can modify: tools, prompt, model, context, state")

print("\n   Function parameters:")
print("   • request: ModelRequest → Contains tools, context, etc.")
print("   • handler: Callable → Function to continue to model")

print("\n   The logic:")
print("   1. Read user_role from request.runtime.context.user_role")
print("   2. If 'internal' → pass (keep all tools)")
print("   3. If 'external' → Override tools to [web_search] only")
print("   4. Call handler(request) to continue to model")

print("\n   Security enforcement:")
print("   • External users CANNOT use sql_query")
print("   • Database is protected from public access")
print("   • Same agent, different permissions")


# =============================================================================
# PART 5: CREATE AGENT WITH DYNAMIC MIDDLEWARE
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 5: CREATE AGENT WITH DYNAMIC MIDDLEWARE")
print("=" * 80)

agent = create_agent(
    model="gpt-4o-mini",
    tools=[web_search, sql_query],  # Register BOTH tools
    middleware=[dynamic_tool_call],  # Add security middleware
    context_schema=UserRole  # Define context schema
)

print("\n✅ Agent created with dynamic tool access control")
print("   • tools=[web_search, sql_query] → Both registered")
print("   • middleware=[dynamic_tool_call] → Security layer")
print("   • context_schema=UserRole → Expects user_role in context")
print("\n   How it works:")
print("   • Middleware intercepts EVERY model call")
print("   • Checks user_role from context")
print("   • Dynamically restricts tools based on role")
print("   • ONE agent, TWO permission levels")


# =============================================================================
# PART 6: TEST WITH EXTERNAL USER (RESTRICTED)
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 6: TEST WITH EXTERNAL USER (RESTRICTED ACCESS)")
print("=" * 80)

print("\n" + "─" * 80)
print("SCENARIO: External customer asks database question")
print("─" * 80)

print("\n📧 User asks: 'How many artists are in the database?'")
print("🔒 User role: 'external' (customer/public)")

response_external = agent.invoke(
    {"messages": [HumanMessage(content="How many artists are in the database?")]},
    context={"user_role": "external"}
)

print("\n⚙️  WHAT HAPPENED BEHIND THE SCENES:")
print("   1. User invoked with context={'user_role': 'external'}")
print("   2. @wrap_model_call middleware intercepted")
print("   3. Read: user_role = 'external'")
print("   4. Went to else block")
print("   5. Restricted tools to: [web_search] only")
print("   6. Removed sql_query from available tools")
print("   7. Model received request with ONLY web_search")
print("   8. Agent tried to answer but has no database access")

print(f"\n🤖 Agent response:")
print(f"   {response_external['messages'][-1].content}")

print("\n✅ SECURITY SUCCESS:")
print("   • External user BLOCKED from database")
print("   • sql_query tool not available to agent")
print("   • Database protected from public access")


# =============================================================================
# PART 7: TEST WITH INTERNAL USER (FULL ACCESS)
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 7: TEST WITH INTERNAL USER (FULL ACCESS)")
print("=" * 80)

print("\n" + "─" * 80)
print("SCENARIO: Internal employee asks same question")
print("─" * 80)

print("\n📧 Employee asks: 'How many artists are in the database?'")
print("🔓 User role: 'internal' (employee)")

response_internal = agent.invoke(
    {"messages": [HumanMessage(content="How many artists are in the database?")]},
    context={"user_role": "internal"}
)

print("\n⚙️  WHAT HAPPENED BEHIND THE SCENES:")
print("   1. User invoked with context={'user_role': 'internal'}")
print("   2. @wrap_model_call middleware intercepted")
print("   3. Read: user_role = 'internal'")
print("   4. Went to if block")
print("   5. pass (did nothing - kept all tools)")
print("   6. Model received request with BOTH tools: [web_search, sql_query]")
print("   7. Agent used sql_query to query database")
print("   8. Got actual data from database")

print(f"\n🤖 Agent response:")
print(f"   {response_internal['messages'][-1].content}")

print("\n✅ FULL ACCESS SUCCESS:")
print("   • Internal employee has database access")
print("   • sql_query tool available")
print("   • Agent successfully queried database")


# =============================================================================
# PART 8: THE COMPARISON
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 8: THE COMPARISON - Same Question, Different Access")
print("=" * 80)

print("""
┌─────────────────────────────────────────────────────────────────┐
│ QUESTION: "How many artists are in the database?"              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ EXTERNAL USER (context={'user_role': 'external'}):             │
│ ──────────────────────────────────────────────────────         │
│ • Middleware restricts to: [web_search] only                   │
│ • sql_query NOT available                                      │
│ • Response: "I don't have database access"                     │
│ • ✅ Security enforced                                          │
│                                                                 │
│ INTERNAL USER (context={'user_role': 'internal'}):             │
│ ──────────────────────────────────────────────────────         │
│ • Middleware keeps: [web_search, sql_query]                    │
│ • sql_query available                                          │
│ • Response: "There are 275 artists in the database"            │
│ • ✅ Full access granted                                        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

ONE AGENT. TWO USERS. DIFFERENT PERMISSIONS. RUNTIME CONTROL.
""")


# =============================================================================
# PART 9: ADVANCED PATTERNS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 9: ADVANCED PRODUCTION PATTERNS")
print("=" * 80)

print("""
📚 PATTERN 1: MULTI-TIER PERMISSIONS
────────────────────────────────────

@dataclass
class UserContext:
    role: str = "guest"  # guest, user, admin, super_admin

@wrap_model_call
def tiered_tools(request, handler):
    role = request.runtime.context.role

    if role == "super_admin":
        # Full access
        tools = [web_search, sql_query, delete_data, admin_panel]
    elif role == "admin":
        # Admin access (no delete)
        tools = [web_search, sql_query, admin_panel]
    elif role == "user":
        # Standard user
        tools = [web_search, sql_query]
    else:  # guest
        # Minimal access
        tools = [web_search]

    request = request.override(tools=tools)
    return handler(request)

Use Case: SaaS with multiple subscription tiers
Result: Free → web_search, Pro → + database, Enterprise → + admin


📚 PATTERN 2: DEPARTMENT-BASED TOOLS
────────────────────────────────────

@dataclass
class EmployeeContext:
    department: str = "sales"

@wrap_model_call
def department_tools(request, handler):
    dept = request.runtime.context.department

    if dept == "finance":
        tools = [web_search, financial_db, payroll_system]
    elif dept == "engineering":
        tools = [web_search, code_search, deployment_tools]
    elif dept == "sales":
        tools = [web_search, crm_access, customer_db]
    else:
        tools = [web_search]

    request = request.override(tools=tools)
    return handler(request)

Use Case: Enterprise with department-specific access
Result: Finance sees payroll, Engineering sees code, Sales sees CRM


📚 PATTERN 3: TIME-BASED ACCESS CONTROL
───────────────────────────────────────

from datetime import datetime

@wrap_model_call
def business_hours_tools(request, handler):
    hour = datetime.now().hour
    role = request.runtime.context.role

    # Business hours (9am-5pm)
    if 9 <= hour < 17:
        if role == "internal":
            tools = [web_search, sql_query, sensitive_data]
        else:
            tools = [web_search]
    # After hours
    else:
        # Restricted access even for internal
        tools = [web_search]

    request = request.override(tools=tools)
    return handler(request)

Use Case: Compliance, audit requirements
Result: Sensitive data only accessible during business hours


📚 PATTERN 4: FEATURE FLAGS / A/B TESTING
─────────────────────────────────────────

@dataclass
class UserContext:
    user_id: str
    role: str = "user"

@wrap_model_call
def feature_flag_tools(request, handler):
    user_id = request.runtime.context.user_id

    # Check feature flag system
    if is_beta_user(user_id):
        tools = [web_search, sql_query, new_experimental_tool]
    else:
        tools = [web_search, sql_query]

    request = request.override(tools=tools)
    return handler(request)

Use Case: Gradual rollout, beta testing
Result: 10% of users get new tool for testing
""")


# =============================================================================
# PART 10: COMBINING DYNAMIC PROMPTS + TOOLS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 10: COMBINING DYNAMIC PROMPTS + TOOLS")
print("=" * 80)

print("""
You can use BOTH @dynamic_prompt AND @wrap_model_call together:

@dataclass
class UserContext:
    language: str = "English"
    role: str = "external"

@dynamic_prompt
def language_prompt(request: ModelRequest) -> str:
    lang = request.runtime.context.language
    return f"Respond in {lang}."

@wrap_model_call
def role_tools(request, handler):
    role = request.runtime.context.role

    if role == "internal":
        tools = [web_search, sql_query]
    else:
        tools = [web_search]

    request = request.override(tools=tools)
    return handler(request)

agent = create_agent(
    model="gpt-4o-mini",
    tools=[web_search, sql_query],
    middleware=[language_prompt, role_tools],  # BOTH!
    context_schema=UserContext
)

Result:
• Spanish external user → Spanish language + web_search only
• French internal user → French language + all tools
• Full context-driven adaptation
""")


# =============================================================================
# SUMMARY AND BEST PRACTICES
# =============================================================================

print("\n\n" + "=" * 80)
print("✅ DYNAMIC TOOLS - COMPLETE")
print("=" * 80)

print("\n🎯 KEY LEARNINGS:")
print("   1. @wrap_model_call intercepts ModelRequest (f(x) wrapping)")
print("   2. request.override(tools=[...]) changes available tools")
print("   3. handler(request) continues to model with modified request")
print("   4. One agent serves multiple user types with different permissions")
print("   5. Security enforced at runtime (not configuration)")

print("\n💼 PRODUCTION USE CASES:")
print("   • SaaS multi-tier access (free/pro/enterprise)")
print("   • Enterprise RBAC (role-based access control)")
print("   • Department-specific tool access")
print("   • Time-based security restrictions")
print("   • Feature flags and beta testing")

print("\n⚠️  COMMON MISTAKES:")
print("   1. Giving all tools to all users → Use dynamic tools")
print("   2. Creating separate agents per role → Use one agent + middleware")
print("   3. Forgetting to pass context → No permission control")
print("   4. Not validating user_role → Security bypass risk")

print("\n🚀 PRODUCTION CHECKLIST:")
print("   ✓ Define context schema with user role/permissions")
print("   ✓ Create @wrap_model_call middleware for tool filtering")
print("   ✓ Use request.override(tools=[...]) to restrict access")
print("   ✓ Call handler(request) to continue to model")
print("   ✓ Test with different user roles")
print("   ✓ Validate user identity before setting context")
print("   ✓ Log tool access for audit compliance")

print("\n📚 NEXT STEPS:")
print("   • Dynamic Models → Switch foundation models based on complexity")
print("   • Combine prompts + tools + models → Full runtime control")
print("   • Implement real auth system (JWT, OAuth) → Set context from token")
print("   • Add audit logging → Track who accessed what")

print("\n" + "=" * 80)
print("🎓 Security gates at runtime. Not deploy time.")
print("=" * 80)
