"""
Human-in-the-Loop (HITL) Middleware - Approve Dangerous Actions

Demonstrates how to require human approval before agents execute critical tools
like sending emails, deleting files, or making payments. Essential for production
agents that can take irreversible actions.

Module: 3 - Production-Ready Agents
Lesson: 3.3 - Human-in-the-Loop
Pattern: Interrupt on dangerous tools, allow humans to approve/reject/edit
Key Concept: Safety gates for production agents
"""

from dotenv import load_dotenv
from langchain.tools import tool, ToolRuntime
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.messages import HumanMessage
from langgraph.types import Command
from pprint import pprint

load_dotenv()


print("=" * 80)
print("HUMAN-IN-THE-LOOP (HITL) - SAFETY GATES FOR PRODUCTION AGENTS")
print("=" * 80)
print("\n💡 Purpose: Require approval before dangerous actions")
print("💡 Use Case: Email agents, payment systems, file operations, API calls\n")


# =============================================================================
# PART 1: DEFINE CUSTOM STATE
# =============================================================================

print("=" * 80)
print("PART 1: CUSTOM STATE - Store Email Content")
print("=" * 80)

class EmailState(AgentState):
    """Custom state that includes email content"""
    email: str  # Email content stored in state


print("\n✅ EmailState defined")
print("   • AgentState is the base class")
print("   • email: str is a custom field")
print("   • Tools can access this via runtime.state['email']")


# =============================================================================
# PART 2: CREATE TOOLS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 2: CREATE TOOLS - Read and Send Email")
print("=" * 80)

@tool
def read_email(runtime: ToolRuntime) -> str:
    """Read an email from the inbox."""
    # Access email from state (not from parameters!)
    return runtime.state["email"]


@tool
def send_email(body: str) -> str:
    """Send an email with the given body text."""
    # In production, this would actually send email
    # For demo, we just return confirmation
    return f"Email sent successfully with body: {body[:50]}..."


print("\n✅ Two tools created:")
print("\n1. read_email(runtime: ToolRuntime)")
print("   • SAFE tool - no approval needed")
print("   • Reads from runtime.state['email']")
print("   • No parameters needed (gets data from state)")

print("\n2. send_email(body: str)")
print("   • DANGEROUS tool - needs approval!")
print("   • Takes body parameter (email text)")
print("   • Would send real email in production")


# =============================================================================
# PART 3: CREATE AGENT WITH HITL MIDDLEWARE
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 3: CREATE AGENT WITH HITL MIDDLEWARE")
print("=" * 80)

agent = create_agent(
    model="gpt-4o-mini",
    tools=[read_email, send_email],
    state_schema=EmailState,  # Use custom state
    checkpointer=InMemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "read_email": False,   # Don't interrupt (safe)
                "send_email": True,    # DO interrupt (dangerous!)
            },
            description_prefix="Tool execution requires approval",
        ),
    ],
)

print("\n✅ Agent created with HumanInTheLoopMiddleware")
print("\n   interrupt_on configuration:")
print("   • 'read_email': False  → Runs automatically (safe)")
print("   • 'send_email': True   → Pauses for approval (dangerous)")
print("\n   description_prefix: Shows in approval message")


# =============================================================================
# PART 4: RUN AGENT - IT WILL PAUSE
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 4: INVOKE AGENT - Watch It Pause Before Sending")
print("=" * 80)

config = {"configurable": {"thread_id": "email-demo-1"}}

print("\n📧 Incoming email:")
incoming_email = "Hi Seán, I'm going to be late for our meeting tomorrow. Can we reschedule? Best, John."
print(f"   {incoming_email}")

print("\n🤖 Invoking agent...")

response = agent.invoke(
    {
        "messages": [HumanMessage(content="Please read my email and send a response.")],
        "email": incoming_email  # Custom state field
    },
    config=config
)

print("\n⏸️  AGENT PAUSED!")


# =============================================================================
# PART 5: INSPECT THE INTERRUPT
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 5: INSPECT WHAT AGENT WANTS TO DO")
print("=" * 80)

# Check if agent is paused
if "__interrupt__" in response:
    print("\n✅ Agent is waiting for approval")

    # Get the interrupt data
    interrupt_data = response['__interrupt__'][0]
    action_request = interrupt_data.value['action_requests'][0]

    # Show what tool it wants to call
    tool_name = action_request['name']
    tool_args = action_request['args']

    print(f"\n📋 INTERRUPT DETAILS:")
    print(f"   Tool: {tool_name}")
    print(f"   Description: {action_request['description'][:60]}...")

    # Show the email it wants to send
    email_body = tool_args['body']
    print(f"\n📧 EMAIL IT WANTS TO SEND:")
    print("   " + "─" * 76)
    for line in email_body.split('\n'):
        print(f"   {line}")
    print("   " + "─" * 76)

    # Show allowed decisions
    allowed_decisions = interrupt_data.value['review_configs'][0]['allowed_decisions']
    print(f"\n🎯 ALLOWED DECISIONS: {allowed_decisions}")
    print("   These are your options (the menu)")
    print("   Now YOU must choose which one to send!")

