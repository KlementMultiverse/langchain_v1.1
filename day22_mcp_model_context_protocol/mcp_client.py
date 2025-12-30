"""
Day 22: Model Context Protocol (MCP) - Client
Module 2, Lesson 1 - LangChain Academy Foundations
"""

import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

print("🤖 Day 22: Model Context Protocol (MCP)\n")

# Load environment variables
load_dotenv()

print("=" * 70)
print("STEP 1: Create MCP Client and Connect to Server")
print("=" * 70)

# Create client and connect to local server
client = MultiServerMCPClient(
    {
        "local_server": {
            "transport": "stdio",
            "command": "python",
            "args": ["resources/mcp_server.py"],
        }
    }
)

print("✅ Connected to MCP server!")
print("   Server file: resources/mcp_server.py")
print()


async def run_mcp():
    print("=" * 70)
    print("STEP 2: Get Tools, Resources, and Prompts from Server")
    print("=" * 70)

    # Get tools from the server
    tools = await client.get_tools()
    print(f"📦 Tools: {[tool.name for tool in tools]}")

    # Get resources from the server
    resources = await client.get_resources("local_server")
    print(f"📚 Resources: {[r.uri for r in resources]}")

    # Get prompts from the server
    prompt = await client.get_prompt("local_server", "prompt")
    prompt = prompt[0].content
    print(f"\n📝 System Prompt (first 150 chars):")
    print(f"{prompt[:150]}...")
    print()

    print("=" * 70)
    print("STEP 3: Create AI Agent with Tools and Prompt")
    print("=" * 70)

    agent = create_agent(
        model="gpt-5-nano",
        tools=tools,
        system_prompt=prompt
    )

    print("✅ Agent created!")
    print(f"   Model: gpt-5-nano")
    print(f"   Tools: {[tool.name for tool in tools]}")
    print()

    print("=" * 70)
    print("STEP 4: Ask the Agent a Question")
    print("=" * 70)

    question = "Tell me about the langchain-mcp-adapters library"
    print(f"❓ Question: {question}")
    print()

    config = {"configurable": {"thread_id": "1"}}

    response = await agent.ainvoke(
        {"messages": [HumanMessage(content=question)]},
        config=config
    )

    print("=" * 70)
    print("💬 Agent Answer:")
    print("=" * 70)

    final_message = response['messages'][-1].content
    print(f"\n{final_message}\n")

    print("=" * 70)
    print("FULL RESPONSE (with all details):")
    print("=" * 70)
    pprint(response)
    print()


# Run the async function
asyncio.run(run_mcp())

print("\n" + "=" * 70)
print("🎯 KEY LEARNINGS:")
print("=" * 70)
print("""
✅ MCP = Model Context Protocol
   - Standardized way for AI agents to use tools/resources
   - Server provides capabilities, Client uses them

✅ MCP SERVER (resources/mcp_server.py):
   - TOOL: search_web - Action the AI can perform
   - RESOURCE: github_file - Data the AI can read
   - PROMPT: Instructions for the AI

✅ MCP CLIENT (this file):
   1. Connect to server
   2. Get tools/resources/prompts
   3. Create agent with those capabilities
   4. Agent uses tools automatically!

🔑 HOW IT WORKS:
   Client → Launch server → Get tools → Create agent → Ask question
   Agent automatically decides which tools to use!
""")

print("✅ Day 22 Complete!")
