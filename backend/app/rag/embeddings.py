from app.config import settings

try:
    from langchain_huggingface import HuggingFaceEmbeddings
except ImportError:
    from langchain_community.embeddings import HuggingFaceEmbeddings


def get_embedding_model():
    """Initialize and return the local HuggingFace Embedding model."""
    model_name = settings.EMBEDDING_MODEL
    encode_kwargs = {"normalize_embeddings": True}
    model_kwargs = {"device": "cpu"}

    embeddings = HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs,
    )
    return embeddings
