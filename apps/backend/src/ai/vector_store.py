from typing import List
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from .gemini_client import embed_texts
from ..config import get_settings

settings = get_settings()


class GeminiEmbeddings(Embeddings):
    """
    Lightweight embeddings using Gemini API.
    NO local ML models.
    SAFE for 512 MB RAM.
    """

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return embed_texts(texts)

    def embed_query(self, text: str) -> List[float]:
        return embed_texts([text])[0]


embedding = GeminiEmbeddings()

vector_store = Chroma(
    collection_name=settings.VECTOR_COLLECTION_NAME,
    persist_directory=str(settings.VECTOR_DB_DIR),
    embedding_function=embedding,
)


def add_documents(documents: List[Document]) -> None:
    if not documents:
        print("⚠️ No documents to add")
        return

    vector_store.add_documents(documents)
    print(f"✅ Added {len(documents)} documents to vector DB")
