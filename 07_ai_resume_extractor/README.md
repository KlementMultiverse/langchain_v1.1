# AI Resume Extractor - Structured Output with Small LLMs

**Extract structured data from resumes using AI (LangChain + Pydantic + Ollama)**

## What This Does

Converts unstructured resume files into clean, structured database records using **Two-Pass Extraction** - a production technique for handling verbose small language models.

**Key Features:**
- 📄 Supports PDF, DOCX, and TXT files
- 🤖 Uses local LLM (Ollama qwen3:4b) - no API costs
- ✅ Validates data with Pydantic models
- 💾 Saves to SQLite database
- 🗑️ Auto-deletes processed files

---

## The Problem: Verbose Models

Small LLM models tend to be "chatty" - they explain their thinking instead of returning clean data.

**Example:**
```
Input: "Extract skills from this resume"
Output: "Well, looking at the resume, I can see Python mentioned in the experience section, and also JavaScript which appears in the projects..."
```

**We need:** `["Python", "JavaScript"]`

---

## The Solution: Two-Pass Extraction

**Pass 1: Extract** (let the model work naturally)
- Ask for information
- Model can think/explain

**Pass 2: Clean** (force structured format)
- Take Pass 1 output
- Ask model to return ONLY structured data
- Get clean result

This technique works with small, local models without needing expensive API calls or function calling features.

---

## Architecture

```
source_folder/ (drop resumes here)
    ↓
file_loader.py (PDF/DOCX/TXT → text)
    ↓
parser_production.py (Two-pass AI extraction)
    ↓
models.py (Pydantic validation)
    ↓
database.py (SQLite storage)
    ↓
Structured data in database ✅
```

---

## Project Structure

```
07_ai_resume_extractor/
├── models.py                 ✅ Pydantic data models
├── file_loader.py            ✅ Load PDF/DOCX/TXT files
├── config.py                 ✅ Settings and prompts
├── parser.py                 ✅ Single-pass parser (simple)
├── parser_production.py      ✅ Two-pass parser (production)
├── database.py               ✅ SQLite operations
├── main.py                   ✅ Main orchestrator
├── requirements.txt          📄 Dependencies
├── source_folder/            📁 Drop resumes here
└── output/                   📁 Exports (future)
```

---

## Installation

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull qwen3:4b

# Clone repo
git clone <your-repo-url>
cd langchain_learning/examples/07_ai_resume_extractor

# Install dependencies (use main venv or create new one)
pip install -r requirements.txt
```

---

## Usage

**1. Drop resume files in `source_folder/`**
```bash
cp your_resume.pdf source_folder/
```

**2. Run the extractor**
```bash
python main.py
```

**3. Check the database**
```bash
sqlite3 resumes.db "SELECT * FROM resumes;"
```

**Output:**
- ✅ Extracted contact info (name, email, phone, location)
- ✅ Skills as JSON array
- ✅ Work experience (company, title, duration)
- ✅ Professional summary
- ✅ Source files deleted

---

## Data Models

### ContactInfo
```python
- name: str (required)
- email: str (required)
- phone: str (required) - 10 digits only
- location: str (optional) - city name only
```

### Resume
```python
- contact: ContactInfo
- summary: str (optional)
- skills: List[str]
- experience: List[JobExperience]
- education: List[Education]
```

---

## Tech Stack

- **LangChain** 1.2+ - AI orchestration
- **Pydantic** 2.10+ - Data validation
- **Ollama** - Local LLM runtime
- **qwen3:4b** - Small, fast model
- **SQLite** - Database
- **PyPDF, python-docx, unstructured** - File loaders

---

## Key Concepts

### 1. Two-Pass Extraction
Handles verbose model output by:
1. Extracting (with flexibility)
2. Cleaning (with structure)

### 2. Pydantic Validation
- Type safety
- Automatic validation
- Clean error messages

### 3. Multi-File Architecture
- Separation of concerns
- Testable components
- Production-ready patterns

### 4. Local LLM Usage
- No API costs
- Privacy (data stays local)
- Works offline

---

## Example Output

**Input:** `resume.pdf`

**Database Record:**
```
id: 1
name: Sarah Chen
email: sarah.chen@email.com
phone: 5559876543
location: Austin
skills: ["Python", "TensorFlow", "SQL", "AWS"]
summary: "Senior Data Scientist with 6 years experience..."
experience: [{"company": "DataCorp", "title": "Senior Data Scientist", "duration": "2021-Present"}]
```

---

## Production Notes

**This approach is valuable when:**
- Using small, local models (4B-7B parameters)
- API costs are a concern
- Privacy matters (data stays local)
- Function calling isn't available

**Alternatives for larger models:**
- Function calling (OpenAI, Anthropic)
- Structured output modes
- Grammar-based sampling

---

## Author

**Klement**
Learning LangChain - Building production AI systems
Date: December 16, 2025

---

## License

MIT

---

## Notes

- Optimized for USA resumes (10-digit phone numbers)
- City-only location format
- Clean phone digits (no formatting)
- All data validated before storage
