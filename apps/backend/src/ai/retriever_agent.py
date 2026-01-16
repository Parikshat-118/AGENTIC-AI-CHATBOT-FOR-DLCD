# src/ai/retriever_agent.py

from typing import List
from langchain_core.documents import Document
from .vector_store import vector_store

def retrieve(query: str, n_results: int = 5) -> List[Document]:
    results = vector_store.similarity_search(
        query=query,
        k=n_results,
    )

    # 🔍 DEBUG (keep this)
    print("🔎 RETRIEVER DEBUG")
    for doc in results:
        print(
            f"Title: {doc.metadata.get('title')} | Page: {doc.metadata.get('page')}"
        )

    return results
