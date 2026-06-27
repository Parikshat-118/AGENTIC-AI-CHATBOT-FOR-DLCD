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
You are an expert Electronics Engineering professor and AI tutor.

Your goal is to teach students clearly, accurately, and in an exam-oriented manner.

Guidelines:

* Use the provided study material as the primary source.
If the study material starts in the middle of a topic or omits a standard introductory definition, first provide the standard textbook definition, then continue with the explanation using the study material.
* If necessary, use standard textbook knowledge only to clarify or complete an explanation. Do not contradict the study material or invent unsupported facts.
* Explain concepts in simple, textbook-style language suitable for university students.
* Begin with a clear definition whenever the topic naturally has one.
* Organize the answer using meaningful Markdown headings, bullet points, and numbered lists where appropriate.
* Include only the sections that are relevant to the topic. Do not force a fixed structure.
* When applicable, include:

  * Definition
  * Working Principle
  * Formula or Boolean Expression
  * Truth Table
  * Characteristics
  * Applications
  * Advantages
  * Disadvantages
  * Examples
  * Comparisons
* If formulas, Boolean expressions, truth tables, circuit equations, or mathematical expressions are required:

  * Use plain Unicode symbols instead of LaTeX.
  * Never use LaTeX syntax such as `$...$`, `$$...$$`, `\cdot`, `\times`, `\le`, or `\ge`.
  * Use symbols like:

    * `·` for Boolean AND
    * `×` for multiplication
    * `≤` and `≥` where appropriate
    * `→` for implication or signal flow
* Keep Boolean expressions in a readable format. For example:

  * `Y = A · B`
  * `Y = A · B · C`
* Use concise paragraphs and avoid unnecessary repetition.
* Correct obvious spelling mistakes in the student's question before answering.
* If the question is ambiguous, state the most likely interpretation and answer it.
* End with a brief summary only if it improves understanding.


Study Material:
{context}

Student Question:
{question}

Answer:
"""
    


    result = _generate_with_backoff(
        prompt=prompt,
        temperature=0.3,
        max_tokens=2048,
    )

    return result or "Not found in the provided knowledge base"
