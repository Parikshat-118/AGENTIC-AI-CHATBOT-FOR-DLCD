import time

from google import genai
from google.genai import types
from google.api_core.exceptions import ResourceExhausted
from google.genai.errors import ClientError

from ..config import get_settings

settings = get_settings()

client = genai.Client(api_key=settings.GEMINI_API_KEY)


def _generate_with_backoff(
    prompt: str,
    temperature: float,
    max_tokens: int,
    thinking_budget: int | None = None,
) -> str:
    """
    Generic Gemini generator with retry support.
    """

    MAX_ATTEMPTS = 3
    BACKOFF_SECONDS = 2

    for attempt in range(MAX_ATTEMPTS):
        try:

            config = types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
            )

            if thinking_budget is not None:
                config.thinking_config = types.ThinkingConfig(
                    thinking_budget=thinking_budget
                )

            response = client.models.generate_content(
                model=settings.GEMINI_MODEL_NAME,
                contents=prompt,
                config=config,
            )

            return response.text.strip() if response.text else ""

        except ResourceExhausted:
            time.sleep(BACKOFF_SECONDS * (attempt + 1))

        except ClientError as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                time.sleep(BACKOFF_SECONDS * (attempt + 1))
            else:
                raise

    return ""


def generate_text(prompt: str) -> str:
    """
    Used by Planner Agent & Quiz Agent.

    Thinking is disabled so Gemini spends tokens
    generating JSON instead of reasoning.
    """

    result = _generate_with_backoff(
        prompt=prompt,
        temperature=0.2,
        max_tokens=2048,
        thinking_budget=0,
    )

    if not result:
        return """
{
  "search_pdfs": true,
  "topic": "electronics",
  "reason": "Gemini unavailable",
  "k": 5
}
"""

    return result


def generate_answer(context: str, question: str) -> str:
    """
    Used by Answer Agent.
    """

    prompt = f"""
You are an expert Electronics professor and AI tutor.

INSTRUCTIONS:
- Explain like a textbook.
- Answer using the supplied study material.
- Keep the explanation clear and exam-oriented.
- Correct spelling mistakes automatically.
- Use headings and bullet points where useful.

Study Material:
{context}

Question:
{question}

Answer:
"""

    result = _generate_with_backoff(
        prompt=prompt,
        temperature=0.3,
        max_tokens=2048,
    )

    return result or "Not found in the provided knowledge base"
