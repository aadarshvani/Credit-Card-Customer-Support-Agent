from rag.vector_store import search_faiss

def query_knowledge_base(query: str) -> dict:
    """
    Query the knowledge base using FAISS vector search and return the most relevant chunks.
    """
    try:
        results = search_faiss(query, k=3)
        if results:
            return {"status": "success", "results": results}
        else:
            return {"status": "not_found", "message": "No relevant answer found."}
    except Exception as e:
        return {"status": "error", "message": str(e)}
