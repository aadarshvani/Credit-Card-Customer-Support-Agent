# Aggregates responses from tools
"""
Aggregates responses from multiple tools (RAG, web search, ML models, etc.)
and selects the most relevant or combines them for the final answer.
"""

from manager.prompts import AGGREGATOR_PROMPT
from core.llm import get_llm

def aggregate_responses(responses: list) -> dict:
    """
    Aggregates a list of response dicts from different tools using LLM to synthesize the best answer.
    """
    try:
        prompt = AGGREGATOR_PROMPT.format(responses=responses)
        llm = get_llm()
        best_answer = llm.invoke(prompt).content
        return {"status": "success", "type": "aggregated", "answer": best_answer, "sources": responses}
    except Exception as e:
        return {"status": "error", "type": "aggregated", "message": str(e), "sources": responses}
