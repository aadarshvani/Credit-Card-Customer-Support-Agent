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
        response = requests.post(CHURN_MODEL_API, json=customer_data)
        response.raise_for_status()
        result = response.json()
        prompt = CHURN_TOOL_PROMPT.format(customer_data=customer_data)
        llm = get_llm()
        explanation = llm.invoke(prompt).content
        return {"status": "success", "type": "ml", "risk": result.get("risk"), "explanation": explanation}
    except Exception as e:
        return {"status": "error", "type": "ml", "message": str(e)}