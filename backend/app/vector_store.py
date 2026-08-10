"""
ChromaDB vector store for the Pakistan Law Assistant.

Stores embedded legal-document chunks locally and preserves the metadata
needed for source and page-level citations.
"""

from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document

from backend.app.embeddings import get_embeddings


# Persistent ChromaDB location.
CHROMA_DIR = (
    Path(__file__).resolve().parent.parent / "data" / "chroma_db"
)

COLLECTION_NAME = "pakistan_law_documents"


def get_vector_store() -> Chroma:
    """
    Return the persistent ChromaDB vector store.

    The embedding function is the same model used when indexing and
    querying, which is essential for compatible vector dimensions.
    """
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(CHROMA_DIR),
    )


def add_documents(
    documents: List[Document],
) -> Chroma:
    """
    Add document chunks to the persistent ChromaDB collection.

    Returns:
        The initialized Chroma vector store.
    """
    vector_store = get_vector_store()

    if documents:
        vector_store.add_documents(documents)

    return vector_store


def get_collection_count() -> int:
    """Return the number of chunks currently stored in ChromaDB."""
    vector_store = get_vector_store()

    return vector_store._collection.count()