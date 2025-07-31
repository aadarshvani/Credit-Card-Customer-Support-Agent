import os
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from langchain_huggingface import HuggingFaceEmbeddings

MINILM_MODEL_NAME = os.getenv("MINILM_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings():
    """
    Returns a HuggingFaceEmbeddings instance for MiniLM.
    """
    return HuggingFaceEmbeddings(model_name=MINILM_MODEL_NAME)