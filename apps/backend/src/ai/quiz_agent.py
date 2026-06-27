# src/ai/quiz_agent.py

import json
import re
import random
from typing import List

from .gemini_client import generate_text
from .vector_store import vector_store


DIFFICULTY_INSTRUCTIONS = {
    "easy": "Ask simple definition and application-based questions.",
    "medium": "Ask conceptual reasoning questions.",
    "hard": "Ask analytical and problem-solving questions.",
}

BAD_WORDS = [
    "figure",
    "fig.",
    "diagram",
    "page",
    "table",
]

QUIZ_PROMPT_TEMPLATE = """
You are an expert Electronics Engineering professor preparing university examination questions.

Generate EXACTLY {n_questions} multiple-choice questions.

Difficulty: {difficulty}

Difficulty Instructions:

{difficulty_instructions}

IMPORTANT RULES:

• Questions must test conceptual understanding.
• Prefer:
  - Definitions
  - Working principle
  - Characteristics
  - Applications
  - Comparisons
  - Advantages & disadvantages
  - Logical reasoning
  - Circuit behaviour

• Avoid:
  - Page numbers
  - Figure numbers
  - IC numbers
  - Model names
  - Part numbers
  - Exact voltage values
  - Obscure implementation details
  - Manufacturing details

• Questions should resemble semester examination questions.

• Cover different concepts.

• Never ask two questions testing the same concept.

• Distribute questions across different topics in the supplied material.

• If generating multiple questions, ensure each question covers a different concept from the study material.

• Do not generate two questions from the same subsection unless unavoidable.

• If the study material covers multiple concepts, cover as many concepts as possible.

• Avoid asking trivial factual recall questions.

• Each question must have exactly four options.

• Exactly ONE option is correct.

• The answer MUST exactly match one option.

• Options must be four distinct values (no duplicates).

• Keep options short.

• Each question should be under 35 words.

• Each option should be under 15 words.

• Do NOT repeat questions.

• Return ONLY JSON.

Output Format:

[
    {{
        "question":"...",
        "options":["A","B","C","D"],
        "answer":"..."
    }}
]

Study Material:

{context}
"""


def _extract_json(text):

    if not text:
        return None

    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()

    start = text.find("[")
    end = text.rfind("]")

    if start == -1 or end == -1:
        return None

    text = text[start:end+1]

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def _normalize(text: str):
    return text.strip().lower()


def _apply_difficulty(chunks: List[str], difficulty: str):
    n = len(chunks)

    if n == 0:
        return []

    if difficulty == "easy":
        return chunks[:max(1, int(0.3 * n))]

    if difficulty == "hard":
        return chunks[int(0.7 * n):]

    return chunks[int(0.3 * n):int(0.7 * n)]


def _select_chunks(filtered: List[str]):
    if len(filtered) <= 8:
        return filtered
    return filtered[:4] + random.sample(filtered[4:], 4)


def _contains_bad_words(q: dict) -> bool:
    question = q["question"].lower()
    if any(word in question for word in BAD_WORDS):
        return True

    for opt in q["options"]:
        if any(word in str(opt).lower() for word in BAD_WORDS):
            return True

    return False


def generate_quiz_from_pdf(
    pdf_title: str,
    n_questions: int = 10,
    difficulty: str = "medium",
):

    SAFE_QUESTIONS = min(n_questions, 10)

    raw = vector_store.get(include=["documents", "metadatas"])

    matched = [
        doc
        for doc, meta in zip(raw["documents"], raw["metadatas"])
        if _normalize(meta.get("title", "")) == _normalize(pdf_title)
    ]

    if not matched:
        matched = [
            doc
            for doc, meta in zip(raw["documents"], raw["metadatas"])
            if _normalize(pdf_title) in _normalize(meta.get("title", ""))
        ]

    if not matched:
        return []

    filtered = _apply_difficulty(matched, difficulty)

    if not filtered:
        filtered = matched

    selected = _select_chunks(filtered)

    context = "\n\n".join(selected)

    difficulty_instructions = DIFFICULTY_INSTRUCTIONS.get(
        difficulty, DIFFICULTY_INSTRUCTIONS["medium"]
    )

    MAX_RETRIES = 5

    for attempt in range(MAX_RETRIES):

        if attempt > 0:
            selected = _select_chunks(filtered)
            context = "\n\n".join(selected)

        prompt = QUIZ_PROMPT_TEMPLATE.format(
            context=context,
            n_questions=SAFE_QUESTIONS,
            difficulty=difficulty,
            difficulty_instructions=difficulty_instructions,
        )

        response = generate_text(prompt)

        quiz = _extract_json(response)

        if quiz is None:
            continue

        valid = []

        for q in quiz:

            if not (
                isinstance(q, dict)
                and "question" in q
                and "options" in q
                and "answer" in q
                and isinstance(q["options"], list)
                and len(q["options"]) == 4
            ):
                continue

            options = [str(opt).strip() for opt in q["options"]]
            answer = str(q["answer"]).strip()

            if len(set(options)) != 4:
                continue

            if answer not in options:
                continue

            q["options"] = options
            q["answer"] = answer

            if _contains_bad_words(q):
                continue

            valid.append(q)

        if valid:
            seen = set()
            unique = []

            for q in valid:
                key = q["question"].strip().lower()

                if key not in seen:
                    seen.add(key)
                    unique.append(q)

            valid = unique

            random.shuffle(valid)
            return valid[:SAFE_QUESTIONS]

    return []
