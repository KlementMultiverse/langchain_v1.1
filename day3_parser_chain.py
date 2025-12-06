from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatOllama(
	model="qwen3:4b",
	temperature=0.7
)


prompt = ChatPromptTemplate.from_messages([
	("system","you are a helpful assistant, answer in one sentence"),
	("human","{question}")
])

output_parser = StrOutputParser()

  # Chain with 3 steps!
chain = prompt | model | output_parser

  # Run it
answer = chain.invoke({"question": "What is Python?"})
print(type(answer))  # Check the type
print(answer)


