# Intent classification and routing
# Intent classification and routing

from tools.churn import predict_churn
from tools.credit import check_credit_approval
from tools.human_review import request_human_review
from tools.web_search import search_web
from rag.rag_engine import query_knowledge_base
from manager.prompts import INTENT_CLASSIFICATION_PROMPT

from core.llm import get_llm
from core.embeddings import get_embeddings
from langchain_core.prompts import ChatPromptTemplate

def detect_intent(query: str) -> str:
    """
    Uses an LLM to classify the intent of the user's query.
    """
    prompt = ChatPromptTemplate.from_template(INTENT_CLASSIFICATION_PROMPT)
    llm = get_llm()
    chain = prompt | llm
    result = chain.invoke({"query": query})
    return result.content.strip().lower()

def route_query(query: str, customer_data: dict = None) -> dict:
    """
    Detects intent and routes the query to the appropriate tool.
    """
    intent = detect_intent(query)
    if intent == "churn_risk":
        if customer_data:
            result = predict_churn(customer_data)
            return {"status": "success", "type": "churn", "message": result.get("explanation", "Churn analysis completed."), "data": result}
        else:
            return {"status": "error", "message": "Customer data required for churn prediction."}
    elif intent == "credit_approval":
        if customer_data:
            result = check_credit_approval(customer_data)
            return {"status": "success", "type": "credit", "message": result.get("explanation", "Credit analysis completed."), "data": result}
        else:
            return {"status": "error", "message": "Customer data required for credit approval."}
    elif intent == "web_search":
        result = search_web(query)
        return {"status": "success", "type": "web", "message": result.get("summary", "Web search completed."), "data": result}
    elif intent == "rag_search":
        result = query_knowledge_base(query)
        return {"status": "success", "type": "rag", "message": "Knowledge base search completed.", "data": result}
    elif intent == "human_review":
        result = request_human_review(query, customer_data)
        return {"status": "pending", "type": "human", "message": result.get("message", "Human review requested."), "data": result}
    else:
        return {"status": "error", "message": f"Unknown intent: {intent}"}