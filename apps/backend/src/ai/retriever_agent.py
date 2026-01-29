from typing import List
from langchain_core.documents import Document
from .vector_store import vector_store


def retrieve(query: str, n_results: int = 3) -> List[Document]:
    """
    Lightweight retrieval for free-tier deployment.
    """

    results = vector_store.similarity_search(
        query=query,
        k=n_results,
    )

    # 🔍 Debug (safe to keep)
    print("🔎 RETRIEVER DEBUG")
    for doc in results:
        print(
            f"Title: {doc.metadata.get('title')} | Page: {doc.metadata.get('page')}"
        )

    return results