else:
    print("\n❌ No interrupt found (agent completed without pausing)")


# =============================================================================
# PART 6: REAL-WORLD DECISION LOGIC
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 6: REAL-WORLD DECISION LOGIC (Interactive)")
print("=" * 80)

print("\n💡 In production, you'd show this to the user in a UI")
print("💡 For this demo, we'll simulate user input\n")

# Simulate user decision (in production, this comes from UI)
print("What would you like to do?")
print("  [a] Approve - Send email as-is")
print("  [r] Reject - Don't send email")
print("  [e] Edit - Change email text before sending")

user_choice = input("\nYour choice (a/r/e): ").lower()

print("\n" + "─" * 80)

# =============================================================================
# OPTION 1: APPROVE
# =============================================================================

if user_choice == 'a':
    print("\n✅ YOU CHOSE: APPROVE")
    print("   Sending Command with 'approve' decision...\n")

    response = agent.invoke(
        Command(resume={"decisions": [{"type": "approve"}]}),
        config=config  # Same thread_id to continue conversation
    )

    print("✅ EMAIL SENT!")
    print(f"\n📨 Final response:")
    if 'messages' in response:
        print(f"   {response['messages'][-1].content}")


# =============================================================================
# OPTION 2: REJECT
# =============================================================================

elif user_choice == 'r':
    print("\n❌ YOU CHOSE: REJECT")
    reject_reason = input("Why are you rejecting? (Enter reason): ")

    print(f"\n   Sending Command with 'reject' decision...")
    print(f"   Reason: {reject_reason}\n")

    response = agent.invoke(
        Command(resume={
            "decisions": [{
                "type": "reject",
                "message": reject_reason
            }]
        }),
        config=config
    )

    print("❌ EMAIL NOT SENT")
    print(f"\n🤖 Agent received your rejection")

    # Agent might try something else or ask for clarification
    if "__interrupt__" in response:
        print("   Agent is asking for approval again (new action)")
    else:
        print("   Agent stopped (conversation ended)")


# =============================================================================
# OPTION 3: EDIT
# =============================================================================

elif user_choice == 'e':
    print("\n✏️  YOU CHOSE: EDIT")
    print("\nOriginal email:")
    print("─" * 76)
    print(email_body)
    print("─" * 76)

    new_body = input("\nEnter your edited email text:\n> ")

    print(f"\n   Sending Command with 'edit' decision...")
    print(f"   New body: {new_body[:50]}...\n")

    response = agent.invoke(
        Command(resume={
            "decisions": [{
                "type": "edit",
                "edited_action": {
                    "name": "send_email",  # Same tool name
                    "args": {"body": new_body}  # Your edited content
                }
            }]
        }),
        config=config
    )

    print("✏️  EDITED EMAIL SENT!")
    print(f"\n📨 Final response:")
    if 'messages' in response:
        print(f"   {response['messages'][-1].content}")

else:
    print("\n⚠️  Invalid choice. In production, you'd re-prompt the user.")


# =============================================================================
# PART 7: EXPLANATION OF THE FLOW
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 7: WHAT JUST HAPPENED - Step by Step")
print("=" * 80)

print("""
STEP 1: Agent invoked with message and email
   ↓
   agent.invoke({
       "messages": [HumanMessage(...)],
       "email": "Hi Seán, I'm late..."  ← Saved to state
   })

STEP 2: Agent reads message "Please read my email and send a response"
   ↓
   Agent decides: "I need to call read_email() tool"

STEP 3: read_email() runs (interrupt_on["read_email"] = False)
   ↓
   Returns: "Hi Seán, I'm late..."
   No pause (safe tool)

STEP 4: Agent decides: "I need to call send_email() tool"
   ↓
   HumanInTheLoopMiddleware sees: interrupt_on["send_email"] = True
   ↓
   ⏸️  AGENT PAUSES (doesn't execute send_email yet)

STEP 5: response['__interrupt__'] contains:
   • Tool name: "send_email"
   • Tool args: {"body": "Hi John, Thanks for..."}
   • Allowed decisions: ["approve", "reject", "edit"]

STEP 6: Human reviews and chooses
   ↓
   User sees email preview
   User chooses: approve / reject / edit

STEP 7: Send decision back to agent
   ↓
   agent.invoke(Command(resume={"decisions": [{"type": "approve"}]}))

STEP 8: Agent continues based on decision
   ↓
   • approve → Runs send_email() with original args
   • reject → Doesn't run, agent sees rejection message
   • edit → Runs send_email() with YOUR edited args

STEP 9: Agent completes
   ↓
   Email sent (or not, depending on your decision)
""")


