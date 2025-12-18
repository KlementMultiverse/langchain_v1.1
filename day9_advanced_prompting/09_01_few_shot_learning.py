"""
  Day 9 - Program 1: Few-Shot Learning
  Teaching AI by showing examples instead of explaining rules
"""

from common_config import get_model
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

print("=" * 60)
print("🎓 FEW-SHOT LEARNING - Teaching AI by Examples")
print("=" * 60)

# Get Groq model (fast & reliable!)
model = get_model(temperature=0.3)  # Low temp = more consistent

examples = [
	{
          "input": "I'm feeling overwhelmed with work.",
          "output": "It sounds like you have a lot on your plate right now. What specific task is stressing you the most?"
        },
        {
          "input": "I can't sleep at night.",
          "output": "Sleep difficulties can be really frustrating. How long has this been happening, and what do you typically do before bed?"
        },
        {
          "input": "I had a fight with my friend.",
          "output": "Conflicts with friends can be painful. Would you like to talk about what happened and how you're feeling about it?"
        }
   ]

example_prompt = ChatPromptTemplate.from_messages([
      ("human", "{input}"),
      ("ai", "{output}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
      example_prompt=example_prompt,
      examples=examples
)

final_prompt = ChatPromptTemplate.from_messages([
      ("system", "You are an empathetic therapist. Respond with understanding and ask thoughtful follow-up questions."),
      few_shot_prompt,
      ("human", "{input}")
  ])

chain = final_prompt | model

# SECTION 7: Test with NEW input (not in examples!)
print("\n🧪 Testing with NEW scenario (AI has never seen this before!):\n")

test_input = "I'm worried about money and paying bills."
print(f"User: {test_input}\n")

response = chain.invoke({"input": test_input})
print(f"AI Therapist: {response.content}")

# SECTION 8: Test another NEW scenario
print("\n" + "=" * 60)
print("🧪 Testing with DIFFERENT scenario:\n")

test_input2 = "My boss criticized me in front of everyone."
print(f"User: {test_input2}\n")
response2 = chain.invoke({"input": test_input2})
print(f"AI Therapist: {response2.content}")

# SECTION 9: Key Takeaways
print("\n" + "=" * 60)
print("✅ WHAT YOU LEARNED:")
print("=" * 60)
print("""
1. Few-Shot Learning = Teaching AI by examples (not rules!)
2. Just 3 examples taught the AI to handle INFINITE scenarios
3. Pattern Recognition: AI learned "empathy + question" approach
4. Temperature matters: 0.3 = consistent, follows examples precisely
5. FewShotChatMessagePromptTemplate = LangChain's teaching tool

🎯 Real-world uses:
   - Customer service bots (show example responses)
   - Code generation (show example code patterns)
   - Translation (show example translations)
   - ANY task where you can provide examples!
""")
