from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"


def load_pdf(file_path: Path) -> list[Document]:
    """Load a single PDF and return its LangChain documents."""
    loader = PyPDFLoader(str(file_path))
    documents = loader.load()

    for document in documents:
        document.metadata["source_file"] = file_path.name

    return documents


def load_legal_documents() -> list[Document]:
    """Load all PDF legal documents from the documents directory."""
    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Legal documents directory not found: {DOCUMENTS_DIR}"
        )

    pdf_files = sorted(DOCUMENTS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            f"No PDF documents found in: {DOCUMENTS_DIR}"
        )

    documents: list[Document] = []

    for pdf_file in pdf_files:
        documents.extend(load_pdf(pdf_file))

    return documents