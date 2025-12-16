"""
Resume Parser using AI

Uses LangChain + Ollama to extract structured data from resume text.

Author: Klement
Date: December 15, 2025
"""

from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from models import Resume
from config import MODEL_NAME, TEMPERATURE, EXTRACTION_PROMPT


# ============================================================
# SETUP PARSER
# ============================================================

# Create output parser (converts LLM response to Resume object)
output_parser = PydanticOutputParser(pydantic_object=Resume)

# Create prompt template
prompt_template = PromptTemplate(
    template="{instructions}\n\nResume Text:\n{resume_text}\n\n{format_instructions}",
    input_variables=["resume_text"],
    partial_variables={
        "instructions": EXTRACTION_PROMPT,
        "format_instructions": output_parser.get_format_instructions()
    }
)

# Create LLM
llm = ChatOllama(
    model=MODEL_NAME,
    temperature=TEMPERATURE
)

# Build the chain: Prompt → LLM → Parser
chain = prompt_template | llm | output_parser


# ============================================================
# MAIN FUNCTION
# ============================================================

def parse_resume(resume_text: str) -> Resume:
    """
    Parse resume text and extract structured data using AI.

    Args:
        resume_text: Raw text extracted from resume file

    Returns:
        Resume object with structured data (contact, skills, experience, education)

    Raises:
        Exception: If parsing fails or LLM returns invalid data
    """
    try:
        result = chain.invoke({"resume_text": resume_text})
        return result
    except Exception as e:
        print(f"❌ Parsing failed: {e}")
        raise
