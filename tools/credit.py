# Credit approval logic
import requests

from core.config import CREDIT_MODEL_API
from manager.prompts import CREDIT_TOOL_PROMPT
from core.llm import get_llm

def check_credit_approval(customer_data: dict) -> dict:
    """
    Calls the credit approval model API and returns approval status, limit, and LLM-generated explanation.
    """
    try:
        # Check if API endpoint is configured
        if not CREDIT_MODEL_API or CREDIT_MODEL_API == "your_credit_model_endpoint":
            # Fallback: use LLM to simulate credit approval
            prompt = CREDIT_TOOL_PROMPT.format(customer_data=customer_data)
            llm = get_llm()
            explanation = llm.invoke(prompt).content
            return {
                "status": "success", 
                "type": "ml", 
                "approval": "pending", 
                "limit": 5000,
                "explanation": explanation,
                "note": "Using simulated credit approval (API not configured)"
            }
        
        # Call actual API
        response = requests.post(CREDIT_MODEL_API, json=customer_data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # Generate explanation using LLM
        prompt = CREDIT_TOOL_PROMPT.format(customer_data=customer_data)
        llm = get_llm()
        explanation = llm.invoke(prompt).content
        
        return {
            "status": "success", 
            "type": "ml", 
            "approval": result.get("approval", "pending"), 
            "limit": result.get("limit", 5000), 
            "explanation": explanation
        }
    except Exception as e:
        return {
            "status": "error", 
            "type": "ml", 
            "message": f"Credit approval failed: {str(e)}",
            "approval": "pending",
            "limit": 0,
            "explanation": "Unable to process credit approval at this time."
        }