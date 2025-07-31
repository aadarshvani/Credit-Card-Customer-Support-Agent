
import os
import pickle
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
from langchain_community.vectorstores import FAISS
from core.embeddings import get_embeddings
from rag.text_splitter import split_markdown

INDEX_PATH = os.path.join(os.path.dirname(__file__), "faiss_index.bin")
CHUNKS_PATH = os.path.join(os.path.dirname(__file__), "chunks.pkl")

def build_faiss_index(markdown_path: str):
    with open(markdown_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = split_markdown(text)
    embedder = get_embeddings()
    embeddings = embedder.embed_documents(chunks)
    # Create FAISS vector store
    faiss_store = FAISS.from_texts(chunks, embedder)
    faiss_store.save_local(INDEX_PATH)
    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump(chunks, f)
    return faiss_store, chunks



def load_faiss_index():
    faiss_store = FAISS.load_local(INDEX_PATH, get_embeddings())
    with open(CHUNKS_PATH, "rb") as f:
        chunks = pickle.load(f)
    return faiss_store, chunks



def search_faiss(query: str, k: int = 3):
    faiss_store, chunks = load_faiss_index()
    results = faiss_store.similarity_search(query, k=k)
    return [r.page_content if hasattr(r, 'page_content') else r for r in results]
