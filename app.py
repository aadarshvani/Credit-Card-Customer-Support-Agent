from langgraph.graph import StateGraph, END
from manager.state import SessionState
from agents.router import route_query
from agents.aggregator import aggregate_responses
from agents.quality_checker import check_response_quality
import os
from rag.vector_store import build_faiss_index, INDEX_PATH

if not os.path.exists(INDEX_PATH):
    print("Building FAISS index for the first time...")
    build_faiss_index("rag/knowledge_base/faqs.md")
    print("FAISS index built.")

def user_input_node(state: SessionState) -> SessionState:
    # Get user input from Streamlit or CLI
    return state

def router_node(state: SessionState) -> SessionState:
    query = state["history"][-1]["query"]
    customer_data = state.get("customer_data")
    response = route_query(query, customer_data)
    state["tool_responses"] = [response]
    return state

def aggregator_node(state: SessionState) -> SessionState:
    responses = state.get("tool_responses", [])
    aggregated = aggregate_responses(responses)
    # Always set aggregated_response, even if aggregation fails
    if not aggregated:
        aggregated = {"message": "", "summary": ""}
    state["aggregated_response"] = aggregated
    return state

def quality_checker_node(state: SessionState) -> SessionState:
    question = state["history"][-1]["query"]
    answer = state.get("aggregated_response", {}).get("message") or state.get("aggregated_response", {}).get("answer") or ""
    
    # Create the response dict for quality checking
    response_dict = {"question": question, "answer": answer}
    checked = check_response_quality(response_dict)
    
    # Update state with quality information
    state["quality"] = checked.get("quality", "unknown")
    state["feedback"] = checked.get("feedback")
    state["final_answer"] = answer
    return state

def improvement_node(state: SessionState) -> SessionState:
    # Optionally re-run aggregation or tool with feedback
    state["iteration_count"] = state.get("iteration_count", 0) + 1
    # For simplicity, just return the same answer here
    return state

def end_node(state: SessionState) -> SessionState:
    # Log, save, and return answer to user
    return state

graph = StateGraph(SessionState)
graph.add_node("UserInput", user_input_node)
graph.add_node("Router", router_node)
graph.add_node("Aggregator", aggregator_node)
graph.add_node("QualityChecker", quality_checker_node)
graph.add_node("Improve", improvement_node)
graph.add_node("End", end_node)

graph.add_edge("UserInput", "Router")
graph.add_edge("Router", "Aggregator")
graph.add_edge("Aggregator", "QualityChecker")
graph.add_conditional_edges(
    "QualityChecker",
    lambda state: "Improve" if state["quality"] != "high" and state.get("iteration_count", 0) < 2 else "End"
)
graph.add_edge("Improve", "Aggregator")
graph.add_edge("End", END)
graph.set_entry_point("UserInput")

app_flow = graph.compile()

# Example usage:
if __name__ == "__main__":
    # Initialize state with user_id, session_id, and first query in history
    state = SessionState(
        user_id="user123",
        session_id="sess456",
        history=[{"query": "How do I close my credit card?"}],
        iteration_count=0
    )
    for step in app_flow.stream(state):
        print(step)


