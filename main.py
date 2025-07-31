import streamlit as st
from manager.state import SessionState
from app import app_flow

st.set_page_config(page_title="AmEx AI Credit Support Agent", page_icon="🏦", layout="wide")

# --- Session State ---
if "session_state" not in st.session_state:
    st.session_state.session_state = SessionState(
        user_id="user1",
        session_id="sess1",
        history=[],
        iteration_count=0,
    )
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def add_message(role, content):
    st.session_state.session_state["history"].append({"role": role, "content": content})

# --- Custom CSS for wide, clean UI ---
st.markdown(
    """
    <style>
    .main-container {max-width: 1200px; margin: 0 auto;}
    .chat-bubble {padding: 16px 20px; border-radius: 18px; margin: 8px 0; max-width: 70%; font-size: 1.1em;}
    .user-bubble {background: #e6f7ff; color: #222; margin-left: auto; border-bottom-right-radius: 4px;}
    .agent-bubble {background: #f6f6f6; color: #222; margin-right: auto; border-bottom-left-radius: 4px;}
    .chat-row {display: flex; align-items: flex-end;}
    .avatar {width: 44px; height: 44px; border-radius: 50%; background: #fff; display: flex; align-items: center; justify-content: center; font-size: 1.7em; margin: 0 10px; box-shadow: 0 1px 4px #0001;}
    .input-bar {position: fixed; bottom: 0; left: 0; width: 100vw; background: #fff; box-shadow: 0 -2px 12px #0002; padding: 16px 0 12px 0; z-index: 100;}
    .stTextInput>div>div>input {font-size: 1.1em; padding: 10px; border-radius: 8px;}
    .stButton>button {font-size: 1.1em; border-radius: 8px;}
    .stApp {background: #f3f7fa;}
    @media (max-width: 900px) {.main-container {max-width: 98vw;}}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Header ---
st.markdown(
    """
    <div class='main-container'>
    <h1 style='text-align: center; margin-bottom: 0;'>🏦 AmEx AI Credit Support Agent</h1>
    <p style='text-align: center; color: #888; margin-top: 0;'>Your intelligent assistant for American Express credit card support.</p>
    <hr style='margin-bottom: 0;'>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Main Chat Area ---
with st.container():
    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    for msg in st.session_state.session_state["history"]:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class='chat-row' style='justify-content: flex-end;'>
                    <div class='chat-bubble user-bubble'>{msg['content']}</div>
                    <div class='avatar' title='You'>🧑</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class='chat-row' style='justify-content: flex-start;'>
                    <div class='avatar' title='Agent'>🤖</div>
                    <div class='chat-bubble agent-bubble'>{msg['content']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

# --- Fixed Input Bar ---
with st.container():
    st.markdown("<div class='input-bar main-container'>", unsafe_allow_html=True)
    with st.form(key="chat_form", clear_on_submit=True):
        cols = st.columns([0.85, 0.15])
        user_input = cols[0].text_input(
            "Type your question...",
            value=st.session_state.user_input,
            key="user_input",
            placeholder="Ask me anything about your AmEx credit card...",
            label_visibility="collapsed",
        )
        submitted = cols[1].form_submit_button("Send")
        if submitted and user_input.strip():
            add_message("user", user_input)
            # Prepare state for graph
            state = st.session_state.session_state
            state["history"][-1]["query"] = user_input
            # Run the graph
            for step in app_flow.stream(state):
                pass  # The graph updates the state in place
            # Get the latest agent answer
            answer = state.get("final_answer") or "Sorry, I couldn't find an answer."
            add_message("agent", answer)
            st.session_state.user_input = ""
    st.markdown("</div>", unsafe_allow_html=True)

# --- Sidebar: Chat History & Controls ---
with st.sidebar:
    st.title("Chat History")
    for msg in st.session_state.session_state["history"]:
        role = "🧑" if msg["role"] == "user" else "🤖"
        st.markdown(f"{role} {msg['content']}")
    if st.button("Clear chat"):
        st.session_state.session_state["history"] = []
        st.experimental_rerun()

# --- Footer ---
st.markdown(
    """
    <div style='text-align: center; color: #aaa; font-size: 0.95em; margin-top: 60px;'>
        Powered by advanced AI, RAG, and ML models.<br>
        <span style='font-size:0.9em;'>© 2025 AmEx AI Credit Support Agent</span>
    </div>
    """,
    unsafe_allow_html=True,
)