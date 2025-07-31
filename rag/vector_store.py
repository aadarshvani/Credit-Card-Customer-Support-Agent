
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
    """Build FAISS index from markdown file"""
    try:
        if not os.path.exists(markdown_path):
            raise FileNotFoundError(f"Markdown file not found: {markdown_path}")
            
        with open(markdown_path, "r", encoding="utf-8") as f:
            text = f.read()
        
        chunks = split_markdown(text)
        embedder = get_embeddings()
        
        # Create FAISS vector store
        faiss_store = FAISS.from_texts(chunks, embedder)
        faiss_store.save_local(INDEX_PATH)
        
        with open(CHUNKS_PATH, "wb") as f:
            pickle.dump(chunks, f)
            
        print(f"FAISS index built successfully with {len(chunks)} chunks")
        return faiss_store, chunks
    except Exception as e:
        print(f"Error building FAISS index: {str(e)}")
        raise

def load_faiss_index():
    """Load existing FAISS index"""
    try:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError("FAISS index not found. Please build the index first.")
            
        faiss_store = FAISS.load_local(INDEX_PATH, get_embeddings())
        
        if not os.path.exists(CHUNKS_PATH):
            raise FileNotFoundError("Chunks file not found. Please rebuild the index.")
            
        with open(CHUNKS_PATH, "rb") as f:
            chunks = pickle.load(f)
            
        return faiss_store, chunks
    except Exception as e:
        print(f"Error loading FAISS index: {str(e)}")
        raise

def search_faiss(query: str, k: int = 3):
    """Search FAISS index for similar documents"""
    try:
        faiss_store, chunks = load_faiss_index()
        results = faiss_store.similarity_search(query, k=k)
        return [r.page_content if hasattr(r, 'page_content') else str(r) for r in results]
    except Exception as e:
        print(f"Error searching FAISS index: {str(e)}")
        return []
