import os
from pathlib import Path
from typing import List, Optional, Tuple
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from app.config import settings
from app.rag.embeddings import get_embedding_model


class VectorStoreManager:
    """Manages FAISS vector store creation, persistence, and loading."""

    def __init__(self, index_dir: str = None):
        self.index_dir = Path(index_dir or settings.VECTORSTORE_DIR)
        self.embedding_model = get_embedding_model()
        self.vector_store: Optional[FAISS] = None

    def is_index_ready(self) -> bool:
        """Check if persistent FAISS index files exist on disk."""
        faiss_file = self.index_dir / "index.faiss"
        pkl_file = self.index_dir / "index.pkl"
        return faiss_file.exists() and pkl_file.exists()

    def build_index(self, documents: List[Document]) -> FAISS:
        """Create a new FAISS vector store from document chunks and persist to disk."""
        if not documents:
            raise ValueError("Cannot build FAISS index with empty document list.")

        self.vector_store = FAISS.from_documents(
            documents=documents, embedding=self.embedding_model
        )
        self.save_index()
        return self.vector_store

    def save_index(self):
        """Save the current FAISS vector store to disk."""
        if self.vector_store is None:
            raise ValueError("No active FAISS vector store to save.")

        self.index_dir.mkdir(parents=True, exist_ok=True)
        self.vector_store.save_local(str(self.index_dir))

    def load_index(self) -> Optional[FAISS]:
        """Load an existing FAISS index from disk."""
        if not self.is_index_ready():
            return None

        self.vector_store = FAISS.load_local(
            folder_path=str(self.index_dir),
            embeddings=self.embedding_model,
            allow_dangerous_deserialization=True,
        )
        return self.vector_store

    def get_or_load_index(self) -> Optional[FAISS]:
        """Get currently active in-memory index or load from disk if available."""
        if self.vector_store is not None:
            return self.vector_store
        return self.load_index()

    def search_with_scores(
        self, query: str, top_k: int = None
    ) -> List[Tuple[Document, float]]:
        """Perform similarity search with relevance scores."""
        index = self.get_or_load_index()
        if index is None:
            return []

        k = top_k or settings.TOP_K
        # FAISS search_with_relevance_scores or similarity_search_with_score
        try:
            results = index.similarity_search_with_relevance_scores(query, k=k)
        except Exception:
            # Fallback to similarity_search_with_score
            results = index.similarity_search_with_score(query, k=k)
        return results
