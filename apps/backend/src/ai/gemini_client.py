import google.generativeai as genai
from typing import List
from google.api_core.exceptions import ResourceExhausted
from ..config import get_settings

settings = get_settings()

genai.configure(api_key=settings.GEMINI_API_KEY)


def generate_text(prompt: str) -> str:
    """
    Used by Planner Agent
    SAFE against Gemini quota exhaustion
    """
    model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.2,
                "max_output_tokens": 512,
            },
        )
        return response.text.strip()

    except ResourceExhausted:
        # Planner fallback (CRITICAL)
        return """
{
  "search_pdfs": true,
  "topic": "electronics",
  "reason": "Fallback due to Gemini API quota exhaustion",
  "k": 5
}
"""


def generate_answer(context: str, question: str) -> str:
    """
    Used by Answer Agent
    Gives clear textbook-style answers grounded in PDFs
    """
    model = genai.GenerativeModel(settings.GEMINI_MODEL_NAME)

    prompt = f"""
You are an expert Electronics professor and AI tutor.

INSTRUCTIONS (VERY IMPORTANT):
- The user is a student asking a learning question.
- The provided study material may be fragmented, indirect, or technical.
- You MUST give a clear, standard textbook explanation of the concept.
- Use the study material ONLY to support and ground your explanation,
  NOT to limit or weaken it.
- NEVER say phrases like:
  "the text does not explicitly say"
  "we can infer"
  "based on limited information"
- If the topic is a known electronics concept (logic gate, flip-flop,
  counter, register, etc.), explain it properly even if PDFs are indirect.
- Do NOT invent advanced details not relevant to the question.
- Write in simple, exam-oriented teaching language.
- if a user did a spelling mistake correct it and answer the question

Study Material (for grounding only):
{context}

Student Question:
{question}

Answer (clear, direct, teaching-style):
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 900,
            },
        )
        return response.text.strip()

    except ResourceExhausted:
        # GENERAL fallback 
        return (
            "Not found in the provided knowledge base"
        )


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Gemini embeddings (LOGIC PRESERVED)
    Fixed to return one embedding per text for Chroma compatibility
    """

    embeddings: List[List[float]] = []

    for text in texts:
        result = genai.embed_content(
            model=settings.GEMINI_EMBED_MODEL_NAME,
            content=text,
            task_type="retrieval_document",
        )
        embeddings.append(result["embedding"])

    return embeddings
