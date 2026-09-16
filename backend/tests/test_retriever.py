import pytest
from unittest.mock import MagicMock
from langchain_core.documents import Document
from app.rag.retriever import DocumentRetriever
from app.schemas.query import SourceItem

def test_retriever_filtering():
    mock_vectorstore = MagicMock()
    doc1 = Document(page_content="Check coolant level and water pump", metadata={"document": "cooling.pdf", "page": 2})
    doc2 = Document(page_content="Tire pressure recommendation", metadata={"document": "tires.pdf", "page": 5})
    
    # Simulate scores (higher is better for relevance score)
    mock_vectorstore.search_with_scores.return_value = [
        (doc1, 0.85),
        (doc2, 0.15),
    ]
    
    retriever = DocumentRetriever(mock_vectorstore)
    docs, sources, confidence = retriever.retrieve("overheating coolant", top_k=2, similarity_threshold=0.5)
    
    assert len(docs) == 1
    assert len(sources) == 1
    assert sources[0].document == "cooling.pdf"
    assert sources[0].page == 2
    assert confidence is True
