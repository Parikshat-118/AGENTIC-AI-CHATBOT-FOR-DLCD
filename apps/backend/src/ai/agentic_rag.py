from .retriever_agent import retrieve
from .answer_agent import generate_final_answer


def agentic_answer(query: str, n_results: int = 3) -> dict:
    documents = retrieve(query=query, n_results=n_results)

    final = generate_final_answer(
        query=query,
        documents=documents[:3],  # HARD LIMIT
        plan=None,
    )

    return {
        "query": query,
        "answer": final["answer"],
        "sources": final["sources"],
        "agent_reasoning": {
            "mode": "all-pdfs",
            "retrieved_docs": len(documents),
        },
    }


def agentic_pdf_answer(query: str, pdf_title: str, n_results: int = 3) -> dict:
    documents = retrieve(query=query, n_results=10)

    filtered = [
        d for d in documents
        if d.metadata.get("title") == pdf_title
    ]

    final = generate_final_answer(
        query=query,
        documents=filtered[:3],  # HARD LIMIT
        plan=None,
    )

    return {
        "query": query,
        "pdf_title": pdf_title,
        "answer": final["answer"],
        "sources": final["sources"],
        "agent_reasoning": {
            "mode": "single-pdf",
            "retrieved_docs": len(filtered),
        },
    }
