"""
Legal-aware hybrid retrieval layer for the Pakistan Law Assistant.

Retrieval strategy:
1. Semantic retrieval from ChromaDB
2. Exact legal-reference retrieval
3. Legal phrase matching
4. Semantic + lexical reranking
5. Lightweight penalties for poor chunks
"""

import re

from langchain_core.documents import Document

from backend.app.vector_store import get_vector_store


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _extract_legal_references(query: str) -> list[str]:
    """
    Extract references such as:
        Article 10A
        Article 25A
        Section 302
        Section 154
    """
    normalized = _normalize(query)

    references = re.findall(
        r"\b(article|section)\s+(\d+[a-z]?)\b",
        normalized,
    )

    return [
        f"{reference_type} {number}"
        for reference_type, number in references
    ]


def _extract_query_terms(query: str) -> list[str]:
    normalized = _normalize(query)
    terms = []

    terms.extend(_extract_legal_references(query))

    important_phrases = [
        "fair trial",
        "due process",
        "fundamental right",
        "freedom of speech",
        "freedom of expression",
        "right to education",
        "right to information",
        "right to life",
        "death penalty",
        "life imprisonment",
        "electronic crimes",
        "cyber crime",
        "criminal liability",
        "private defence",
        "bail",
        "pre-arrest bail",
        "post-arrest bail",
    ]

    for phrase in important_phrases:
        if phrase in normalized:
            terms.append(phrase)

    stop_words = {
        "what",
        "does",
        "is",
        "are",
        "the",
        "a",
        "an",
        "of",
        "to",
        "in",
        "on",
        "for",
        "and",
        "or",
        "with",
        "under",
        "which",
        "what's",
        "explain",
        "tell",
        "me",
        "about",
        "please",
        "can",
        "you",
    }

    words = re.findall(r"\b[a-z0-9]+\b", normalized)

    for word in words:
        if len(word) >= 3 and word not in stop_words:
            terms.append(word)

    return list(dict.fromkeys(terms))


def _reference_matches(
    reference: str,
    document: Document,
) -> bool:
    """
    Check whether a document actually contains the legal reference.

    Handles PDF formats such as:

        Article 10A
        10A.
        10A.
        Section 302
        302.
    """

    text = _normalize(document.page_content)

    match = re.match(
        r"(article|section)\s+(\d+[a-z]?)",
        reference,
    )

    if not match:
        return False

    number = match.group(2)

    # Match the legal number itself rather than requiring
    # the PDF to contain the literal phrase "Article 10A".
    return bool(
        re.search(
            rf"\b{re.escape(number)}\b",
            text,
        )
    )


def _exact_reference_documents(
    query: str,
    vector_store,
) -> list[Document]:
    """
    Retrieve documents containing an exact legal reference directly
    from Chroma's document store.

    This is important because semantic similarity can miss highly
    specific legal references such as Article 10A.
    """

    references = _extract_legal_references(query)

    if not references:
        return []

    documents = []

    for reference in references:
        match = re.match(
            r"(article|section)\s+(\d+[a-z]?)",
            reference,
        )

        if not match:
            continue

        number = match.group(2)

        try:
            result = vector_store.get(
                where_document={
                    "$contains": number
                },
                include=["documents", "metadatas"],
            )
        except Exception:
            continue

        raw_documents = result.get("documents") or []
        metadatas = result.get("metadatas") or []

        for index, text in enumerate(raw_documents):
            if not text:
                continue

            metadata = (
                metadatas[index]
                if index < len(metadatas)
                else {}
            )

            document = Document(
                page_content=text,
                metadata=metadata or {},
            )

            if _reference_matches(reference, document):
                documents.append(document)

    return documents


def _lexical_score(
    query: str,
    document: Document,
) -> float:
    text = _normalize(document.page_content)
    terms = _extract_query_terms(query)

    if not terms:
        return 0.0

    score = 0.0

    for term in terms:

        # Exact legal reference
        if term.startswith("article ") or term.startswith("section "):
            match = re.match(
                r"(article|section)\s+(\d+[a-z]?)",
                term,
            )

            if match:
                number = match.group(2)

                if re.search(
                    rf"\b{re.escape(number)}\b",
                    text,
                ):
                    score += 30.0

            continue

        occurrences = text.count(term)

        if occurrences == 0:
            continue

        # Important legal phrase
        if " " in term:
            score += 8.0 * min(occurrences, 3)

        # Normal keyword
        else:
            score += 1.0 * min(occurrences, 5)

    return score


def _document_penalty(document: Document) -> float:
    text = _normalize(document.page_content)

    penalty = 0.0

    if "contents" in text:
        penalty += 5.0

    if "articles pages" in text:
        penalty += 5.0

    if len(text) < 300:
        penalty += 2.0

    return penalty


def retrieve_documents(
    query: str,
    k: int = 5,
    semantic_k: int = 20,
) -> list[Document]:

    if not query.strip():
        return []

    vector_store = get_vector_store()

    # ---------------------------------------------------------
    # 1. Semantic retrieval
    # ---------------------------------------------------------

    semantic_documents = vector_store.similarity_search(
        query,
        k=semantic_k,
    )

    # ---------------------------------------------------------
    # 2. Exact legal-reference retrieval
    # ---------------------------------------------------------

    exact_documents = _exact_reference_documents(
        query,
        vector_store,
    )

    # ---------------------------------------------------------
    # 3. Merge candidates without duplicates
    # ---------------------------------------------------------

    candidates = []

    seen = set()

    for document in (
        exact_documents + semantic_documents
    ):
        chunk_id = document.metadata.get("chunk_id")

        identifier = (
            chunk_id
            or (
                document.metadata.get("source_file"),
                document.metadata.get("page"),
                document.page_content[:100],
            )
        )

        if identifier in seen:
            continue

        seen.add(identifier)
        candidates.append(document)

    # ---------------------------------------------------------
    # 4. Score candidates
    # ---------------------------------------------------------

    scored_candidates = []

    semantic_rank = {}

    for rank, document in enumerate(
        semantic_documents
    ):
        identifier = document.metadata.get(
            "chunk_id"
        )

        if identifier:
            semantic_rank[identifier] = rank

    for document in candidates:

        chunk_id = document.metadata.get(
            "chunk_id"
        )

        rank = semantic_rank.get(
            chunk_id,
            semantic_k,
        )

        semantic_rank_score = (
            max(
                semantic_k - rank,
                0,
            )
            / semantic_k
        )

        lexical_score = _lexical_score(
            query,
            document,
        )

        penalty = _document_penalty(
            document
        )

        exact_reference_bonus = 0.0

        references = _extract_legal_references(
            query
        )

        for reference in references:
            if _reference_matches(
                reference,
                document,
            ):
                exact_reference_bonus += 50.0

        final_score = (
            exact_reference_bonus
            + lexical_score
            + semantic_rank_score
            - penalty
        )

        scored_candidates.append(
            (
                final_score,
                document,
            )
        )

    # ---------------------------------------------------------
    # 5. Final ranking
    # ---------------------------------------------------------

    scored_candidates.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        document
        for _, document in scored_candidates[:k]
    ]