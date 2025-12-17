# Pseudocode Planning Examples

Real-world examples from projects showing how to plan before coding.

---

## Example 1: AI Resume Extractor - File Loader Planning

**Date:** December 16, 2025
**Project:** Day 7 - AI Resume Extractor
**Context:** Need to load PDF/DOCX/TXT files and extract text

### 🎯 Goal
Build a function that loads all resume files from a folder and returns their text content.

### 📋 Planning Process (Work Backwards)

**Step 1: What's the final output we need?**
```
Dictionary: { "resume.pdf": "text content here...", "resume2.docx": "more text..." }
```

**Step 2: What do we need to create that output?**
- Loop through all files in folder
- Load each file
- Extract text from each file
- Store in dictionary with filename as key

**Step 3: Break down "Load each file" - what does that need?**
- Determine file type (PDF, DOCX, or TXT)
- Use appropriate loader for that type
- Handle errors if file type not supported

**Step 4: Break down "Determine file type" - what does that need?**
- Get file extension
- Convert to lowercase (for consistency)

### 🏗️ Architecture (Bottom-Up)

```
LAYER 1 (Smallest building blocks):
├── get_file_extension(file_path)
│   └── Returns: ".pdf", ".docx", ".txt"

LAYER 2 (Uses Layer 1):
├── load_resume_file(file_path)
│   ├── Uses: get_file_extension()
│   ├── Chooses: PDF/DOCX/TXT loader
│   └── Returns: text content

LAYER 3 (Uses Layer 2):
└── load_all_resumes(folder_path)
    ├── Uses: load_resume_file()
    ├── Loops through: all files in folder
    └── Returns: dictionary of all texts
```

### 📝 Pseudocode (Before any coding)

```pseudocode
FUNCTION get_file_extension(file_path):
    # Extract extension from path
    # Convert to lowercase
    # Return extension

FUNCTION load_resume_file(file_path):
    # Check if file exists (error handling)
    # Get file extension
    # IF extension is .pdf:
    #     Use PyPDFLoader
    # ELSE IF extension is .docx:
    #     Use WordDocumentLoader
    # ELSE IF extension is .txt:
    #     Use TextLoader
    # ELSE:
    #     Raise error (unsupported type)
    # Load documents
    # Join all pages into one string
    # Return text

FUNCTION load_all_resumes(folder_path):
    # Create empty dictionary
    # Get all files in folder
    # FOR EACH file:
    #     IF file is resume file (not folder):
    #         Get filename
    #         Load text using load_resume_file()
    #         Store in dictionary
    # Return dictionary
```

### 💡 Key Insights

1. **Work backwards from goal**: Start with "what do I want" → work back to "what do I need"

2. **Identify layers**: Each layer uses the layer below it
   - Layer 1: Pure helpers (no dependencies)
   - Layer 2: Uses Layer 1
   - Layer 3: Uses Layer 2

3. **Build bottom-up**: Code Layer 1 first, test it, then Layer 2, then Layer 3

4. **Strategy Pattern**: Different loaders for different file types (PDF/DOCX/TXT)

5. **Error handling planned early**: Check file exists, validate extension

### 🧪 Testing Strategy

```
Test Layer 1 first:
✓ get_file_extension("resume.PDF") → ".pdf"
✓ get_file_extension("doc.DOCX") → ".docx"

Then test Layer 2:
✓ load_resume_file("test.pdf") → returns text
✓ load_resume_file("test.docx") → returns text
✓ load_resume_file("test.xyz") → raises error

Finally test Layer 3:
✓ load_all_resumes("empty_folder") → {}
✓ load_all_resumes("folder_with_files") → {filename: text, ...}
```

---

## Key Lessons

### Before Any Coding:
1. **Understand the goal** - What's the final output?
2. **Work backwards** - What do I need to create that output?
3. **Identify dependencies** - What does each part need?
4. **Plan layers** - Bottom (helpers) to top (main function)
5. **Write pseudocode** - Logic before syntax

### Why This Works:
- **Clear direction**: Know what to build before building
- **Testable units**: Each layer can be tested independently
- **No rework**: Didn't have to rewrite because of poor planning
- **Maintainable**: Easy to understand the structure

### Common Mistakes to Avoid:
- ❌ Starting to code immediately
- ❌ Building top-down (main function first)
- ❌ Not identifying dependencies
- ❌ Skipping pseudocode
- ❌ Not planning error handling

### Instead:
- ✅ Think first, code second
- ✅ Build bottom-up (helpers first)
- ✅ Map out dependencies
- ✅ Write pseudocode in plain language
- ✅ Plan for errors from the start

---

*From this example, we learned that planning takes 10 minutes but saves hours of debugging and refactoring.*
