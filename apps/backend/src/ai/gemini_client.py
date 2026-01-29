import time
from google import genai
from google.api_core.exceptions import ResourceExhausted
from google.genai.errors import ClientError
from ..config import get_settings

settings = get_settings()

# Gemini client (text-only, free tier safe)
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def _generate_with_backoff(prompt: str, temperature: float, max_tokens: int) -> str:
    """
    Internal helper with rate-limit safety.
    """

    MAX_ATTEMPTS = 3
    BACKOFF_SECONDS = 2

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config={
                    "temperature": temperature,
                    "max_output_tokens": max_tokens,
                },
            )
            return response.text.strip()

        except ResourceExhausted:
            # Gemini quota hit
            time.sleep(BACKOFF_SECONDS * (attempt + 1))

        except ClientError as e:
            # Explicit 429 handling
            if "RESOURCE_EXHAUSTED" in str(e):
                time.sleep(BACKOFF_SECONDS * (attempt + 1))
            else:
                raise e

    # After retries → fail safely
    return ""


def generate_text(prompt: str) -> str:
    """
    Used by Planner Agent & Quiz Agent
    """
    result = _generate_with_backoff(
        prompt=prompt,
        temperature=0.2,
        max_tokens=512,
    )

    if not result:
        # Planner-safe fallback
        return """
{
  "search_pdfs": true,
  "topic": "electronics",
  "reason": "Gemini rate limit fallback",
  "k": 5
}
"""
    return result


def generate_answer(context: str, question: str) -> str:
    """
    Used by Answer Agent
    """

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
- If a user did a spelling mistake, correct it and answer the question.

Study Material (for grounding only):
{context}

Student Question:
{question}

Answer (clear, direct, teaching-style):
"""

    result = _generate_with_backoff(
        prompt=prompt,
        temperature=0.3,
        max_tokens=900,
    )

    return result or "Not found in the provided knowledge base"
