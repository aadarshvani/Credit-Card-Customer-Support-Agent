# Load your LLM here (Groq, OpenAI, etc.)
import os
from langchain_groq import ChatGroq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm(model: str = "gemma2-9b-it") -> ChatGroq:
    """
    Returns a ChatGroq LLM instance with the specified model.
    """
    return ChatGroq(api_key=GROQ_API_KEY, model=model)
