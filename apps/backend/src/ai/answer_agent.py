from typing import List
from langchain_core.documents import Document
from .gemini_client import generate_answer


def classify_intent(query: str) -> str:
    """
    Uses LLM reasoning to classify intent.
    """
    q = query.lower()

    if any(x in q for x in ["define", "definition", "what is"]):
        return "definition"

    if any(x in q for x in ["difference", "compare", "vs"]):
        return "comparison"

    if any(x in q for x in ["numerical", "calculate", "example", "solve"]):
        return "numerical"

    if any(x in q for x in ["list", "applications", "advantages", "disadvantages"]):
        return "list"

    if any(x in q for x in ["explain", "working", "describe"]):
        return "explanation"

    return "exam"   # DEFAULT


def generate_final_answer(
    query: str,
    documents: List[Document],
    plan: dict | None,
) -> dict:

    if not documents:
        return {
            "answer": " No relevant information found in this particuar knowledge base",
            "sources": [],
        }

    MAX_DOCS = 3
    context = "\n\n".join(doc.page_content for doc in documents)

    answer = generate_answer(
        context=context,
        question=(
            f"Answer STRICTLY from the given PDF content.\n"
            f"If the answer is not present, say:\n"
            f"'Not found in the provided knowledge base'\n\n"
            f"Question: {query}"
        ),
    )

    sources = [
        {
            "pdf": d.metadata.get("pdf"),
            "page": d.metadata.get("page"),
            "category": d.metadata.get("category"),
            "title": d.metadata.get("title"),
        }
        for d in documents
    ]

    return {
        "answer": answer,
        "sources": sources,
    }