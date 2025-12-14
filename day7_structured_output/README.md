# Day 7: Structured Output with Pydantic + LangChain

**Mastering data extraction from unstructured text using LLMs**

## 🎯 What This Is

A complete guide to extracting structured, validated data from unstructured text using LangChain 1.1 and Pydantic v2. This is THE production pattern for building reliable AI data extraction systems.

## 🔧 Tech Stack

- **LangChain**: 1.1.3 (December 2025)
- **langchain-ollama**: 0.2.0+
- **Pydantic**: v2
- **Ollama**: qwen3:4b (local LLM)
- **Python**: 3.10+

## 📚 Programs Overview

### 1️⃣ `01_pydantic_basics.py`
**Foundation: Data validation with Pydantic**

- Create Pydantic models with type hints
- Automatic validation (catches bad data)
- Type safety for production code

**Key Concept**: Define your data structure once, get validation everywhere.

```python
class Person(BaseModel):
    name: str
    age: int
    email: str
```

---

### 2️⃣ `02_field_descriptions.py`
**Guide the LLM: Field descriptions and constraints**

- Add descriptions to fields (tells LLM what to extract)
- Set constraints (min/max values)
- View JSON Schema (what LLM actually sees)

**Key Concept**: Field descriptions are instructions for the LLM.

```python
age: int = Field(description="Age in years", ge=0, le=120)
```

**Production Tip**: Use `model_json_schema()` to debug extraction issues!

---

### 3️⃣ `03_optional_vs_required.py`
**Control what's mandatory: Required vs Optional fields**

- Required fields: No default value
- Optional fields: Has default value or `Optional[type]`
- LLM sees `"required"` list in JSON Schema

**Key Rule**:
```python
name: str                    # Required (no default)
city: str = "Unknown"        # Optional (has default)
email: Optional[str] = None  # Optional (can be None)
```

---

### 4️⃣ `04_nested_models.py`
**Complex structures: Nested Pydantic models**

- Model real-world data (Person → Address)
- Validate entire hierarchies
- Handle lists of nested objects

**Real-World Examples**:
- Invoice → List[LineItem]
- Resume → List[JobExperience]
- Order → List[Product]

```python
class Person(BaseModel):
    name: str
    address: Address  # Nested model
    jobs: List[JobExperience]  # List of nested models
```

---

### 5️⃣ `05_langchain_structured_output.py` ⭐
**THE BIG ONE: LangChain + Pydantic = Production Data Extraction**

**What it does**:
- Connects Pydantic models to LLM
- Extracts structured data from messy text
- Validates all output automatically
- Outputs JSON ready for database/API

**The Flow**:
```
Unstructured Text → LLM → JSON → Pydantic Validation → Type-Safe Object
```

**Key Method** (December 2025):
```python
model = ChatOllama(model="qwen3:4b", temperature=0)
structured_llm = model.with_structured_output(PersonInfo)
result = structured_llm.invoke(text)  # Returns validated PersonInfo object!
```

**Features Demonstrated**:
1. ✅ Extract all fields from text
2. ✅ Handle missing optional fields (graceful defaults)
3. ✅ Prompt engineering (guide LLM with instructions)
4. ✅ Convert to JSON for database (`model_dump()`)

**Production Pattern**:
```python
# Define structure
class PersonInfo(BaseModel):
    name: str = Field(description="Full name")
    age: int = Field(description="Age in years")
    city: str = Field(description="City name only")
    occupation: Optional[str] = Field(default=None)

# Connect to LLM
structured_llm = model.with_structured_output(PersonInfo)

# Extract data
text = "Meet John Smith, 30 years old, living in NYC. Software engineer."
person = structured_llm.invoke(text)

# person.name, person.age, person.city are GUARANTEED to be correct types!
# Save to database
db.save(person.model_dump())
```

---

## 🚀 How to Run

```bash
# 1. Activate virtual environment
source venv_langchain_dec2025/bin/activate

# 2. Run any program
python 01_pydantic_basics.py
python 02_field_descriptions.py
python 03_optional_vs_required.py
python 04_nested_models.py
python 05_langchain_structured_output.py
```

---

## 💡 Key Learnings

### **1. Why Pydantic + LLM?**

**Without Pydantic** (raw LLM output):
```json
{"name": "John", "age": "thirty"}  ❌ Age is string!
```
Your code crashes when you try `age + 5`.

**With Pydantic** (validated):
```python
person.age  # ALWAYS int, NEVER string
```
ValidationError thrown immediately if LLM outputs bad data.

---

### **2. The Validation Flow**

```
LLM Output (untrusted) → Pydantic (validator) → Your Code (safe!)
```

Think of Pydantic as a security checkpoint that catches bad data before it reaches your application.

---

### **3. Field Descriptions = LLM Instructions**

```python
# ❌ Vague
city: str

# ✅ Clear
city: str = Field(description="City name only, without state or country")
```

The LLM reads these descriptions and extracts accordingly!

---

### **4. Prompt Engineering Matters**

When field descriptions aren't enough, add instructions to the input text:

```python
text = """
Extract person information. For city, extract ONLY the city name.

Text: Meet Alice Cooper, 35-year-old data scientist in Austin, Texas.
"""
```

This guides the LLM to extract "Austin" (not "Austin, Texas").

---

### **5. December 2025 Best Practice**

**Use the DEFAULT method** with Ollama:
```python
# ✅ Recommended (uses constrained decoding)
structured_llm = model.with_structured_output(PersonInfo)

# ❌ Avoid (field name mismatches)
structured_llm = model.with_structured_output(PersonInfo, method="json_mode")
```

The default method uses Ollama's native structured output feature (added March 2025) which enforces exact field names.

---

## 🏭 Production Use Cases

This pattern is used in:

- **Resume Parsing**: Extract skills, experience, education
- **Invoice Processing**: Extract line items, totals, dates
- **Customer Support**: Extract intent, sentiment, priority
- **Document Analysis**: Extract entities, relationships
- **Data Migration**: Clean and validate legacy data
- **API Integration**: Transform unstructured responses to typed objects

---

## 🎓 What's Next?

**After mastering structured output, you can:**
- Build production data extraction pipelines
- Create reliable document processing systems
- Combine with RAG for knowledge extraction
- Add streaming for real-time extraction
- Scale to multi-document processing

---

## 📊 Progression

```
01_pydantic_basics.py        → Validation foundation
02_field_descriptions.py     → Guide the LLM
03_optional_vs_required.py   → Control mandatory fields
04_nested_models.py          → Complex structures
05_langchain_structured_output.py → PRODUCTION PATTERN ⭐
```

Each program builds on the previous one, culminating in a complete production-ready extraction system.

---

## 🔥 Key Takeaway

**Structured output = The bridge between messy real-world text and clean database records.**

Master this pattern and you can build production AI systems that reliably extract, validate, and store data from any text source.

---

**Author**: Klement
**Date**: December 13-14, 2025
**LangChain Version**: 1.1.3
**Status**: Production-Ready ✅
