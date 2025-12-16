"""
Database Operations

SQLite database operations for storing and retrieving resume data.

Author: Klement
Date: December 15, 2025
"""

import sqlite3
import json
from typing import List, Optional
from models import Resume
from config import DATABASE_FILE


# ============================================================
# DATABASE SETUP
# ============================================================

def create_database():
    """
    Create the resumes database table if it doesn't exist.

    Table structure:
    - id: Auto-increment primary key
    - name: Candidate name
    - email: Email address
    - phone: 10-digit phone number
    - location: City name (optional)
    - summary: Professional summary (optional)
    - skills: JSON list of skills
    - experience: JSON list of job experiences
    - education: JSON list of education entries
    - created_at: Timestamp when record was created
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            location TEXT,
            summary TEXT,
            skills TEXT,
            experience TEXT,
            education TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database ready: {DATABASE_FILE}")


# ============================================================
# SAVE RESUME
# ============================================================

def save_resume(resume: Resume) -> int:
    """
    Save a resume to the database.

    Args:
        resume: Resume object with extracted data

    Returns:
        ID of the inserted record

    Raises:
        sqlite3.Error: If database operation fails
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO resumes (name, email, phone, location, summary, skills, experience, education)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            resume.contact.name,
            resume.contact.email,
            resume.contact.phone,
            resume.contact.location,
            resume.summary,
            json.dumps(resume.skills),
            json.dumps([exp.model_dump() for exp in resume.experience]),
            json.dumps([edu.model_dump() for edu in resume.education])
        ))

        conn.commit()
        resume_id = cursor.lastrowid
        print(f"✅ Saved: {resume.contact.name} (ID: {resume_id})")
        return resume_id

    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        raise
    finally:
        conn.close()


# ============================================================
# QUERY RESUMES
# ============================================================

def get_all_resumes() -> List[dict]:
    """
    Get all resumes from the database.

    Returns:
        List of dictionaries with resume data
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resumes ORDER BY created_at DESC")
    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_resume_by_id(resume_id: int) -> Optional[dict]:
    """
    Get a specific resume by ID.

    Args:
        resume_id: The resume ID to retrieve

    Returns:
        Dictionary with resume data, or None if not found
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM resumes WHERE id = ?", (resume_id,))
    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None


def search_resumes(keyword: str) -> List[dict]:
    """
    Search resumes by keyword (searches name, email, skills).

    Args:
        keyword: Search term

    Returns:
        List of matching resumes
    """
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM resumes
        WHERE name LIKE ? OR email LIKE ? OR skills LIKE ?
        ORDER BY created_at DESC
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ============================================================
# DELETE OPERATIONS
# ============================================================

def delete_resume(resume_id: int) -> bool:
    """
    Delete a resume by ID.

    Args:
        resume_id: The resume ID to delete

    Returns:
        True if deleted, False if not found
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
    conn.commit()

    deleted = cursor.rowcount > 0
    conn.close()

    return deleted


def reset_database():
    """
    Delete all resumes from the database (keep table structure).
    """
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM resumes")
    conn.commit()

    count = cursor.rowcount
    conn.close()

    print(f"✅ Deleted {count} resumes from database")
    return count
