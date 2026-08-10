"""
Embedding model for the Pakistan Law Assistant.

Uses a local Hugging Face sentence-transformer model so that document
embeddings can be generated without an external embedding API.
"""

from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings


EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """
    Create and cache the Hugging Face embedding model.

    The model is loaded once per Python process and reused for all
    embedding and retrieval operations.
    """
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )