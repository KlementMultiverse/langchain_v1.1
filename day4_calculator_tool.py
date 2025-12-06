from langchain_core.prompts import ChatPromptTemplate
from  langchain_ollama import ChatOllama
from langchain_core.tools import tool

@tool
def multiply(a:int, b:int) -> int:
	" multiply two numbers together"
	return a*b

model =  ChatOllama(
	model = "qwen3:4b",
	temperature=0
)

model_with_tools = model.bind_tools([multiply])

messages = [
	("system","You are a helpful assitant, use tools tools when needed"),
	("human"," what is 25 times 47")
]

prompt = ChatPromptTemplate.from_messages(messages)

chain = prompt | model_with_tools

response = chain.invoke({})

print(response)

print(response.tool_calls)


if response.tool_calls:
      tool_call = response.tool_calls[0]
      args = tool_call['args']
      result = multiply.invoke(args)
      print(f"\n✅ Tool executed! Result: {result}")

