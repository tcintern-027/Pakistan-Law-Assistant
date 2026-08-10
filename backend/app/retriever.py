"""
Legal-aware hybrid retrieval layer for the Pakistan Law Assistant.

Combines:
1. Semantic retrieval from ChromaDB
2. Exact legal-reference matching
3. Important legal phrase matching
4. Lightweight penalties for table-of-contents chunks
"""

import re

from langchain_core.documents import Document

from backend.app.vector_store import get_vector_store


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _extract_query_terms(query: str) -> list[str]:
    normalized = _normalize(query)
    terms = []

    legal_references = re.findall(
        r"\b(?:article|section)\s+\d+[a-z]?\b",
        normalized,
    )
    terms.extend(legal_references)

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


def _lexical_score(query: str, document: Document) -> float:
    text = _normalize(document.page_content)
    terms = _extract_query_terms(query)

    if not terms:
        return 0.0

    score = 0.0

    for term in terms:
        occurrences = text.count(term)

        if occurrences == 0:
            continue

        if term.startswith("article ") or term.startswith("section "):
            score += 15.0 * min(occurrences, 2)

        elif " " in term:
            score += 6.0 * min(occurrences, 3)

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

    candidates = vector_store.similarity_search(
        query,
        k=semantic_k,
    )

    scored_candidates = []

    for rank, document in enumerate(candidates):
        lexical_score = _lexical_score(query, document)

        semantic_rank_score = (
            semantic_k - rank
        ) / semantic_k

        penalty = _document_penalty(document)

        final_score = (
            lexical_score * 2.0
            + semantic_rank_score
            - penalty
        )

        scored_candidates.append(
            (final_score, document)
        )

    scored_candidates.sort(
        key=lambda x: x[0],
        reverse=True,
    )

    return [
        document
        for _, document in scored_candidates[:k]
    ]
