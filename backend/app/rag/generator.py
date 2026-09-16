import httpx
from typing import List, Optional
from langchain_core.documents import Document
from app.config import settings
from app.schemas.query import ChatMessage, SourceItem

SYSTEM_PROMPT = """You are a BMW Service Knowledge Assistant.

Answer the technician's question using ONLY the retrieved service documentation provided below.

Strict Rules:
1. Do not invent procedures, specifications, torque values, warnings, or diagnostic steps.
2. If the retrieved context does not contain enough information to answer the question reliably, state clearly:
   "I couldn't find sufficient information in the available BMW service documentation to answer this question reliably."
3. Cite the source document name and page number whenever providing technical details.
4. For high-voltage/EV procedures, emphasize applicable safety procedures, PPE, and de-energization requirements.
5. Provide a concise, professional, technician-friendly response formatted with clean markdown bullet points.

Context from BMW Service Documentation:
----------------------------------------
{context}
----------------------------------------
"""

NO_INFO_FALLBACK = (
    "I couldn't find sufficient information in the available BMW service documentation "
    "to answer this question reliably."
)


class OllamaGenerator:
    """Generates grounded technical responses using local Ollama LLM."""

    def __init__(
        self,
        base_url: str = None,
        model: str = None,
    ):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL

    def is_ollama_available(self) -> bool:
        """Check if local Ollama service is reachable."""
        try:
            response = httpx.get(f"{self.base_url}/api/tags", timeout=3.0)
            return response.status_code == 200
        except Exception:
            return False

    def format_context(self, documents: List[Document]) -> str:
        """Format retrieved document chunks into prompt context with clear headers."""
        if not documents:
            return "No relevant documentation found."

        context_blocks = []
        for idx, doc in enumerate(documents, 1):
            doc_name = doc.metadata.get("document", "Unknown Document")
            page_num = doc.metadata.get("page", "Unknown Page")
            snippet = doc.page_content.strip()
            block = f"[Source {idx}: Document '{doc_name}', Page {page_num}]\n{snippet}"
            context_blocks.append(block)

        return "\n\n".join(context_blocks)

    def format_chat_history(self, chat_history: List[ChatMessage]) -> str:
        """Format lightweight conversation context."""
        if not chat_history:
            return ""

        formatted = []
        for msg in chat_history[-4:]:  # keep last 4 messages for light context
            role = "Technician" if msg.role == "user" else "Assistant"
            formatted.append(f"{role}: {msg.content}")

        return "\n".join(formatted)

    def generate_answer(
        self,
        question: str,
        documents: List[Document],
        sources: List[SourceItem],
        chat_history: Optional[List[ChatMessage]] = None,
        confidence_met: bool = True,
    ) -> str:
        """
        Generate answer from Ollama LLM using retrieved context.
        If confidence is not met or no documents retrieved, return strict no-info fallback.
        """
        if not confidence_met or not documents or not sources:
            return NO_INFO_FALLBACK

        context_str = self.format_context(documents)
        system_instruction = SYSTEM_PROMPT.format(context=context_str)

        messages = [{"role": "system", "content": system_instruction}]

        # Add light chat history if present
        if chat_history:
            for msg in chat_history[-4:]:
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": question})

        if not self.is_ollama_available():
            # If Ollama is offline, return context-grounded fallback response informing user
            citations_str = "\n".join(
                [f"- **{s.document}** (Page {s.page})" for s in sources]
            )
            return (
                f"[Note: Local Ollama service at {self.base_url} is not running or model '{self.model}' is not loaded.]\n\n"
                f"**Retrieved Service Documentation Relevant to your Question:**\n"
                f"{citations_str}\n\n"
                f"**Extracted Context Snippet:**\n> {documents[0].page_content[:400]}..."
            )

        try:
            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": 0.2,  # Low temperature for strict factual grounding
                    "top_p": 0.9,
                },
            }

            response = httpx.post(
                f"{self.base_url}/api/chat",
                json=payload,
                timeout=60.0,
            )

            if response.status_code == 200:
                data = response.json()
                answer = data.get("message", {}).get("content", "").strip()
                if not answer:
                    return NO_INFO_FALLBACK
                return answer
            elif response.status_code == 404:
                return (
                    f"Error: Ollama model '{self.model}' is not installed.\n"
                    f"Please run `ollama pull {self.model}` in your terminal to install the model."
                )
            else:
                return f"Error communicating with Ollama (HTTP {response.status_code}): {response.text}"

        except Exception as e:
            return f"Error generating answer with local LLM: {str(e)}"
