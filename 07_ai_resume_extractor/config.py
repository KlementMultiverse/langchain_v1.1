"""
Configuration Settings

Centralizes all settings, paths, and AI prompts for the resume extractor.

Author: Klement
Date: December 15, 2025
"""

from pathlib import Path

# ============================================================
# PROJECT PATHS
# ============================================================

# Base directory (where this config.py file is located)
BASE_DIR = Path(__file__).parent

# Folder paths
SOURCE_FOLDER = BASE_DIR / "source_folder"
OUTPUT_FOLDER = BASE_DIR / "output"

# Database file
DATABASE_FILE = BASE_DIR / "resumes.db"


# ============================================================
# OLLAMA MODEL SETTINGS
# ============================================================

MODEL_NAME = "qwen3:4b"
TEMPERATURE = 0.1  # Low temperature for consistent extraction


# ============================================================
# AI EXTRACTION PROMPT
# ============================================================

EXTRACTION_PROMPT = """Extract resume information and return ONLY valid JSON.

Extract:
- name (required)
- email (required)
- phone: 10 digits only, no formatting (required)
- location: city name only (optional)
- summary: professional summary (optional)
- skills: list of skills
- experience: list with company, title, duration, responsibilities
- education: list with institution, degree, field, year

Return ONLY the JSON, no explanations."""


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def ensure_folders_exist():
	"""
	Create source and output folders if they don't exist.

	Call this at program startup to ensure required folders are present.
	"""
	SOURCE_FOLDER.mkdir(exist_ok=True)
	OUTPUT_FOLDER.mkdir(exist_ok=True)
	print(f"✅ Folders ready: {SOURCE_FOLDER}, {OUTPUT_FOLDER}")


