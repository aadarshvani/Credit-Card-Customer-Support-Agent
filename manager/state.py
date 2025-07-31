# Session memory, user feedback, interaction logs
from typing import TypedDict, Optional, List, Dict, Any

class SessionState(TypedDict, total=False):
    user_id: str
    session_id: str
    history: List[Dict[str, Any]]  # List of {"query": str, "response": str, ...}
    last_intent: Optional[str]
    last_tool: Optional[str]
    last_response: Optional[str]
    feedback: Optional[str]
    customer_data: Optional[Dict[str, Any]]
    iteration_count: int