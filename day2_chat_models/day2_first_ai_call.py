from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

print("Real AI conversation \n ")
print("=" * 60)

print("Loading Qwen3:4b model on GPU \n")
model = ChatOllama(
	model="qwen3:4b",
	temperature=0.7
)
print("model Loaded \n")

messages = [
	SystemMessage(content="you are a helpful assitant"),
	HumanMessage(content=" What is Langchain")
]

response = model.invoke(messages)
print("Human : ", messages[1].content)
print("AI : ", response.content)

  # Task 2: Follow-up question
print("\n" + "=" * 60)
print("💬 Multi-turn conversation:")
print("=" * 60)

  # Add the AI's previous response to messages
messages.append(response)

  # Ask a follow-up question
Human_msg2 = HumanMessage(content="Can you explain that in simpler terms?") 
messages.append(Human_msg2 )



  # Get second response
print("\n🤖 Asking follow-up question...")
print("\n Human : ",messages[3].content) 

response2 = model.invoke(messages)

print("\n📥 AI Response:")
print("-" * 60)
print(response2.content)
print("-" * 60)

	

