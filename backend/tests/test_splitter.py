import pytest
from langchain_core.documents import Document
from app.rag.splitter import TextSplitter

def test_text_splitter():
    splitter = TextSplitter(chunk_size=100, chunk_overlap=20)
    long_content = "BMW Service Technician Guide. " * 20
    doc = Document(page_content=long_content, metadata={"document": "test.pdf", "page": 1})
    
    chunks = splitter.split_documents([doc])
    assert len(chunks) > 1
    assert "chunk_id" in chunks[0].metadata
    assert chunks[0].metadata["document"] == "test.pdf"
    assert chunks[0].metadata["page"] == 1
