# Web search integration
from langchain_community.tools.tavily_search import TavilySearchResults
from core.config import WEB_SEARCH_API_KEY
from manager.prompts import WEB_SEARCH_PROMPT
from core.llm import get_llm

def search_web(query: str, limit: int = 5) -> dict:
    """
    Uses LangChain's TavilySearchResults tool to perform a web search and summarizes results with LLM.
    """
    try:
        # Check if API key is configured
        if not WEB_SEARCH_API_KEY or WEB_SEARCH_API_KEY == "your_search_api_key":
            # Fallback: use LLM to simulate web search
            prompt = WEB_SEARCH_PROMPT.format(query=query, results="No web search available")
            llm = get_llm()
            summary = llm.invoke(prompt).content
            return {
                "status": "success", 
                "type": "web", 
                "summary": summary, 
                "raw_results": [],
                "note": "Using simulated web search (API key not configured)"
            }
        
        # Perform actual web search
        search_tool = TavilySearchResults(api_key=WEB_SEARCH_API_KEY)
        results = search_tool.run(query, num_results=limit)
        
        # Summarize results using LLM
        prompt = WEB_SEARCH_PROMPT.format(query=query, results=results)
        llm = get_llm()
        summary = llm.invoke(prompt).content
        
        return {
            "status": "success", 
            "type": "web", 
            "summary": summary, 
            "raw_results": results
        }
    except Exception as e:
        return {
            "status": "error", 
            "type": "web", 
            "message": f"Web search failed: {str(e)}",
            "summary": "Unable to perform web search at this time.",
            "raw_results": []
        }