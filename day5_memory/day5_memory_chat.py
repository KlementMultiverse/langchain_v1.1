from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama

model = ChatOllama( model = "qwen3:4b", temperature = 0.7)

conversation_history = []

print("Chatbot with memory")
print("=" * 50)
print(" Type 'exit' to quit \n")

while True:
	user_input = input("You : ")
	if user_input.lower()=='exit':
		break

	conversation_history.append(HumanMessage(content=user_input))
	response = model.invoke(conversation_history)
	conversation_history.append(response)

	print(f" AI : {response.content}")

print(f" \n Total messages in memory : {len(conversation_history)}")

 
