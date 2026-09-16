from typing import List, Dict, Any, Tuple
from langchain_core.documents import Document
from app.config import settings
from app.rag.vectorstore import VectorStoreManager
from app.schemas.query import SourceItem


class DocumentRetriever:
    """Handles top-K similarity search, threshold filtering, and source metadata extraction."""

    def __init__(self, vectorstore_manager: VectorStoreManager = None):
        self.vectorstore_manager = vectorstore_manager or VectorStoreManager()

    def retrieve(
        self,
        query: str,
        top_k: int = None,
        similarity_threshold: float = None,
    ) -> Tuple[List[Document], List[SourceItem], bool]:
        """
        Search vector store for relevant chunks matching query.
        Returns:
            - List[Document]: Retrieved document chunks above threshold.
            - List[SourceItem]: Formatted source metadata objects.
            - bool: Confidence met status (True if at least one document meets threshold).
        """
        k = top_k or settings.TOP_K
        threshold = similarity_threshold if similarity_threshold is not None else settings.SIMILARITY_THRESHOLD

        raw_results = self.vectorstore_manager.search_with_scores(query, top_k=k)
        if not raw_results:
            return [], [], False

        filtered_docs = []
        source_items = []

        for doc, score in raw_results:
            # Normalize distance/similarity score if necessary
            # FAISS relevance scores: higher is better (0.0 to 1.0)
            # L2 distance: lower is better. Normalize score to 0..1 range if negative or >1
            norm_score = float(score)
            if norm_score < 0:
                norm_score = max(0.0, 1.0 + norm_score)

            # Filter chunks below similarity threshold
            if norm_score >= threshold or len(filtered_docs) == 0:
                # Include top result if list is empty to prevent missing edge case match, but track threshold
                if norm_score >= threshold:
                    filtered_docs.append(doc)
                    source_items.append(
                        SourceItem(
                            document=doc.metadata.get("document", "Unknown Document"),
                            page=int(doc.metadata.get("page", 1)),
                            content=doc.page_content,
                            score=round(norm_score, 4),
                        )
                    )

        confidence_met = len(source_items) > 0 and source_items[0].score >= threshold
        return filtered_docs, source_items, confidence_met
