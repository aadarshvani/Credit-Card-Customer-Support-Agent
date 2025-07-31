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
        response = requests.post(CREDIT_MODEL_API, json=customer_data)
        response.raise_for_status()
        result = response.json()
        prompt = CREDIT_TOOL_PROMPT.format(customer_data=customer_data)
        llm = get_llm()
        explanation = llm.invoke(prompt).content
        return {"status": "success", "type": "ml", "approval": result.get("approval"), "limit": result.get("limit"), "explanation": explanation}
    except Exception as e:
        return {"status": "error", "type": "ml", "message": str(e)}