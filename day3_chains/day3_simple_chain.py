from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

model = ChatOllama(
	model = "qwen3:4b",
	temperature = 0.7
)

prompt = ChatPromptTemplate.from_messages([
	("system"," you are a helpful assitant, Be {style} while responding"),
	("human", " tell me about {topic}")
])

chain = prompt | model

response = chain.invoke({"topic":"Python", "style":"Funny"})

print("answer is   : ", response.content)



