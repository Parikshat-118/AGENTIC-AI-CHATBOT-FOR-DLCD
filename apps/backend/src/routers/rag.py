from fastapi import APIRouter, Query
from src.ai.agentic_rag import agentic_answer, agentic_pdf_answer

router = APIRouter()


def is_greeting(text: str) -> bool:
    if not text:
        return False

    greetings = {
        "hi", "hello", "hey", "hii", "hola",
        "good morning", "good afternoon", "good evening",
    }

    msg = text.lower().strip()
    return msg in greetings or any(msg.startswith(g + " ") for g in greetings)



@router.get("/answer")
def answer(
    query: str = Query(...),
    n_results: int = Query(5),
):
    if is_greeting(query):
        return {
            "answer": (
                "👋 Hello! I’m **ElectroMentor**, your Digital Electronics assistant.\n\n"
                "Ask me anything related to digital electronics or your study PDFs."
            )
        }

    return agentic_answer(
        query=query,
        n_results=n_results
    )



@router.get("/pdf-answer")
def pdf_answer(
    query: str = Query(...),
    pdf_title: str = Query(...),
    n_results: int = Query(5),
):
    if is_greeting(query):
        return {
            "answer": (
                f"👋 You’re studying **{pdf_title}**.\n"
                "Ask me anything from this document."
            )
        }

    return agentic_pdf_answer(
        query=query,
        pdf_title=pdf_title,
        n_results=n_results,
    )
