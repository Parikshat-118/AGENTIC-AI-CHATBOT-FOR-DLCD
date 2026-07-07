from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):

    GROQ_API_KEY: str
    GROQ_MODEL_NAME: str       # Read from .env (no hardcoded default)

    GEMINI_EMBED_MODEL_NAME: str = "models/embedding-001"

    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    KB_DIR: Path = BASE_DIR / "kb"

    VECTOR_DB_DIR: Path = BASE_DIR / "data" / "vector_db"
    VECTOR_COLLECTION_NAME: str = "pdf_chunks"

    class Config:
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
