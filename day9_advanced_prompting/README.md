# 🧠 Day 9: Advanced Prompt Engineering

**Master Few-Shot Learning, Chain-of-Thought, and Production Prompt Patterns**

---

## 🎯 What You'll Learn

Day 9 teaches the most powerful prompting techniques used in production AI systems:

1. **Few-Shot Learning** - Teach AI by showing examples (not rules!)
2. **Chain-of-Thought (CoT)** - Make AI show its reasoning step-by-step
3. **Prompt Template Library** - Organize prompts like production code
4. **Combined Techniques** - Few-Shot + CoT = Maximum Power! 🔥

---

## 📂 Programs

| Program | Concept | What It Teaches |
|---------|---------|-----------------|
| `09_01_few_shot_learning.py` | Few-Shot | Pattern recognition from 3 examples |
| `09_02_chain_of_thought.py` | CoT Reasoning | Step-by-step problem solving |
| `09_03_prompt_template_library.py` | Organization | Reusable prompt templates |
| `09_04_combined_few_shot_cot.py` | 🔥 POWER | Few-Shot + CoT together |

---

## 🚀 Setup

### Prerequisites
```bash
# You should already have from previous days:
# - Python 3.12+
# - langchain, langchain-core

# NEW for Day 9:
pip install langchain-groq python-dotenv
```

### API Configuration
```bash
# Copy the example .env file
cp .env.example .env

# Edit .env and add your GROQ API key:
# GROQ_API_KEY=your_key_here
# Get free key at: https://console.groq.com
```

---

## 🎓 Running the Programs

### Program 1: Few-Shot Learning
```bash
python 09_01_few_shot_learning.py
```

**What happens:**
- Shows 3 example conversations (therapist style)
- AI learns the empathy + question pattern
- Tests with NEW scenarios it's never seen
- Proves: 3 examples → infinite applications!

---

### Program 2: Chain-of-Thought
```bash
python 09_02_chain_of_thought.py
```

**What happens:**
- Examples show step-by-step math reasoning
- AI learns to break problems into steps
- Compares WITH vs WITHOUT CoT
- Result: More accurate + explainable!

---

### Program 3: Prompt Template Library
```bash
python 09_03_prompt_template_library.py
```

**What happens:**
- Demonstrates reusable prompt templates
- Customer support, code review, content writing, data analysis
- Shows how production apps organize prompts
- One template → used everywhere!

---

### Program 4: Combined Few-Shot + CoT 🔥
```bash
python 09_04_combined_few_shot_cot.py
```

**What happens:**
- Few-shot examples that CONTAIN step-by-step reasoning
- Most powerful prompting technique!
- This is how GPT-4, Claude work in production
- Pattern + Reasoning = MAGIC ✨

---

## 🧠 Key Concepts

### Few-Shot Learning
```python
examples = [
    {"input": "problem 1", "output": "solution 1"},
    {"input": "problem 2", "output": "solution 2"},
    {"input": "problem 3", "output": "solution 3"}
]
# AI learns the pattern → applies to NEW problems!
```

**Key Insight:** AI learns by pattern recognition (like humans!)

---

### Chain-of-Thought (CoT)
```python
answer = """
Let me solve this step by step:
Step 1: Identify what we know
Step 2: Calculate X
Step 3: Apply formula
Answer: Result
Key insight: Why this works
"""
```

**Key Insight:** Transparent reasoning = Higher accuracy

---

### Combined: Few-Shot + CoT
```python
examples = [
    {"question": "...", "answer": """
    Step 1: ...  ← CoT reasoning
    Step 2: ...
    Answer: ...
    """}  # ← Few-shot example WITH CoT!
]
```

**Key Insight:** Nested techniques = Production-grade AI

---

## 💡 Real-World Applications

### Few-Shot Learning
- Customer support bots
- Content generation
- Code completion
- Translation

### Chain-of-Thought
- Math tutoring
- Medical diagnosis
- Legal analysis
- Code debugging

### Combined
- Educational platforms
- Complex decision systems
- High-stakes applications
- Any task requiring explainability

---

## 🔥 The Secret Sauce

**Most people think:**
```
Few-Shot = One technique
CoT = Another technique
```

**Reality:**
```
Few-Shot (container)
    └── CoT (content of each example)

Examples CONTAIN step-by-step reasoning!
```

This is how production AI systems achieve:
- ✅ Consistency (from Few-Shot pattern)
- ✅ Accuracy (from CoT reasoning)
- ✅ Explainability (transparent steps)

---

## 📊 Expected Output

### Program 1 (Few-Shot)
```
User: I'm worried about money
AI: Financial stress can be a heavy burden. Have you identified
     which bills are causing the most concern?
```
✅ Learned empathy + question pattern!

### Program 2 (CoT)
```
Step 1: Total cupcakes = 48
Step 2: Boxes sold = 5 × 6 = 30
Step 3: Remaining = 48 - 30 = 18
Answer: 18 cupcakes left
```
✅ Shows all work!

### Program 4 (Combined)
```
Step 1: Find adults = 60% of 150 = 90
Step 2: Revenue from adults = 90 × $50 = $4500
Step 3: Children = 150 - 90 = 60
Step 4: Revenue from children = 60 × $30 = $1800
Step 5: Total = $4500 + $1800 = $6300

Key insight: Break into parts, calculate separately, sum
```
✅ Pattern + Reasoning = POWER!

---

## 🎯 What Makes Day 9 Special

**This is NOT basic prompting!**

These are the exact techniques used by:
- OpenAI (GPT-4 prompting best practices)
- Anthropic (Claude prompt engineering)
- Google (PaLM/Gemini instruction tuning)
- Production AI companies

**You're learning industry-standard patterns!**

---

## 📚 Next Steps

After Day 9, you can:
1. **Practice**: Write your own Few-Shot + CoT prompts
2. **Experiment**: Try different temperatures (0.3 vs 0.7)
3. **Build**: Create a prompt library for your domain
4. **Combine**: Use with Day 8 streaming for real-time AI

---

## 🐛 Troubleshooting

**Issue:** "GROQ_API_KEY not found"
- Check `.env` file exists
- Verify API key is correct
- Ensure `python-dotenv` is installed

**Issue:** "Module not found"
- Run: `pip install langchain-groq python-dotenv`

**Issue:** "Rate limit exceeded"
- Groq free tier has limits
- Add delay between calls: `time.sleep(1)`

---

## 🚀 Ready?

```bash
# Start with Program 1
python 09_01_few_shot_learning.py

# Master all 4 programs
# Then practice writing your own prompts!
```

---

**"Few-Shot + CoT = The secret sauce of production AI"** 🔥

*This is how the pros do it!*
