from fastapi import APIRouter, Query
from src.ai.quiz_agent import generate_quiz_from_pdf

router = APIRouter()


@router.get("/quiz")
def generate_quiz(
    pdf_title: str = Query(...),
    difficulty: str = Query("medium", pattern="^(easy|medium|hard)$"),
    batch: int = Query(1, ge=1),
    batch_size: int = Query(2, ge=1, le=5),
):
    quiz = generate_quiz_from_pdf(
        pdf_title=pdf_title,
        n_questions=batch_size,
        difficulty=difficulty,
    )

   
    return {
        "batch": batch,
        "questions": quiz or []
    }
