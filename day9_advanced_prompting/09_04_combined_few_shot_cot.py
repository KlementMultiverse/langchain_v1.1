"""
Day 9 - BONUS: Combining Few-Shot + Chain-of-Thought
The MOST POWERFUL prompting technique!
"""

from common_config import get_model
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

print("=" * 60)
print("🚀 COMBINING FEW-SHOT + CoT - Maximum Power!")
print("=" * 60)

model = get_model(temperature=0.3)

# THE SECRET: Examples that show BOTH pattern AND reasoning!
combined_examples = [
    {
        "question": "A store has a 20% off sale. If a shirt costs $50, what's the final price?",
        "answer": """Let me solve this step by step:

Step 1: Identify what we know
- Original price: $50
- Discount: 20% off

Step 2: Calculate the discount amount
- 20% of $50 = 0.20 × $50 = $10

Step 3: Subtract discount from original price
- Final price = $50 - $10 = $40

Answer: The final price is $40.

Key insight: When you see "X% off", multiply the percentage (as decimal) by the price to get the discount amount, then subtract from original."""
    },
    {
        "question": "If a car travels 240 miles in 4 hours, what's its average speed?",
        "answer": """Let me solve this step by step:

Step 1: Identify the formula
- Speed = Distance ÷ Time

Step 2: Identify what we know
- Distance: 240 miles
- Time: 4 hours

Step 3: Apply the formula
- Speed = 240 miles ÷ 4 hours = 60 miles per hour

Answer: The average speed is 60 mph.

Key insight: Speed problems always use the formula: Speed = Distance ÷ Time. Remember this relationship!"""
    },
    {
        "question": "A recipe serves 4 people but you need to serve 10. If it calls for 2 cups of flour, how much do you need?",
        "answer": """Let me solve this step by step:

Step 1: Find the scaling factor
- Original servings: 4 people
- Needed servings: 10 people
- Scaling factor = 10 ÷ 4 = 2.5

Step 2: Identify ingredients to scale
- Original flour: 2 cups

Step 3: Apply scaling factor
- New flour amount = 2 cups × 2.5 = 5 cups

Answer: You need 5 cups of flour.

Key insight: Recipe scaling is multiplication. Find the ratio (new ÷ old), then multiply ALL ingredients by that ratio."""
    }
]

# Create the combined few-shot + CoT prompt
example_template = ChatPromptTemplate.from_messages([
    ("human", "{question}"),
    ("ai", "{answer}")
])

few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_template,
    examples=combined_examples
)

# Final prompt: System message + Examples + User question
final_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert tutor who teaches by showing clear reasoning.

ALWAYS follow this structure:
1. Break problems into clear steps
2. Show ALL calculations
3. Explain the final answer
4. Provide a key insight or learning point

This helps students LEARN, not just get answers!"""),
    few_shot_prompt,
    ("human", "{question}")
])

# Create chain
chain = final_prompt | model

# TEST 1: Math problem
print("\n" + "=" * 60)
print("🧪 TEST 1: New Math Problem")
print("=" * 60)

question1 = "A pizza is cut into 8 slices. If 3 friends share it equally, how many slices does each person get? (Answer can be a fraction)"

print(f"\nQuestion: {question1}\n")
response1 = chain.invoke({"question": question1})
print(f"AI Response:\n{response1.content}")

# TEST 2: Real-world problem
print("\n" + "=" * 60)
print("🧪 TEST 2: Real-World Problem")
print("=" * 60)

question2 = "You have $100 budget. You buy 3 books at $12 each and 2 notebooks at $5 each. How much money is left?"

print(f"\nQuestion: {question2}\n")
response2 = chain.invoke({"question": question2})
print(f"AI Response:\n{response2.content}")

# TEST 3: Complex multi-step
print("\n" + "=" * 60)
print("🧪 TEST 3: Complex Multi-Step Problem")
print("=" * 60)

question3 = "A gym has 150 members. 60% are adults, and the rest are children. If the monthly fee is $50 for adults and $30 for children, what's the total monthly revenue?"

print(f"\nQuestion: {question3}\n")
response3 = chain.invoke({"question": question3})
print(f"AI Response:\n{response3.content}")

# Compare: What if we DIDN'T use Few-Shot + CoT?
print("\n" + "=" * 60)
print("📊 COMPARISON: Without Few-Shot + CoT")
print("=" * 60)

simple_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful math assistant."),
    ("human", "{question}")
])

simple_chain = simple_prompt | model

print(f"\nSame Question: {question3}\n")
simple_response = simple_chain.invoke({"question": question3})
print(f"AI WITHOUT Few-Shot + CoT:\n{simple_response.content}")

# Key Takeaways
print("\n" + "=" * 60)
print("✅ THE POWER OF COMBINING TECHNIQUES:")
print("=" * 60)
print("""
🔥 Few-Shot + CoT = MOST POWERFUL prompting technique!

How it works:
1. Few-Shot examples show the AI WHAT to do (pattern)
2. CoT reasoning shows the AI HOW to think (step-by-step)
3. Combined = AI learns to apply pattern WITH reasoning!

Benefits:
✅ Higher accuracy (AI thinks through problems)
✅ Explainable results (you see the reasoning)
✅ Consistent quality (follows example pattern)
✅ Educational value (teaches, doesn't just answer)
✅ Catches mistakes (AI spots errors in its own logic)

When to use:
- Math/logic problems
- Complex analysis
- Educational applications
- When transparency matters
- High-stakes decisions

Production tip:
class PromptLibrary:
    @staticmethod
    def math_tutor():
        # Few-shot examples with CoT reasoning
        return combined_few_shot_cot_template

    @staticmethod
    def code_debugger():
        # Few-shot examples showing debugging steps
        return combined_debugging_template

🚀 This is how GPT-4, Claude, and other top models are used in production!

The formula:
Few-Shot (pattern) + CoT (reasoning) + Good examples = 🔥 MAGIC 🔥
""")
