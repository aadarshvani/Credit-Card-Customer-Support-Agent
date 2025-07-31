from rag.vector_store import search_faiss
import os

def query_knowledge_base(query: str) -> dict:
    """
    Query the knowledge base using FAISS vector search and return the most relevant chunks.
    """
    try:
        # Check if FAISS index exists
        index_path = os.path.join(os.path.dirname(__file__), "faiss_index.bin")
        if not os.path.exists(index_path):
            return {
                "status": "error", 
                "message": "Knowledge base not initialized. Please run the initialization script first.",
                "results": []
            }
        
        results = search_faiss(query, k=3)
        if results:
            return {
                "status": "success", 
                "results": results,
                "message": f"Found {len(results)} relevant documents."
            }
        else:
            return {
                "status": "not_found", 
                "message": "No relevant answer found in the knowledge base.",
                "results": []
            }
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Knowledge base query failed: {str(e)}",
            "results": []
        }
