import os
import re
from pathlib import Path
from typing import List, Dict, Any
from langchain_core.documents import Document

try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader


def clean_text(text: str) -> str:
    """Clean redundant whitespace and line breaks from extracted PDF text."""
    if not text:
        return ""
    # Replace multiple horizontal spaces/tabs with single space
    text = re.sub(r"[ \t]+", " ", text)
    # Replace more than two consecutive newlines with two newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    # Strip leading and trailing whitespace
    return text.strip()


class DocumentLoader:
    """Document loader that scans directory for PDF files and extracts text page by page."""

    def __init__(self, documents_dir: str):
        self.documents_dir = Path(documents_dir)

    def load_pdf(self, pdf_path: Path) -> List[Document]:
        """Extract text from a single PDF document page by page."""
        documents = []
        try:
            reader = PdfReader(str(pdf_path))
            total_pages = len(reader.pages)

            for page_idx, page in enumerate(reader.pages):
                raw_text = page.extract_text() or ""
                cleaned = clean_text(raw_text)

                if cleaned:
                    metadata = {
                        "document": pdf_path.name,
                        "page": page_idx + 1,
                        "source": str(pdf_path),
                        "total_pages": total_pages,
                    }
                    doc = Document(page_content=cleaned, metadata=metadata)
                    documents.append(doc)
        except Exception as e:
            print(f"Error reading PDF {pdf_path.name}: {e}")

        return documents

    def load_all_documents(self) -> List[Document]:
        """Find and parse all PDF files inside the configured documents directory."""
        if not self.documents_dir.exists():
            return []

        pdf_files = sorted(list(self.documents_dir.glob("*.pdf")))
        all_docs = []

        for pdf_file in pdf_files:
            docs = self.load_pdf(pdf_file)
            all_docs.extend(docs)

        return all_docs

    def get_document_summary(self) -> List[Dict[str, Any]]:
        """Retrieve overview metadata for all PDFs in documents directory."""
        if not self.documents_dir.exists():
            return []

        summary = []
        for pdf_file in sorted(list(self.documents_dir.glob("*.pdf"))):
            try:
                reader = PdfReader(str(pdf_file))
                summary.append({
                    "filename": pdf_file.name,
                    "path": str(pdf_file),
                    "pages": len(reader.pages),
                    "size_bytes": pdf_file.stat().st_size
                })
            except Exception as e:
                summary.append({
                    "filename": pdf_file.name,
                    "path": str(pdf_file),
                    "pages": 0,
                    "error": str(e)
                })
        return summary
