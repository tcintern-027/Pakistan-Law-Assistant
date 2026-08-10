"""
Text splitting module for the Pakistan Law Assistant.

Splits page-level legal documents into retrieval-friendly chunks while
preserving document metadata required for legal citations.
"""

from collections import defaultdict
from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Legal documents generally benefit from chunks large enough to preserve
# complete legal provisions while remaining focused for retrieval.
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


# Prefer natural boundaries first, then progressively smaller boundaries.
LEGAL_SEPARATORS = [
    "\n\n",
    "\n",
    ". ",
    "; ",
    ", ",
    " ",
    "",
]


def get_text_splitter() -> RecursiveCharacterTextSplitter:
    """Create and return the configured legal-document text splitter."""
    return RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=LEGAL_SEPARATORS,
        length_function=len,
        is_separator_regex=False,
    )


def split_documents(documents: List[Document]) -> List[Document]:
    """
    Split page-level legal documents into smaller retrieval chunks.

    Existing metadata such as source_file and page is preserved.

    Additional metadata:
        chunk_id:
            Globally unique identifier for the chunk.

        chunk_index:
            Zero-based index of the chunk within its source page.
    """
    splitter = get_text_splitter()

    chunks = splitter.split_documents(documents)

    # Track chunk position separately for every source page.
    page_chunk_counts = defaultdict(int)

    for global_index, chunk in enumerate(chunks):
        source_file = chunk.metadata.get("source_file", "unknown")
        page = chunk.metadata.get("page", "unknown")

        page_key = (source_file, page)
        chunk_index = page_chunk_counts[page_key]

        chunk.metadata["chunk_id"] = f"chunk_{global_index:05d}"
        chunk.metadata["chunk_index"] = chunk_index

        page_chunk_counts[page_key] += 1

    return chunks


def get_chunk_stats(chunks: List[Document]) -> dict:
    """Return useful statistics about the generated chunks."""

    if not chunks:
        return {
            "total_chunks": 0,
            "unique_sources": 0,
            "avg_chunk_length": 0,
            "min_chunk_length": 0,
            "max_chunk_length": 0,
        }

    lengths = [len(chunk.page_content) for chunk in chunks]

    sources = {
        chunk.metadata.get("source_file", "unknown")
        for chunk in chunks
    }

    return {
        "total_chunks": len(chunks),
        "unique_sources": len(sources),
        "avg_chunk_length": round(sum(lengths) / len(lengths), 2),
        "min_chunk_length": min(lengths),
        "max_chunk_length": max(lengths),
    }