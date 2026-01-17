from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain.embeddings import HuggingFaceEmbeddings
from typing import List

from ..config import get_settings

settings = get_settings()

# ✅ MUST MATCH EXISTING VECTOR DB (384 dims)
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    collection_name=settings.VECTOR_COLLECTION_NAME,  # pdf_chunks
    persist_directory=str(settings.VECTOR_DB_DIR),
    embedding_function=embedding,
)

def add_documents(documents: List[Document]) -> None:
    if not documents:
        print("⚠️ No documents to add")
        return

    vector_store.add_documents(documents)
    print(f"✅ Added {len(documents)} documents to vector DB")
