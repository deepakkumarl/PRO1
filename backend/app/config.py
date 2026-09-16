import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Application Settings loaded from environment variables or .env file."""
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2"

    # Embedding Configuration
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    # Chunking Configuration
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 150

    # Retrieval Configuration
    TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.5

    # Storage Paths
    DOCUMENTS_DIR: str = str(BASE_DIR / "data" / "documents")
    VECTORSTORE_DIR: str = str(BASE_DIR / "vectorstore" / "faiss_index")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

settings = Settings()
