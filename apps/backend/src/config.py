from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    # =========================
    # Gemini / Google AI
    # =========================
    GEMINI_API_KEY: str
    GEMINI_MODEL_NAME: str = "gemini-2.0-flash"
    GEMINI_EMBED_MODEL_NAME: str = "text-embedding-004"

    # =========================
    # Base directory (apps/backend)
    # =========================
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # =========================
    # Knowledge base (local PDFs if still used)
    # =========================
    KB_DIR: Path = BASE_DIR / "kb"

    # =========================
    # Vector DB (Chroma)
    # =========================
    VECTOR_DB_DIR: Path = BASE_DIR / "data" / "vector_db"
    VECTOR_COLLECTION_NAME: str = "pdf_chunks"

    class Config:
        # IMPORTANT: compute path directly, not via BASE_DIR
        env_file = Path(__file__).resolve().parent.parent / ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
