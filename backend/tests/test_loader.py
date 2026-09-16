import pytest
from pathlib import Path
from app.rag.loader import clean_text, DocumentLoader
from langchain_core.documents import Document

def test_clean_text():
    raw_text = "  BMW   Service   Manual\n\n\n\nSection 1.1   "
    cleaned = clean_text(raw_text)
    assert "  " not in cleaned
    assert "\n\n\n" not in cleaned
    assert cleaned.startswith("BMW Service Manual")

def test_loader_empty_dir(tmp_path):
    loader = DocumentLoader(str(tmp_path))
    docs = loader.load_all_documents()
    assert isinstance(docs, list)
    assert len(docs) == 0
