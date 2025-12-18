"""
Day 9 - Program 2: Chain-of-Thought (CoT) Reasoning
Teaching AI to show its work (think step-by-step)
"""

from common_config import get_model
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

print("=" * 60)
print("🧠 CHAIN-OF-THOUGHT REASONING - Teaching AI to Think!")
print("=" * 60)

# Get Groq model
model = get_model(temperature=0.3)

# SECTION 1: Examples WITH Chain-of-Thought
# Notice: Each example shows REASONING STEPS before the answer!
cot_examples = [
    {
        "question": "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. Each can has 3 tennis balls. How many tennis balls does he have now?",
        "answer": """Let me think step by step:
1. Roger starts with 5 tennis balls
2. He buys 2 cans of tennis balls
3. Each can has 3 balls, so 2 cans = 2 × 3 = 6 balls
4. Total = starting balls + new balls = 5 + 6 = 11 balls

Answer: Roger has 11 tennis balls."""
    },
    {
        "question": "A restaurant has 23 tables. Each table has 4 chairs. If 12 chairs are broken, how many working chairs are there?",
        "answer": """Let me think step by step:
1. Total tables = 23
2. Each table has 4 chairs
3. Total chairs = 23 × 4 = 92 chairs
4. Broken chairs = 12
5. Working chairs = total chairs - broken chairs = 92 - 12 = 80 chairs

Answer: There are 80 working chairs."""
    },
    {
        "question": "Sarah saves $15 per week. After 8 weeks, she spends $45 on a gift. How much money does she have left?",
        "answer": """Let me think step by step:
1. Sarah saves $15 per week
2. After 8 weeks: 8 × $15 = $120 saved
3. She spends $45 on a gift
4. Money left = total saved - spent = $120 - $45 = $75

Answer: Sarah has $75 left."""
    }
]

# SECTION 2: Create CoT prompt template
cot_example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{question}"),
    ("ai", "{answer}")
])

# SECTION 3: Build few-shot CoT prompt
cot_few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=cot_example_prompt,
    examples=cot_examples
)

# SECTION 4: Final prompt with system instructions
cot_final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math tutor. Always think step-by-step and show your reasoning before giving the final answer."),
    cot_few_shot_prompt,
    ("human", "{question}")
])

# SECTION 5: Create chain
cot_chain = cot_final_prompt | model

# SECTION 6: Test with NEW math problem
print("\n🧪 Testing Chain-of-Thought with NEW problem:\n")
test_question = "A bakery makes 48 cupcakes. They sell them in boxes of 6. If they sell 5 boxes, how many cupcakes are left?"
print(f"Question: {test_question}\n")

cot_response = cot_chain.invoke({"question": test_question})
print(f"AI with CoT:\n{cot_response.content}")

# SECTION 7: Compare WITHOUT Chain-of-Thought
print("\n" + "=" * 60)
print("🔬 COMPARISON: What if we DON'T use Chain-of-Thought?")
print("=" * 60)

# Simple prompt WITHOUT step-by-step reasoning
simple_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a math tutor. Answer the question directly."),
    ("human", "{question}")
])

simple_chain = simple_prompt | model

print(f"\nSame Question: {test_question}\n")
simple_response = simple_chain.invoke({"question": test_question})
print(f"AI WITHOUT CoT:\n{simple_response.content}")

# SECTION 8: Test complex reasoning
print("\n" + "=" * 60)
print("🧩 Testing COMPLEX reasoning problem:")
print("=" * 60)

complex_question = "A train leaves Station A at 2 PM traveling at 60 mph. Another train leaves Station B (120 miles away) at 3 PM traveling toward Station A at 80 mph. At what time will they meet?"

print(f"\nQuestion: {complex_question}\n")
complex_response = cot_chain.invoke({"question": complex_question})
print(f"AI with CoT:\n{complex_response.content}")

# SECTION 9: Key Takeaways
print("\n" + "=" * 60)
print("✅ WHAT YOU LEARNED:")
print("=" * 60)
print("""
1. Chain-of-Thought = Teaching AI to show its reasoning steps
2. CoT dramatically improves accuracy on complex problems
3. Examples show the PROCESS, not just the answer
4. AI learns to break problems into smaller steps
5. More explainable = more trustworthy!

🎯 Real-world uses:
   - Math tutoring (show work to students)
   - Medical diagnosis (explain reasoning)
   - Legal analysis (show logical steps)
   - Debugging code (trace through logic)
   - ANY task requiring transparent reasoning!

💡 Pro tip: Use CoT when accuracy matters more than speed!
""")