# =============================================================================
# PART 8: PRODUCTION PATTERNS
# =============================================================================

print("\n\n" + "=" * 80)
print("PART 8: PRODUCTION PATTERNS")
print("=" * 80)

print("""
📚 PATTERN 1: INTERRUPT ONLY DANGEROUS TOOLS
─────────────────────────────────────────────
interrupt_on={
    "read_file": False,      # Safe - just reading
    "delete_file": True,     # Dangerous - needs approval
    "search_docs": False,    # Safe - just searching
    "send_email": True,      # Dangerous - external action
    "make_payment": True,    # Dangerous - costs money
}

Use Case: File management, email, payments
Why: Let agent work freely, but pause before irreversible actions


📚 PATTERN 2: APPROVAL WORKFLOW IN WEB APP
──────────────────────────────────────────
# Backend API endpoint
@app.post("/chat")
async def chat(message: str, thread_id: str):
    response = agent.invoke(...)

    if "__interrupt__" in response:
        # Agent paused - send to frontend for approval
        return {
            "status": "awaiting_approval",
            "action": response['__interrupt__'][0].value,
            "thread_id": thread_id
        }
    else:
        return {"status": "complete", "response": ...}

@app.post("/approve")
async def approve_action(thread_id: str, decision: dict):
    # User approved/rejected/edited
    response = agent.invoke(
        Command(resume={"decisions": [decision]}),
        config={"configurable": {"thread_id": thread_id}}
    )
    return {"status": "complete"}

Use Case: Web apps, mobile apps
Why: Async approval workflow (user sees UI, clicks button)


📚 PATTERN 3: AUTO-APPROVE BASED ON RULES
─────────────────────────────────────────
if "__interrupt__" in response:
    action = response['__interrupt__'][0].value['action_requests'][0]

    # Auto-approve if email is short and polite
    if action['name'] == 'send_email':
        body = action['args']['body']
        if len(body) < 200 and "please" in body.lower():
            # Auto-approve
            response = agent.invoke(
                Command(resume={"decisions": [{"type": "approve"}]}),
                config=config
            )
        else:
            # Send to human
            show_approval_ui(action)

Use Case: Smart automation with safety rules
Why: Reduce human burden while maintaining safety


📚 PATTERN 4: MULTIPLE APPROVERS
────────────────────────────────
if "__interrupt__" in response:
    action = response['__interrupt__'][0].value['action_requests'][0]

    # Payments > $1000 need manager approval
    if action['name'] == 'make_payment':
        amount = action['args']['amount']
        if amount > 1000:
            approval = await get_manager_approval(action)
        else:
            approval = await get_user_approval(action)

    response = agent.invoke(
        Command(resume={"decisions": [approval]}),
        config=config
    )

Use Case: Enterprise workflows, compliance
Why: Different approval levels based on risk
""")


# =============================================================================
# SUMMARY
# =============================================================================

print("\n\n" + "=" * 80)
print("✅ HUMAN-IN-THE-LOOP - COMPLETE")
print("=" * 80)

print("\n🎯 KEY LEARNINGS:")
print("   1. HumanInTheLoopMiddleware pauses agent before dangerous tools")
print("   2. interrupt_on = {tool_name: True/False} controls which tools pause")
print("   3. response['__interrupt__'] contains what agent wants to do")
print("   4. allowed_decisions shows your options (menu)")
print("   5. Command(resume={...}) sends your decision back to agent")
print("   6. Three decision types: approve, reject, edit")

print("\n💼 PRODUCTION USE CASES:")
print("   • Email agents (review before sending)")
print("   • Payment systems (approve transactions)")
print("   • File operations (confirm deletions)")
print("   • API calls (verify destructive actions)")
print("   • Database updates (review changes)")

print("\n⚠️  COMMON MISTAKES:")
print("   1. No HITL → Agent does dangerous things automatically")
print("   2. Interrupt all tools → Agent can't do anything (too restrictive)")
print("   3. Forget thread_id → Can't resume conversation")
print("   4. Don't show user preview → User approves blindly")

print("\n🚀 PRODUCTION CHECKLIST:")
print("   ✓ Identify dangerous tools (send, delete, pay, etc.)")
print("   ✓ Set interrupt_on for those tools only")
print("   ✓ Build UI to show action preview to user")
print("   ✓ Let user approve/reject/edit")
print("   ✓ Use same thread_id when resuming")
print("   ✓ Handle errors (user closes tab, timeout, etc.)")

print("\n📚 NEXT STEPS:")
print("   • Combine HITL with message trimming")
print("   • Add timeout for approval (auto-reject after 5 min)")
print("   • Log all approvals/rejections for audit")
print("   • Build approval UI in your web app")

print("\n" + "=" * 80)
print("🎓 Safety gates = Production ready")
print("=" * 80)
