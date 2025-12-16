"""
Production Resume Parser - Two-Pass Approach

Uses two-pass extraction for better results with small models:
1. Extract raw data
2. Clean and structure the output

Author: Klement
Date: December 16, 2025
"""

from langchain_ollama import ChatOllama
from models import Resume, ContactInfo, JobExperience, Education
from config import MODEL_NAME, TEMPERATURE
import json
import re


# Create LLM
llm = ChatOllama(model=MODEL_NAME, temperature=TEMPERATURE)


def two_pass_extract(text: str, extraction_prompt: str, cleanup_prompt: str) -> str:
    """
    Two-pass extraction to handle thinking/verbose models.

    Pass 1: Extract (model may think/explain)
    Pass 2: Clean (extract only the answer)
    """
    # Pass 1: Extract
    response1 = llm.invoke(extraction_prompt.format(text=text[:2000]))
    raw_output = response1.content.strip()

    # Pass 2: Clean
    cleanup = cleanup_prompt.format(raw_output=raw_output)
    response2 = llm.invoke(cleanup)
    clean_output = response2.content.strip()

    return clean_output


def extract_contact(text: str) -> ContactInfo:
    """Extract contact information with two-pass approach"""

    extraction_prompt = """From this resume, extract:
- Name
- Email
- Phone (10 digits only)
- Location (city only)

Resume:
{text}
"""

    cleanup_prompt = """From this text, extract ONLY the contact info in this exact format:
Name: [name]
Email: [email]
Phone: [10 digits]
Location: [city]

Text:
{raw_output}

Answer in exact format above:"""

    result = two_pass_extract(text, extraction_prompt, cleanup_prompt)

    # Parse the cleaned result
    name = "Unknown"
    email = "unknown@example.com"
    phone = "0000000000"
    location = None

    for line in result.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip().lower()
            value = value.strip()

            if 'name' in key:
                name = value
            elif 'email' in key:
                email = value
            elif 'phone' in key:
                phone = re.sub(r'\D', '', value)[:10]
            elif 'location' in key:
                location = value if value else None

    return ContactInfo(
        name=name,
        email=email,
        phone=phone if len(phone) == 10 else "0000000000",
        location=location
    )


def extract_skills(text: str) -> list:
    """Extract skills with two-pass approach"""

    extraction_prompt = """What are the technical skills in this resume?

Resume:
{text}
"""

    cleanup_prompt = """From this text, list ONLY the skill names separated by commas.

Text:
{raw_output}

Skills (comma separated):"""

    result = two_pass_extract(text, extraction_prompt, cleanup_prompt)

    # Parse skills
    skills = [s.strip() for s in result.split(',') if s.strip()]

    # Clean up
    cleaned = []
    for skill in skills[:15]:
        skill = skill.lstrip('0123456789.-•*) ')
        if skill and 2 < len(skill) < 30:
            cleaned.append(skill)

    return cleaned[:10] if cleaned else ["General Skills"]


def extract_summary(text: str) -> str:
    """Extract professional summary"""

    extraction_prompt = """Write a one-sentence professional summary for this candidate.

Resume:
{text}
"""

    cleanup_prompt = """From this text, extract ONLY the professional summary sentence.

Text:
{raw_output}

Summary:"""

    result = two_pass_extract(text, extraction_prompt, cleanup_prompt)

    # Take first sentence
    if '.' in result:
        result = result.split('.')[0] + '.'

    return result[:300] if len(result) > 10 else None


def extract_experience(text: str) -> list:
    """Extract most recent job"""

    extraction_prompt = """What is the most recent job in this resume?

Resume:
{text}
"""

    cleanup_prompt = """From this text, extract job details in this format:
Company: [company]
Title: [title]
Duration: [dates]

Text:
{raw_output}

Answer in exact format:"""

    result = two_pass_extract(text, extraction_prompt, cleanup_prompt)

    # Parse
    try:
        lines = [l for l in result.split('\n') if ':' in l]
        if len(lines) >= 3:
            company = lines[0].split(':', 1)[1].strip()
            title = lines[1].split(':', 1)[1].strip()
            duration = lines[2].split(':', 1)[1].strip()

            return [JobExperience(
                company=company,
                title=title,
                duration=duration,
                responsibilities=[]
            )]
    except:
        pass

    return []


def parse_resume(resume_text: str) -> Resume:
    """
    Parse resume using two-pass extraction.

    Args:
        resume_text: Raw text from resume

    Returns:
        Resume object with structured data
    """
    print("      → Extracting contact info...")
    contact = extract_contact(resume_text)

    print("      → Extracting skills...")
    skills = extract_skills(resume_text)

    print("      → Extracting summary...")
    summary = extract_summary(resume_text)

    print("      → Extracting experience...")
    experience = extract_experience(resume_text)

    resume = Resume(
        contact=contact,
        summary=summary,
        skills=skills,
        experience=experience,
        education=[]
    )

    return resume
