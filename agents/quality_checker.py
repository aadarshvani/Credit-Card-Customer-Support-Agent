# Answer quality checking
"""
Checks the quality of generated responses (e.g., relevance, completeness, tone).
Can be extended to use LLMs or rule-based checks.
"""

from manager.prompts import QUALITY_CHECKER_PROMPT
from core.llm import get_llm

def check_response_quality(response: dict) -> dict:
    """
    Checks if the response meets quality standards using LLM.
    Returns the response with a quality flag and optional feedback.
    """
    try:
        question = response.get("question", "")
        answer = response.get("answer", "")
        
        prompt = QUALITY_CHECKER_PROMPT.format(question=question, answer=answer)
        llm = get_llm()
        quality_feedback = llm.invoke(prompt).content
        
        # Determine quality level based on feedback
        if "good" in quality_feedback.lower() or "excellent" in quality_feedback.lower():
            quality = "high"
        elif "needs improvement" in quality_feedback.lower() or "poor" in quality_feedback.lower():
            quality = "low"
        else:
            quality = "medium"
            
        return {
            "quality": quality,
            "feedback": quality_feedback,
            "question": question,
            "answer": answer
        }
    except Exception as e:
        return {
            "quality": "unknown",
            "feedback": f"Quality check failed: {str(e)}",
            "question": response.get("question", ""),
            "answer": response.get("answer", "")
        }