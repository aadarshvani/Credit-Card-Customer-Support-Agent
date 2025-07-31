# Answer quality checking
"""
Checks the quality of generated responses (e.g., relevance, completeness, tone).
Can be extended to use LLMs or rule-based checks.
"""

from manager.prompts import QUALITY_CHECKER_PROMPT
from core.llm import get_llm

def check_response_quality(response: dict, question: str = "") -> dict:
    """
    Checks if the response meets quality standards using LLM, considering the original question.
    Returns the response with a quality flag and optional feedback.
    """
    try:
        answer = response.get("message") or response.get("answer") or ""
        prompt = QUALITY_CHECKER_PROMPT.format(question=question, answer=answer)
        llm = get_llm()
        quality_feedback = llm.invoke(prompt).content
        response["quality_feedback"] = quality_feedback
        return response
    except Exception as e:
        response["quality_feedback"] = f"Quality check failed: {str(e)}"
        return response