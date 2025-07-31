import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WEB_SEARCH_API_KEY = os.getenv("WEB_SEARCH_API_KEY")
CHURN_MODEL_API = os.getenv("CHURN_MODEL_API")
CREDIT_MODEL_API = os.getenv("CREDIT_MODEL_API")
