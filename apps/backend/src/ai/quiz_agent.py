# src/ai/quiz_agent.py

import json
import re
import random
from typing import List

from .gemini_client import generate_text
from .vector_store import vector_store


QUIZ_PROMPT_TEMPLATE = """
You are an exam question generator for Electronics engineering students.

STRICT RULES (DO NOT BREAK):
- Use ONLY the study material provided
- Generate EXACTLY {n_questions} MCQs
- Difficulty level: {difficulty}
- Ask ONLY text-based questions
- DO NOT ask questions that depend on figures, diagrams, or images
- DO NOT mention figure numbers (e.g., Fig., Figure 4.3)
- 4 options per question
- Exactly ONE correct answer
- DO NOT add explanations
- DO NOT add headings
- DO NOT use markdown
- DO NOT include any text outside JSON
- OUTPUT MUST BE VALID JSON ARRAY

FORMAT:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "Correct option text"
  }}
]

Study Material:
{context}
"""


def _extract_json(text: str):
    if not text:
        return None

    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    if not text.endswith("]"):
        return None

    try:
        return json.loads(text)
    except Exception:
        return None


def _normalize(text: str) -> str:
    return text.strip().lower()


def _apply_difficulty(chunks: List[str], difficulty: str) -> List[str]:
    n = len(chunks)
    if n == 0:
        return []

    if difficulty == "easy":
        return chunks[: max(1, int(0.3 * n))]

    if difficulty == "hard":
        return chunks[int(0.7 * n):]

    return chunks[int(0.3 * n): int(0.7 * n)]


def generate_quiz_from_pdf(
    pdf_title: str,
    n_questions: int = 10,
    difficulty: str = "medium",
):
    """
    Generate MCQ quiz with retry + fallback logic
    """

    SAFE_QUESTIONS = min(n_questions, 5)
    raw = vector_store.get(include=["documents", "metadatas"])

   

    matched = [
        text
        for text, meta in zip(raw["documents"], raw["metadatas"])
        if _normalize(meta.get("title", "")) == _normalize(pdf_title)
    ]

    
    if not matched:
        matched = [
            text
            for text, meta in zip(raw["documents"], raw["metadatas"])
            if _normalize(pdf_title) in _normalize(meta.get("title", ""))
        ]

    if not matched:
        print(f" No chunks found for PDF: {pdf_title}")
        return []

    

    filtered = _apply_difficulty(matched, difficulty)
    if not filtered:
        filtered = matched

    selected_chunks = random.sample(
        filtered,
        k=min(2, len(filtered))
    )

    context = "\n\n".join(selected_chunks)

    

    MAX_RETRIES = 4

    for attempt in range(MAX_RETRIES):
        current_difficulty = difficulty

        # Relax difficulty after 2 failures
        if attempt >= 2:
            current_difficulty = "medium"

        prompt = QUIZ_PROMPT_TEMPLATE.format(
            context=context,
            n_questions=SAFE_QUESTIONS,
            difficulty=current_difficulty,
        )

        response = generate_text(prompt)
        quiz = _extract_json(response)

        if not quiz:
            continue

        valid = []
        for q in quiz:
            if (
                isinstance(q, dict)
                and "question" in q
                and "options" in q
                and "answer" in q
                and isinstance(q["options"], list)
                and len(q["options"]) == 4
                and q["answer"] in q["options"]
            ):
                valid.append(q)

        if valid:
            return valid

    # After retries → no more questions
    return []
