"""
SQL Agent - Natural Language to SQL Query

Demonstrates AI agent that writes SQL queries from natural language questions.
Agent automatically explores database schema and generates appropriate queries.

Module: 2 Bonus - SQL Agent
Pattern: Natural language → Schema exploration → SQL generation → Execution
Key Concept: AI handles SQL writing, you validate results
"""

from dotenv import load_dotenv
from langchain_community.utilities import SQLDatabase
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from pprint import pprint

load_dotenv()


# Connect to database
print("Connecting to Chinook music database...")
db = SQLDatabase.from_uri("sqlite:///resources/Chinook.db")

print("\nDatabase schema available to AI:")
print("=" * 70)
print(db.get_table_info())
print("=" * 70)


# Create SQL query tool
@tool
def sql_query(query: str) -> str:
    """Obtain information from the database using SQL queries"""
    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"


# Test the tool
print("\nTesting SQL tool with simple query...")
result = sql_query.invoke("SELECT * FROM Artist LIMIT 10")
print(f"Sample artists: {result[:200]}...")


# Create agent with SQL tool
print("\nCreating AI agent with SQL capability...")
agent = create_agent(
    model="gpt-4o-mini",
    tools=[sql_query]
)


# Test with natural language question
print("\n" + "=" * 70)
print("TESTING NATURAL LANGUAGE TO SQL")
print("=" * 70)

question = HumanMessage(content="Who is the most popular artist beginning with 'S' in this database?")
print(f"\n💬 Question: {question.content}")

print("\n🤖 AI agent processing...")
response = agent.invoke({"messages": [question]})

print("\n" + "=" * 70)
print("FULL CONVERSATION:")
print("=" * 70)
pprint(response['messages'])

print("\n" + "=" * 70)
print("AI-GENERATED SQL QUERY:")
print("=" * 70)
sql_used = response["messages"][-3].tool_calls[0]['args']['query']
print(sql_used)

print("\n" + "=" * 70)
print("FINAL ANSWER:")
print("=" * 70)
print(response["messages"][-1].content)

print("\n" + "=" * 70)
print("✅ SQL Agent Complete")
print("\n💡 Key Learnings:")
print("   - AI explored database schema automatically")
print("   - AI wrote SQL from natural language")
print("   - AI executed query and formatted answer")
print("   - No manual SQL writing required")
print("=" * 70)
