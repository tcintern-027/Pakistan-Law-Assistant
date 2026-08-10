"""
Application configuration for the Pakistan Law Assistant.
"""

from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


class Settings(BaseSettings):
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    CHROMA_PERSIST_DIRECTORY: str = "data/chroma_db"
    CHROMA_COLLECTION_NAME: str = "pakistan_law"

    RETRIEVAL_K: int = 5

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()