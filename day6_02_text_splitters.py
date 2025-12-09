from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage,HumanMessage

print("=" * 60)
print("Iteration 2: Text Splitters  and basic Chunk search")
print("=" * 60)

# Step 1  :  Ask user for document from (6b)
filename = input("\n Enter the filename : ").strip()

# step 2 : Laod the document with error handling....
try:
	print(f" \n Loading '{filename}'....")
	loader = TextLoader(filename)
	docs = loader.load()

	char_count =  len(docs[0].page_content)
	word_count = len(docs[0].page_content.split())
	
	print(f"\n  Characters count : {char_count}")
	print(f" words count : {word_count}")

except (FileNotFoundError, RuntimeError):
	print(f"\n Error Laoding {filename}")
	print("check the file and try again")

	exit()

# Step 3 :  Split the loaded Doc
print("\n" + "=" * 60)
print(" Splitting the document into chunks")
print("=" * 60)

text_splitter = RecursiveCharacterTextSplitter(
	chunk_size = 500, chunk_overlap = 50)


chunks = text_splitter.split_documents(docs)

print(f"\n Document split into {len(chunks)} chunks!")
print(f" Original size is {char_count} characters")
print(" Each chunk is 500 characters")

# Step 4 : Show 3 sample chunks

for i in range(min(3, len(chunks))):
	print(f"\n Chunk {i+1} : ")
	print(f" length of Chunk : {len(chunks[0].page_content)} chars")
	print(f" Preview : {chunks[0].page_content[:80]}")

# Step 5 :Setup AI Model
print( " Model Loading....")
model = ChatOllama( model = "qwen3:4b", temperature = 0.7)
print(" Model Loaded Succesfully")

#Step 6 : Interactive Q&A with Conversation History
print("\n" + "=" * 60 )
print(" Ask Questions")
print("AI will remember converssations and search chunks")
print("=" * 60)
print(" Type 'exit' to quit \n")

conversation_history= []

while True:
	question = input(" You: ").strip()
	if question.lower() == 'exit':
		break

	# Search the chunks
	print(f"\n Searching {len(chunks)} chunks!...")

	# Extract keywords from question
	question_words = question.lower().split()
	relevant_chunks = []

	# Find chunks that contain question keywords - TRACK INDEX!
	for idx, chunk in enumerate(chunks):
		chunk_text = chunk.page_content.lower()
		if any(word in chunk_text for word in question_words):
			# Store BOTH chunk content AND its index number
			relevant_chunks.append((idx, chunk.page_content))

	if len(relevant_chunks) == 0:
		print(" No relevant chunks found! \n ")
		continue


	print(f" \n Found {len(relevant_chunks)} relevant chunks!")

	# take only top 3 chunks as of now
	top_chunks_with_idx = relevant_chunks[:3]

	# Extract just the content for context
	top_chunks = [content for idx, content in top_chunks_with_idx]
	context =" \n\n".join(top_chunks)

	# Show which chunks were selected!
	chunk_numbers = [idx for idx, content in top_chunks_with_idx]
	print(f" Using {len(top_chunks)} chunks: {chunk_numbers}")
	print(f" Total context: {len(context)} chars")

	# Show preview of each selected chunk
	print("\n 📄 Selected Chunks Preview:")
	for idx, content in top_chunks_with_idx:
		preview = content[:100] + "..." if len(content) > 100 else content
		print(f"   Chunk #{idx}: {preview}")
	

	# Build Messages with context and conversation_history
	#Add context as SystemMessage

	messages = [SystemMessage(content = f"Answer ONLY using the following context. Do not use your own knowledge. If the answer is not in the context, say 'I don't know'.\n\nContext:\n{context}")]
	
	# Add previous conversation 
	messages.extend(conversation_history)
	
	# Add current question
	messages.append(HumanMessage(content = question))

	# Get AI Response
	response = model.invoke(messages)

 	#save to conversation history
	conversation_history.append(HumanMessage(content = question))
	conversation_history.append(response)
	
	print(f"\n AI: {response.content}\n")













 































