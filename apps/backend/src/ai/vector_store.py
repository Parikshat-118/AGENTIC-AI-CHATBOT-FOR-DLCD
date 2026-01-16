from langchain_chroma import Chroma
from langchain_core.documents import Document
from typing import List

from ..config import get_settings

settings = get_settings()

# Chroma persists automatically in new versions
vector_store = Chroma(
    collection_name=settings.VECTOR_COLLECTION_NAME,
    persist_directory=str(settings.VECTOR_DB_DIR),
)

def add_documents(documents: List[Document]) -> None:
    """
    Add documents to Chroma vector store.
    Persistence is automatic (no .persist() needed).
    """
    if not documents:
        print(" No documents to add")
        return

    vector_store.add_documents(documents)
    print(f"✅ Added {len(documents)} documents to vector DB")
