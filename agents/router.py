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
            return predict_churn(customer_data)
        else:
            return {"error": "Customer data required for churn prediction."}
    elif intent == "credit_approval":
        if customer_data:
            return check_credit_approval(customer_data)
        else:
            return {"error": "Customer data required for credit approval."}
    elif intent == "web_search":
        return {"results": search_web(query)}
    elif intent == "rag_search":
        return {"results": query_knowledge_base(query)}
    elif intent == "human_review":
        return request_human_review(query, customer_data)
    else:
        return {"error": f"Unknown intent: {intent}"}