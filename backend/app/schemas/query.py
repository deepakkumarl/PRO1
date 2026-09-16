from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str = Field(..., description="Message sender role: 'user' or 'assistant'")
    content: str = Field(..., description="Message text content")

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="Technician question string")
    chat_history: Optional[List[ChatMessage]] = Field(default=[], description="Lightweight conversation history context")

class SourceItem(BaseModel):
    document: str = Field(..., description="PDF source filename")
    page: int = Field(..., description="Page number (1-indexed)")
    content: str = Field(..., description="Snippet of retrieved text chunk")
    score: float = Field(..., description="Similarity relevance score")

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceItem]
    confidence_met: bool = Field(default=True, description="Whether retrieval confidence met configured threshold")

class IngestResponse(BaseModel):
    status: str
    documents_processed: int
    chunks_created: int
    details: List[Dict[str, Any]] = []

class HealthResponse(BaseModel):
    status: str
    ollama_connected: bool
    index_ready: bool
    document_count: int
    ollama_model: str

class DocumentInfo(BaseModel):
    filename: str
    path: str
    pages: int
    chunks: int

class DocumentListResponse(BaseModel):
    documents: List[DocumentInfo]
    total_documents: int
    total_chunks: int
    index_ready: bool
