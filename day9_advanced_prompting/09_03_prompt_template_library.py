"""
Day 9 - Program 3: Prompt Template Library
Building reusable prompt templates (production pattern!)
"""

from common_config import get_model
from langchain_core.prompts import ChatPromptTemplate

print("=" * 60)
print("📚 PROMPT TEMPLATE LIBRARY - Reusable Prompts!")
print("=" * 60)

model = get_model(temperature=0.7)

# LIBRARY: Collection of reusable prompt templates
class PromptLibrary:
    """
    Centralized prompt template storage.
    Production best practice: ONE place for all prompts!
    """

    @staticmethod
    def customer_support():
        """Template for customer support responses"""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a friendly customer support agent.
Guidelines:
- Be empathetic and patient
- Acknowledge the customer's concern
- Provide clear, actionable steps
- End with asking if they need more help"""),
            ("human", "{customer_message}")
        ])

    @staticmethod
    def code_reviewer():
        """Template for code review"""
        return ChatPromptTemplate.from_messages([
            ("system", """You are an expert code reviewer.
Guidelines:
- Focus on: bugs, performance, readability, best practices
- Be constructive (explain WHY something is an issue)
- Suggest specific improvements
- Highlight what's done well too!"""),
            ("human", "Review this code:\n\n{code}")
        ])

    @staticmethod
    def content_writer(tone="professional"):
        """Template for content writing with customizable tone"""
        return ChatPromptTemplate.from_messages([
            ("system", f"""You are a skilled content writer.
Tone: {tone}
Guidelines:
- Clear and engaging writing
- Use active voice
- Break into short paragraphs
- Include relevant examples"""),
            ("human", "Write about: {topic}")
        ])

    @staticmethod
    def data_analyst():
        """Template for data analysis"""
        return ChatPromptTemplate.from_messages([
            ("system", """You are a data analyst.
Guidelines:
- Break down complex data into insights
- Use numbers and statistics
- Identify trends and patterns
- Provide actionable recommendations"""),
            ("human", "Analyze this data:\n\n{data}")
        ])

    @staticmethod
    def translator(target_language="Spanish"):
        """Template for translation"""
        return ChatPromptTemplate.from_messages([
            ("system", f"""You are a professional translator.
Target language: {target_language}
Guidelines:
- Preserve the original meaning
- Use natural, native-sounding language
- Maintain the tone and style
- Handle idioms appropriately"""),
            ("human", "Translate: {text}")
        ])

# DEMONSTRATION: Using templates from the library
print("\n" + "=" * 60)
print("🎬 DEMO 1: Customer Support Template")
print("=" * 60)

support_template = PromptLibrary.customer_support()
support_chain = support_template | model

customer_msg = "My order hasn't arrived and it's been 2 weeks! Order #12345"
print(f"\nCustomer: {customer_msg}\n")

response = support_chain.invoke({"customer_message": customer_msg})
print(f"Support Agent:\n{response.content}")

# DEMO 2: Code Reviewer
print("\n" + "=" * 60)
print("🎬 DEMO 2: Code Review Template")
print("=" * 60)

reviewer_template = PromptLibrary.code_reviewer()
reviewer_chain = reviewer_template | model

code_sample = """
def calculate_total(items):
    total = 0
    for i in items:
        total = total + i
    return total
"""

print(f"\nCode to review:{code_sample}")

review = reviewer_chain.invoke({"code": code_sample})
print(f"Code Review:\n{review.content}")

# DEMO 3: Content Writer with custom tone
print("\n" + "=" * 60)
print("🎬 DEMO 3: Content Writer Template (Casual Tone)")
print("=" * 60)

writer_template = PromptLibrary.content_writer(tone="casual and friendly")
writer_chain = writer_template | model

topic = "Why Python is great for beginners"
print(f"\nTopic: {topic}\n")

content = writer_chain.invoke({"topic": topic})
print(f"Content:\n{content.content}")

# DEMO 4: Data Analyst
print("\n" + "=" * 60)
print("🎬 DEMO 4: Data Analyst Template")
print("=" * 60)

analyst_template = PromptLibrary.data_analyst()
analyst_chain = analyst_template | model

data = """
Q1 Sales: $50,000
Q2 Sales: $65,000
Q3 Sales: $58,000
Q4 Sales: $72,000

Customer Satisfaction:
Q1: 78%
Q2: 82%
Q3: 80%
Q4: 85%
"""

print(f"\nData:{data}")

analysis = analyst_chain.invoke({"data": data})
print(f"Analysis:\n{analysis.content}")

# Key Takeaways
print("\n" + "=" * 60)
print("✅ WHAT YOU LEARNED:")
print("=" * 60)
print("""
1. Prompt Library = Collection of reusable templates (production pattern!)
2. Static methods = No need to create class instance
3. Parameterized templates = Customize behavior (like tone, language)
4. Separation of concerns = Prompts in one place, easy to maintain
5. Consistency = Same quality across your entire application

🎯 Real-world benefits:
   - Update ONE template → Changes everywhere
   - Team collaboration (everyone uses same prompts)
   - Version control (track prompt changes in git)
   - A/B testing (compare template versions)
   - Easy to document and review

💡 Pro tips:
   - Keep prompts in separate file (prompts.py)
   - Add docstrings to explain each template
   - Use parameters for customization (tone, language, etc.)
   - Test templates before deploying to production

🚀 This is how production LLM apps organize prompts!
""")
