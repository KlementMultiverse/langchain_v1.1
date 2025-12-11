from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage

print("="* 60)
print(" Document Loader \n")
print("=" * 60)

# step 1: Ask user  for document filename
filename = input(" \n Enter the Fie Name: ").strip()

#step 2 : Try loading the file with error handling..
try:
	print(f"\n file {filename} loading....\n")
	loader = TextLoader(filename)
	docs = loader.load()
	
	char_count = len(docs[0].page_content)
	word_count = len(docs[0].page_content.split())

	print("Success")
	print(f" characters : {char_count}\n")
	print(f" words : {word_count} \n")
	print(f" preview : {docs[0].page_content[:100]} \n")

except (FileNotFoundError, RuntimeError) as e:
	print(f" Error File {filename} not found \n")
	print(" please check the file and try again \n")
	exit()

#step 3 : Setup AI model
print(" Laoding AI model")
model = ChatOllama( model= "qwen3:4b", temperature=0.7)
print("Model Loaded sucessfully")

#step 4 : Initialize conversation with document in SystemMessage

conversation_history = [
	SystemMessage(content= f" Answer based on this document: {docs[0].page_content}")
]

# step 5 : Interactive Q&A lopp with memory

print("\n" + "="*60)
print(" Ask questions about the document")
print(" type 'exit' to quit \n")

while True:
	question = input("You: ")
	if question == 'exit':
		break

	conversation_history.append(HumanMessage(content=question))
	response = model.invoke(conversation_history)

	conversation_history.append(response)
	
	print(f" AI: {response.content}\n")

# show statistics at the end
print("\n" + "="*60)
print(" Session Statistics :\n")
print(f" Document: {filename}")
print(f" Total messages in memory {len(conversation_history)} \n")
print(f" Questions asked {(len(conversation_history) - 1)//2} \n")
print(" GoodBye")



