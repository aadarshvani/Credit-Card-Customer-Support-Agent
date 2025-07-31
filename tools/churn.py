# Churn prediction logic
import requests
from core.config import CHURN_MODEL_API
from manager.prompts import CHURN_TOOL_PROMPT
from core.llm import get_llm

def predict_churn(customer_data: dict) -> dict:
    """
    Calls the churn prediction model API and returns the risk score and LLM-generated explanation.
    """
    try:
        # Check if API endpoint is configured
        if not CHURN_MODEL_API or CHURN_MODEL_API == "your_churn_model_endpoint":
            # Fallback: use LLM to simulate churn prediction
            prompt = CHURN_TOOL_PROMPT.format(customer_data=customer_data)
            llm = get_llm()
            explanation = llm.invoke(prompt).content
            return {
                "status": "success", 
                "type": "ml", 
                "risk": 0.5,  # Default risk score
                "explanation": explanation,
                "note": "Using simulated churn prediction (API not configured)"
            }
        
        # Call actual API
        response = requests.post(CHURN_MODEL_API, json=customer_data, timeout=10)
        response.raise_for_status()
        result = response.json()
        
        # Generate explanation using LLM
        prompt = CHURN_TOOL_PROMPT.format(customer_data=customer_data)
        llm = get_llm()
        explanation = llm.invoke(prompt).content
        
        return {
            "status": "success", 
            "type": "ml", 
            "risk": result.get("risk", 0.5), 
            "explanation": explanation
        }
    except Exception as e:
        return {
            "status": "error", 
            "type": "ml", 
            "message": f"Churn prediction failed: {str(e)}",
            "risk": 0.5,
            "explanation": "Unable to analyze churn risk at this time."
        }