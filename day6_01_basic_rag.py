from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage


#step1 . Load document
print("Step 1: Loading document")
loader = TextLoader("day6_RAG_knowledge.txt")
docs = loader.load()

print(f" Loaded document has {len(docs[0].page_content)} characters")
print(f" Preview {docs[0].page_content[:100]}....\n")

 # Step 2: Setup AI model
print("Step 2: Loading AI model...")
model = ChatOllama(model="qwen3:4b", temperature=0.7)
print("✅ Model loaded!\n")

conversation_history = [
			SystemMessage(content=f"answer based on this document {docs[0].page_content}")]
# Step 3: Interactive Q&A with document
print("="*60)
print("RAG Chatbot - Ask questions about the document!")
print("="*60)
print("Type 'exit' to quit\n")

while True:
	question = input("You: ")
	if question.lower() == 'exit':
		break
	# Add user question to conversation history

	conversation_history.append(HumanMessage(content=question))

	# Get AI Response with full conversation context
	response = model.invoke( conversation_history)

	#Add AI Response to the conversation history
	conversation_history.append(response)

	print(f"AI: {response.content} \n")

print(f" Total messages in memory : {len(conversation_history)}")


