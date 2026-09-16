from fastapi import APIRouter, HTTPException, status
from typing import List
from app.config import settings
from app.rag.loader import DocumentLoader
from app.rag.splitter import TextSplitter
from app.rag.vectorstore import VectorStoreManager
from app.rag.retriever import DocumentRetriever
from app.rag.generator import OllamaGenerator
from app.schemas.query import (
    QueryRequest,
    QueryResponse,
    IngestResponse,
    HealthResponse,
    DocumentListResponse,
    DocumentInfo,
)

router = APIRouter()

# Instantiate singletons for managers
vectorstore_manager = VectorStoreManager()
document_loader = DocumentLoader(settings.DOCUMENTS_DIR)
text_splitter = TextSplitter()
retriever = DocumentRetriever(vectorstore_manager)
generator = OllamaGenerator()


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint providing status of API, Ollama connection, and vector index."""
    ollama_ok = generator.is_ollama_available()
    index_ok = vectorstore_manager.is_index_ready()

    # Count loaded documents
    docs_summary = document_loader.get_document_summary()
    doc_count = len(docs_summary)

    status_str = "healthy" if (index_ok or doc_count > 0) else "warning"

    return HealthResponse(
        status=status_str,
        ollama_connected=ollama_ok,
        index_ready=index_ok,
        document_count=doc_count,
        ollama_model=settings.OLLAMA_MODEL,
    )


@router.post("/ingest", response_model=IngestResponse)
def ingest_documents():
    """Trigger PDF ingestion, text splitting, embedding generation, and FAISS index persistence."""
    try:
        raw_docs = document_loader.load_all_documents()
        if not raw_docs:
            return IngestResponse(
                status="warning",
                documents_processed=0,
                chunks_created=0,
                details=[{"message": f"No PDF documents found in {settings.DOCUMENTS_DIR}"}],
            )

        # Count unique PDF files
        pdf_summary = document_loader.get_document_summary()
        unique_docs_count = len(pdf_summary)

        # Split into chunks
        chunks = text_splitter.split_documents(raw_docs)

        # Build and save FAISS index
        vectorstore_manager.build_index(chunks)

        return IngestResponse(
            status="success",
            documents_processed=unique_docs_count,
            chunks_created=len(chunks),
            details=pdf_summary,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document ingestion: {str(e)}",
        )


@router.post("/query", response_model=QueryResponse)
def query_rag(request: QueryRequest):
    """Query RAG pipeline: convert question to embedding, retrieve FAISS chunks, generate grounded answer."""
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Question field cannot be empty.",
        )

    # Check if index is built, auto-ingest if index doesn't exist but PDFs do
    if not vectorstore_manager.is_index_ready():
        raw_docs = document_loader.load_all_documents()
        if raw_docs:
            chunks = text_splitter.split_documents(raw_docs)
            vectorstore_manager.build_index(chunks)
        else:
            return QueryResponse(
                question=question,
                answer=(
                    "No service documents have been ingested yet. Please place BMW service PDFs "
                    "in the data/documents directory and run ingestion."
                ),
                sources=[],
                confidence_met=False,
            )

    # Perform retrieval step (Mandatory retrieval before generation)
    docs, sources, confidence_met = retriever.retrieve(question)

    # Generate answer strictly grounded in retrieved documents
    answer = generator.generate_answer(
        question=question,
        documents=docs,
        sources=sources,
        chat_history=request.chat_history,
        confidence_met=confidence_met,
    )

    return QueryResponse(
        question=question,
        answer=answer,
        sources=sources if confidence_met else [],
        confidence_met=confidence_met,
    )


@router.get("/documents", response_model=DocumentListResponse)
def get_documents():
    """Retrieve list of loaded PDF documents, page counts, chunk stats, and index status."""
    docs_summary = document_loader.get_document_summary()
    index_ready = vectorstore_manager.is_index_ready()

    doc_infos = []
    total_chunks = 0

    if index_ready:
        # Calculate chunks if index loaded
        index = vectorstore_manager.get_or_load_index()
        if index and hasattr(index, "docstore"):
            total_chunks = len(index.docstore._dict)

    for item in docs_summary:
        doc_infos.append(
            DocumentInfo(
                filename=item.get("filename", ""),
                path=item.get("path", ""),
                pages=item.get("pages", 0),
                chunks=total_chunks // max(1, len(docs_summary)) if index_ready else 0,
            )
        )

    return DocumentListResponse(
        documents=doc_infos,
        total_documents=len(doc_infos),
        total_chunks=total_chunks,
        index_ready=index_ready,
    )
