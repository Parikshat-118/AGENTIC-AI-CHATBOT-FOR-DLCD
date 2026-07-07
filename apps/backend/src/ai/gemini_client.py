import time

from groq import Groq

from ..config import get_settings

settings = get_settings()

client = Groq(api_key=settings.GROQ_API_KEY)


def _generate_with_backoff(
    prompt: str,
    temperature: float,
    max_tokens: int,
) -> str:

    MAX_ATTEMPTS = 3
    BACKOFF_SECONDS = 2

    for attempt in range(MAX_ATTEMPTS):

        try:

            response = client.chat.completions.create(
                model=settings.GROQ_MODEL_NAME,
                temperature=temperature,
                max_tokens=max_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
            )

            return response.choices[0].message.content.strip()

        except Exception:

            if attempt == MAX_ATTEMPTS - 1:
                return ""

            time.sleep(BACKOFF_SECONDS * (attempt + 1))

    return ""


def generate_text(prompt: str) -> str:
    """
    Used by Planner Agent & Quiz Agent.
    """

    result = _generate_with_backoff(
        prompt=prompt,
        temperature=0.2,
        max_tokens=4096,
    )

    if not result:
        return """
{
  "search_pdfs": true,
  "topic": "electronics",
  "reason": "Groq unavailable",
  "k": 5
}
"""

    return result


def generate_answer(context: str, question: str) -> str:

    prompt = f"""
You are an expert Electronics Engineering professor and AI tutor.

Your goal is to teach students clearly, accurately, and in an exam-oriented manner.

Guidelines:

* Use the provided study material as the primary source.
If the study material starts in the middle of a topic or omits a standard introductory definition, first provide the standard textbook definition, then continue with the explanation using the study material.

* If necessary, use standard textbook knowledge only to clarify or complete an explanation.

* Explain concepts in simple textbook language suitable for university students.

* Begin with a definition whenever appropriate.

* Organize the answer using Markdown headings, bullet points, and numbered lists.

* Include only relevant sections.

* If formulas, truth tables or diagrams help, include them using Markdown.

Study Material:

{context}

Student Question:

{question}

Answer:
"""

    result = _generate_with_backoff(
        prompt=prompt,
        temperature=0.3,
        max_tokens=4096,
    )

    return result or "Not found in the provided knowledge base"
