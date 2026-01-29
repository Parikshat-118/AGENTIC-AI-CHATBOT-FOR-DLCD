import json
from .gemini_client import generate_text
from .agent_prompts import PLANNER_PROMPT


def plan(query: str) -> dict:
    try:
        response = generate_text(
            f"""
{PLANNER_PROMPT}

User query:
"{query}"
"""
        )
        return json.loads(response)

    except Exception:
        # HARD FAIL — DO NOT SEARCH PDFs
        return {
            "search_pdfs": False,
            "topic": None,
            "reason": "Planner failed to classify query safely",
            "k": 0,
        }
