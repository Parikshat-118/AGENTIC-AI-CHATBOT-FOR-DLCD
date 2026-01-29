from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import FastEmbedEmbeddings

from ..config import get_settings

settings = get_settings()

# ✅ Local lightweight embeddings (FREE, 512MB RAM safe)
embedding = FastEmbedEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

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
