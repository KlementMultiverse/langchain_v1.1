# AI Resume Extractor

**Extract structured data from resumes using AI (LangChain + Pydantic + Ollama)**

## What This Does

Takes messy resume files (PDF, DOCX, TXT) and extracts clean, structured data:
- Contact info (name, email, phone, location)
- Skills
- Work experience
- Education

**Input:** Resume file (any format)
**Output:** Clean JSON data ready for database

---

## The Plan (What We're Building)

```
User drops resumes → source_folder/
↓
Run program (python main.py)
↓
AI extracts structured data
↓
Saves to SQLite database
↓
Deletes processed files
↓
User can query/export from database
```

---

## Project Structure

```
07_ai_resume_extractor/
├── models.py           ✅ DONE - Data structure (Pydantic models)
├── file_loader.py      🔜 TODO - Load PDF/DOCX/TXT files
├── config.py           🔜 TODO - Settings and prompts
├── parser.py           🔜 TODO - AI extraction logic
├── database.py         🔜 TODO - SQLite operations
├── main.py             🔜 TODO - Main program
├── reset_db.py         🔜 TODO - Reset database utility
├── source_folder/      📁 Drop resumes here
├── output/             📁 Exported files go here
└── README.md           📄 This file
```

---

## What We've Built So Far

### ✅ models.py (Completed)

**4 Pydantic Models:**

**1. ContactInfo**
```python
- name: str (required)
- email: str (required)
- phone: str (required) - 10 digits, no formatting
- location: str (optional) - City only
```

**2. JobExperience**
```python
- company: str
- title: str
- duration: str
- responsibilities: List[str]
```

**3. Education**
```python
- institution: str
- degree: str
- field: str (optional)
- year: str (optional)
```

**4. Resume (Main Model)**
```python
- contact: ContactInfo
- summary: str (optional)
- skills: List[str]
- experience: List[JobExperience]
- education: List[Education]
```

**Why Pydantic?**
- Validates data automatically
- Type safety (ensures email is string, phone is 10 digits, etc.)
- Easy conversion to JSON for database

**Example:**
```python
from models import Resume, ContactInfo, JobExperience, Education

resume = Resume(
    contact=ContactInfo(
        name="Sarah Martinez",
        email="sarah@email.com",
        phone="5557890123",
        location="Austin"
    ),
    skills=["Python", "SQL", "Tableau"],
    experience=[
        JobExperience(
            company="TechFlow",
            title="Product Manager",
            duration="2021-Present",
            responsibilities=["Led team of 10", "Launched $6M product"]
        )
    ],
    education=[
        Education(
            institution="UT Austin",
            degree="MBA",
            year="2019"
        )
    ]
)

# Convert to JSON for database
resume_json = resume.model_dump()
```

---

## Tech Stack

- **Python**: 3.10+
- **LangChain**: 1.2.0+ (AI orchestration)
- **Pydantic**: 2.10+ (data validation)
- **Ollama**: Local LLM (qwen3:4b model)
- **Document Loaders**: pypdf, python-docx, unstructured
- **Database**: SQLite (built-in)

---

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify Ollama is running
ollama list  # Should show qwen3:4b
```

---

## Current Status

**Completed:**
- ✅ Project structure setup
- ✅ Dependencies installed
- ✅ Data models defined (models.py)
- ✅ Unit tests passed (all 10 tests)
- ✅ Sample resumes collected (PDF, DOCX, TXT)

**Next Steps:**
- 🔜 Build file_loader.py (load PDF/DOCX/TXT)
- 🔜 Build config.py (settings)
- 🔜 Build parser.py (AI extraction)
- 🔜 Build database.py (storage)
- 🔜 Build main.py (orchestrator)

---

## Learning Concepts

**Day 7 Concepts Applied:**
1. **Pydantic BaseModel** - Data validation
2. **Field descriptions** - Guide AI extraction
3. **Optional vs Required** - Mandatory vs optional fields
4. **Nested models** - Models inside models (Resume contains JobExperience)
5. **Type hints** - str, int, List[str], Optional[str]

**Production Patterns:**
- Separation of concerns (each file has one job)
- Type safety (Pydantic validation)
- Modular architecture (reusable components)
- Unit testing (verify code works)

---

## Author

**Klement**
Learning LangChain 1.0 - Building production-grade AI systems
Date: December 15, 2025

---

## Notes

- USA resumes only (phone format: 10-digit US numbers)
- Location: City name only, no state
- Phone: Clean digits only, extensions removed
- All data validated before storage
- Designed for real-world resume parsing scenarios
