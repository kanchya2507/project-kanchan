import os
from pathlib import Path

from dotenv import load_dotenv

# config.py is in project-api/app/rag/, so parents[2] is project-api/.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


def configured_path(env_name: str, default: Path) -> Path:
    value = os.getenv(env_name)
    path = Path(value) if value else default
    return path if path.is_absolute() else PROJECT_ROOT / path


PDF_DIR = configured_path("RAG_PDF_DIR", PROJECT_ROOT / "data" / "pdfs")
CHROMA_DIR = configured_path("RAG_CHROMA_DIR", PROJECT_ROOT / "data" / "chroma")
COLLECTION_NAME = "devops_interview_docs"

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
EMBEDDING_MODEL = os.getenv(
    "RAG_EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)
TOP_K = int(os.getenv("RAG_TOP_K", "5"))