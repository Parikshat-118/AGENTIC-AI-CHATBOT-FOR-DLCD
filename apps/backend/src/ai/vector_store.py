from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import get_settings

settings = get_settings()


embeddings = GoogleGenerativeAIEmbeddings(
    model=settings.GEMINI_EMBED_MODEL_NAME,
    google_api_key=settings.GEMINI_API_KEY,
)


vector_store = Chroma(
    collection_name=settings.VECTOR_COLLECTION_NAME,  # pdf_chunks
    persist_directory=str(settings.VECTOR_DB_DIR),    # apps/backend/data/vector_db
    embedding_function=embeddings,
)
