# Day 15: Prompting

**LangChain Academy - Module 1, Lesson 1.1**

## 📚 What You'll Learn

- Basic prompting (no system prompt)
- System prompts to control AI behavior
- Few-shot learning (teaching by examples)
- Structured prompts (define text format)
- Structured output (Pydantic objects)

## 🗂️ Files

1. **01_basic_prompting.py** - Agent without system prompt
2. **02_system_prompt.py** - Using system prompts to give AI a role
3. **03_few_shot_examples.py** - Teaching AI by showing examples
4. **04_structured_prompts.py** - Defining exact text output format
5. **05_structured_output.py** - Using Pydantic for Python objects (PRODUCTION)

## 🎯 Key Concepts

### Prompting Progression
1. **No prompt** → AI uses default behavior
2. **System prompt** → Give AI a role/instructions
3. **Few-shot examples** → Teach AI by showing examples
4. **Structured prompt** → Define exact text format
5. **Structured output** → Get Python objects (BEST for production)

### System Prompt
- Defines AI's role and behavior
- Sets the tone and expertise level
- Provides instructions and constraints

### Few-Shot Learning
- Provide examples in the system prompt
- AI learns the pattern from examples
- Format: `User: question\nAI: answer`

### Structured Output (Production Pattern)
```python
class CapitalInfo(BaseModel):
    name: str
    location: str
    vibe: str
    economy: str

agent = create_agent(
    model='gpt-5-nano',
    response_format=CapitalInfo  # Returns Python object
)
```

**Why use it:**
- Reliable: AI forced to return valid objects
- Type-safe: Get Python objects with attributes
- Production-ready: No parsing, no errors

## 🚀 How to Run

```bash
cd /home/intruder/langchain_v1.1/day15_prompting
python 01_basic_prompting.py
python 02_system_prompt.py
python 03_few_shot_examples.py
python 04_structured_prompts.py
python 05_structured_output.py
```

## 📖 Related Resources

- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LangChain Prompting Docs](https://docs.langchain.com/concepts/prompts)
