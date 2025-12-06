from langchain_core.messages import AIMessage,SystemMessage, HumanMessage

sys_msg = SystemMessage(content = "You are a mathematician assistant")

hum_msg = HumanMessage(content = " what is 2+2 ?")

ai_msg = AIMessage(content = " 2 + 2 equals 4")

conversation = [sys_msg, hum_msg, ai_msg]

for msg in conversation:
    print(f" {type(msg).__name__} : {msg.content}")

hum_msg2 = HumanMessage(content = " what is 5 *3")
ai_msg2 = AIMessage(content = " 5 * 3 equals to 15")

print("\n--- New Conversation turn---")
print("Human:", hum_msg2.content)
print("AI:", ai_msg2.content)

conversation = [ sys_msg, hum_msg, ai_msg, hum_msg2, ai_msg2]

for i, msg in enumerate(conversation, 1):
      msg_type = type(msg).__name__  # Gets the message type
      print(f"{i}. {msg_type}: {msg.content}")
	
