"""
Resume File Loader

Loads resume files (PDF, DOCX, TXT) and extracts raw text.
Uses LangChain document loaders for format-specific extraction.

Author: Klement
Date: December 15, 2025
"""

from langchain_community.document_loaders import TextLoader,PyPDFLoader
from langchain_community.document_loaders import UnstructuredWordDocumentLoader
from pathlib import Path

def get_file_extension(file_path: str) -> str:
	"""
	Get file extension in lowercase.
	Args:
	file_path: Path to the file
	Returns:
	File extension (e.g., '.pdf', '.docx', '.txt')
      """
	return Path(file_path).suffix.lower()

def load_resume_file(file_path: str) -> str:
	"""
	Load resume file and extract raw text.
	Supports:
          - PDF files (.pdf)
          - Word documents (.docx)
          - Text files (.txt)
	Args:
	file_path: Path to the resume file 
	Returns:
	Extracted text content as a single string 
	Raises:
	ValueError: If file type is not supported
	FileNotFoundError: If file doesn't exist
	"""

	# Validate if file exists 
	if not Path(file_path).exists():
		raise FileNotFoundError(f"file not found:{file_path}")

	#Detect file type and use appropriate loader
	ext = get_file_extension(file_path)
	if ext == ".pdf":
		loader=PyPDFLoader(file_path)
	elif ext == ".docx":
		loader=UnstructuredWordDocumentLoader(file_path)
	elif ext == ".txt":
		loader=TextLoader(file_path)
	else:
		raise ValueError(f"Unsupported file type: {ext}. Supported: .pdf, .docx, .txt")


	# Load Documents and extract text
	docs = loader.load()
	# Combine all pages/sections into a single text string
	text = "\n".join([doc.page_content for doc in docs])
	return text

def load_all_resumes(source_folder: str) -> dict:
	"""
	Load all resume files from a folder.
	Args:
	source_folder: Path to folder containing resume files 
	Returns:
	Dictionary mapping filename to extracted text
	Example: {"resume1.pdf": "John Doe\n...", "resume2.docx": "Jane Smith\n..."}
	"""
	folder = Path(source_folder)
	if not folder.exists():
		raise FileNotFoundError(f"Folder not found: {source_folder}")
 
	results = {}
	supported_extensions = {".pdf",".docx",".txt"}

	#Get all supporrted files
	for file_path in folder.iterdir():
		if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
			try:
				text = load_resume_file(str(file_path))
				results[file_path.name] = text
				print(f"Loaded {file_path.name}")
			except Exception as e:
				print(f"❌ Failed to load {file_path.name}: {e}")

	return results
 














