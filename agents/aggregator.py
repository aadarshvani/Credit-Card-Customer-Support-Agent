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
        if not responses:
            return {"status": "error", "message": "No responses to aggregate"}
            
        prompt = AGGREGATOR_PROMPT.format(responses=responses)
        llm = get_llm()
        best_answer = llm.invoke(prompt).content
        
        return {
            "status": "success", 
            "type": "aggregated", 
            "message": best_answer,  # Changed from "answer" to "message" to match expected format
            "sources": responses
        }
    except Exception as e:
        return {
            "status": "error", 
            "type": "aggregated", 
            "message": f"Failed to aggregate responses: {str(e)}", 
            "sources": responses
        }
