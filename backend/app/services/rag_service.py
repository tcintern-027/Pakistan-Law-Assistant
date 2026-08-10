"""
RAG service for the Pakistan Law Assistant.

Connects:
    User question
        ↓
    Hybrid retriever
        ↓
    Legal context
        ↓
    Legal RAG prompt
        ↓
    Groq LLM
        ↓
    Grounded answer
"""

from backend.app.config import settings
from backend.app.llm import get_llm
from backend.app.prompt import LEGAL_RAG_PROMPT
from backend.app.retriever import retrieve_documents


def _format_context(documents) -> str:
    """
    Format retrieved documents into a source-aware context string.
    """

    if not documents:
        return "No relevant legal documents were retrieved."

    context_parts = []

    for index, document in enumerate(documents, start=1):
        metadata = document.metadata

        source = (
            metadata.get("source_file")
            or metadata.get("source")
            or "Unknown source"
        )

        page = metadata.get("page")

        if isinstance(page, int):
            page = page + 1

        page_text = f"Page {page}" if page is not None else "Page unknown"

        context_parts.append(
            f"[Source {index}]\n"
            f"Document: {source}\n"
            f"{page_text}\n"
            f"Content:\n{document.page_content}"
        )

    return "\n\n".join(context_parts)


def ask_question(question: str) -> dict:
    """
    Retrieve relevant legal documents and generate a grounded answer.
    """

    if not question.strip():
        raise ValueError("Question cannot be empty.")

    documents = retrieve_documents(
        question,
        k=settings.RETRIEVAL_K,
    )

    context = _format_context(documents)

    prompt = LEGAL_RAG_PROMPT.format_messages(
        context=context,
        question=question,
    )

    response = get_llm().invoke(prompt)

    sources = []

    for document in documents:
        metadata = document.metadata

        source = (
            metadata.get("source_file")
            or metadata.get("source")
            or "Unknown source"
        )

        page = metadata.get("page")

        if isinstance(page, int):
            page = page + 1

        sources.append(
            {
                "source": source,
                "page": page,
                "chunk_id": metadata.get("chunk_id"),
                "chunk_index": metadata.get("chunk_index"),
            }
        )

    return {
        "question": question,
        "answer": response.content,
        "sources": sources,
    }