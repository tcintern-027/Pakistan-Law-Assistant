"""
Groq LLM configuration for the Pakistan Law Assistant.
"""

from functools import lru_cache

from langchain_groq import ChatGroq

from backend.app.config import settings


@lru_cache
def get_llm() -> ChatGroq:
    """
    Return the configured Groq chat model.
    """

    return ChatGroq(
        model=settings.GROQ_MODEL,
        temperature=0.1,
        api_key=settings.GROQ_API_KEY,
    )