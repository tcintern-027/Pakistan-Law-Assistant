from pathlib import Path

from backend.app.loaders import load_legal_documents


def test_legal_documents_are_loaded():
    documents = load_legal_documents()

    assert documents
    assert len(documents) > 0


def test_documents_have_content():
    documents = load_legal_documents()

    assert all(document.page_content.strip() for document in documents)


def test_documents_have_source_metadata():
    documents = load_legal_documents()

    assert all(document.metadata.get("source_file") for document in documents)


def test_document_directory_exists():
    documents_dir = (
        Path(__file__).resolve().parent.parent
        / "backend"
        / "data"
        / "documents"
    )

    assert documents_dir.exists()
    assert list(documents_dir.glob("*.pdf"))