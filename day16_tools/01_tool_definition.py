"""
LangChain Academy - Module 1 - Lesson 1.2: Tools
Creating tools with @tool decorator
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.tools import tool

# Method 1: Auto-name from function name
@tool
def square_root(x: float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5

# Method 2: Custom tool name
@tool("square_root")
def custom_name_tool(x: float) -> float:
    """Calculate the square root of a number"""
    return x ** 0.5

# Method 3: Custom name and description
@tool("square_root", description="Calculate the square root of a number")
def full_custom_tool(x: float) -> float:
    return x ** 0.5

# Test the tool directly
result = square_root.invoke({"x": 467})
print(f"Square root of 467: {result}")
