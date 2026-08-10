from backend.app.loaders import load_legal_documents
from backend.app.splitter import (
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    get_chunk_stats,
    split_documents,
)


def test_split_documents_returns_chunks():
    documents = load_legal_documents()
    chunks = split_documents(documents)

    assert len(documents) == 518
    assert len(chunks) > 0
    assert len(chunks) >= len(documents)


def test_chunk_metadata_preserved():
    documents = load_legal_documents()
    chunks = split_documents(documents)

    assert len(chunks) > 0

    for chunk in chunks[:20]:
        assert "source_file" in chunk.metadata
        assert "page" in chunk.metadata
        assert "chunk_id" in chunk.metadata
        assert "chunk_index" in chunk.metadata

        assert chunk.metadata["source_file"]
        assert chunk.metadata["page"] is not None
        assert chunk.metadata["chunk_id"].startswith("chunk_")


def test_chunk_size_within_bounds():
    documents = load_legal_documents()
    chunks = split_documents(documents)

    oversized = [
        chunk
        for chunk in chunks
        if len(chunk.page_content) > CHUNK_SIZE
    ]

    assert len(oversized) == 0


def test_chunk_stats_shape():
    documents = load_legal_documents()
    chunks = split_documents(documents)

    stats = get_chunk_stats(chunks)

    assert stats["total_chunks"] == len(chunks)
    assert stats["unique_sources"] == 4
    assert stats["avg_chunk_length"] > 0
    assert stats["min_chunk_length"] > 0
    assert stats["max_chunk_length"] <= CHUNK_SIZE


def test_chunk_ids_are_unique():
    documents = load_legal_documents()
    chunks = split_documents(documents)

    chunk_ids = [chunk.metadata["chunk_id"] for chunk in chunks]

    assert len(chunk_ids) == len(set(chunk_ids))


def test_chunk_indexes_start_at_zero_for_each_page():
    documents = load_legal_documents()
    chunks = split_documents(documents)

    page_groups = {}

    for chunk in chunks:
        key = (
            chunk.metadata["source_file"],
            chunk.metadata["page"],
        )

        page_groups.setdefault(key, []).append(
            chunk.metadata["chunk_index"]
        )

    for indexes in page_groups.values():
        assert indexes[0] == 0
        assert indexes == list(range(len(indexes)))