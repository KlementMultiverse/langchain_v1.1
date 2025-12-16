"""
Main Resume Extractor

Orchestrates the entire resume extraction pipeline:
1. Load resume files from source folder
2. Extract text using AI
3. Save to database
4. Delete processed files

Author: Klement
Date: December 15, 2025
"""

from pathlib import Path
from config import SOURCE_FOLDER, ensure_folders_exist
from file_loader import load_all_resumes
from parser_production import parse_resume
from database import create_database, save_resume


def main():
    """
    Main execution function.

    Workflow:
    1. Ensure folders and database exist
    2. Load all resumes from source_folder/
    3. Parse each resume with AI
    4. Save to database
    5. Delete processed files
    """
    print("=" * 60)
    print("AI RESUME EXTRACTOR")
    print("=" * 60)

    # Step 1: Setup
    print("\n🔧 Setting up...")
    ensure_folders_exist()
    create_database()

    # Step 2: Load resumes
    print(f"\n📂 Loading resumes from {SOURCE_FOLDER}...")
    resumes_text = load_all_resumes(str(SOURCE_FOLDER))

    if not resumes_text:
        print("📭 No resumes found in source_folder/")
        print("💡 Drop PDF, DOCX, or TXT files in source_folder/ and run again")
        return

    print(f"✅ Found {len(resumes_text)} resume(s)")

    # Step 3: Process each resume
    print("\n🤖 Processing with AI...")
    success_count = 0
    fail_count = 0

    for filename, text in resumes_text.items():
        print(f"\n📄 Processing: {filename}")

        try:
            # Parse with AI
            resume_data = parse_resume(text)

            # Save to database
            save_resume(resume_data)

            # Delete source file
            file_path = SOURCE_FOLDER / filename
            file_path.unlink()
            print(f"🗑️  Deleted: {filename}")

            success_count += 1

        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")
            fail_count += 1

    # Step 4: Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"✅ Successfully processed: {success_count}")
    print(f"❌ Failed: {fail_count}")
    print(f"💾 Database: {create_database.__globals__['DATABASE_FILE']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
