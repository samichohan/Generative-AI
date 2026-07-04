from dotenv import load_dotenv
load_dotenv()
import os

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# ── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(page_title="Mood AI", page_icon="◆", layout="wide", initial_sidebar_state="expanded")

# ── Mood Definitions ──────────────────────────────────────────────────────
MOODS = {
    "angry": {
        "label": "Angry",
        "icon": "🔥",
        "prompt": "You are an angry AI Agent. You respond aggressively and impatiently, but you still give correct and useful answers.",
        "accent": "#e5484d",
    },
    "funny": {
        "label": "Funny",
        "icon": "✦",
        "prompt": "You are a very funny AI Agent. You respond with humor and jokes, while still being genuinely helpful.",
        "accent": "#f5c842",
    },
    "sad": {
        "label": "Sad",
        "icon": "○",
        "prompt": "You are a sad AI Agent. You respond in a melancholic, sighing way, but your answers remain accurate and helpful.",
        "accent": "#5b9bd5",
    },
    "normal": {
        "label": "Normal",
        "icon": "●",
        "prompt": "You are a normal AI Agent. You respond in a plain, balanced, professional way.",
        "accent": "#3ecf8e",
    },
    "intelligent": {
        "label": "Intelligent",
        "icon": "◆",
        "prompt": "You are an intelligent AI Agent. You respond with depth, precision, and an analytical, well-reasoned tone.",
        "accent": "#9b8cf2",
    },
}
DEFAULT_MOOD = "normal"

# ── Session State ──────────────────────────────────────────────────────────
if "mood_key" not in st.session_state:
    st.session_state.mood_key = DEFAULT_MOOD
if "messages" not in st.session_state:
    st.session_state.messages = [SystemMessage(content=MOODS[DEFAULT_MOOD]["prompt"])]
if "chat_display" not in st.session_state:
    st.session_state.chat_display = []

mood = MOODS[st.session_state.mood_key]
accent = mood["accent"]

# ── CSS ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* {{ font-family: 'Inter', sans-serif; }}

.stApp {{
    background: #0d0d10;
    color: #ececf1;
}}
#MainMenu, footer {{ visibility: hidden; }}

/* Keep Streamlit's own header visible — it contains the sidebar toggle arrow */
header[data-testid="stHeader"] {{
    background: #0d0d10 !important;
    height: 3rem;
}}
/* Make the built-in sidebar collapse/expand arrow clearly visible */
button[data-testid="stSidebarCollapsedControl"],
div[data-testid="stSidebarCollapsedControl"] {{
    background: #1a1a1f !important;
    border: 1px solid #2a2a31 !important;
    border-radius: 8px !important;
    color: #ececf1 !important;
    opacity: 1 !important;
    visibility: visible !important;
}}
button[data-testid="stSidebarCollapsedControl"] svg,
div[data-testid="stSidebarCollapsedControl"] svg {{
    color: #ececf1 !important;
    fill: #ececf1 !important;
}}
[data-testid="collapsedControl"] {{
    background: #1a1a1f !important;
    border: 1px solid #2a2a31 !important;
    border-radius: 8px !important;
    opacity: 1 !important;
}}
[data-testid="collapsedControl"] svg {{ color: #ececf1 !important; fill: #ececf1 !important; }}

.block-container {{ padding: 0.6rem 1rem 0 !important; max-width: 100% !important; }}

/* ===== Sidebar ===== */
section[data-testid="stSidebar"] {{
    background: #111114 !important;
    border-right: 1px solid #1f1f24;
}}
section[data-testid="stSidebar"] .block-container {{ padding: 1.2rem 1rem !important; }}

.brand {{
    display: flex; align-items: center; gap: 10px;
    font-size: 1.05rem; font-weight: 700; color: #fff;
    margin-bottom: 1.4rem; padding: 0 4px;
}}
.brand .dot {{ color: {accent}; font-size: 1.2rem; }}

.sidebar-label {{
    font-size: 0.7rem; letter-spacing: 1.5px; text-transform: uppercase;
    color: #5a5a66; margin: 1rem 4px 0.6rem;
}}

section[data-testid="stSidebar"] div[data-testid="stButton"] button {{
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 10px !important;
    color: #b4b4bd !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 9px 12px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    width: 100% !important;
    margin-bottom: 2px !important;
    transition: all 0.12s ease !important;
}}
section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {{
    background: #1a1a1f !important;
    color: #fff !important;
    border-color: #28282f !important;
}}

.mood-active {{
    background: #1a1a1f !important;
    border: 1px solid {accent}55 !important;
    border-radius: 10px;
    padding: 9px 12px;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    color: {accent};
}}

.history-item {{
    padding: 8px 10px; border-radius: 8px; font-size: 0.8rem;
    color: #8a8a96; margin-bottom: 2px; cursor: default;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    border: 1px solid transparent;
}}
.history-empty {{
    font-size: 0.78rem; color: #45454f; padding: 8px 10px; font-style: italic;
}}

.sidebar-footer {{
    font-size: 0.7rem; color: #45454f; padding: 14px 4px 4px;
    border-top: 1px solid #1f1f24; margin-top: 1.4rem;
}}

/* ===== Top mood-pill bar (main area) ===== */
.mood-bar-wrap {{
    max-width: 760px; margin: 0.2rem auto 1.2rem;
}}

div.moodbar [data-testid="stHorizontalBlock"] {{
    gap: 8px !important;
}}

div.moodbar div[data-testid="stButton"] button {{
    background: #15151a !important;
    border: 1px solid #25252c !important;
    border-radius: 999px !important;
    color: #9a9aa6 !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    padding: 7px 14px !important;
    width: 100% !important;
    transition: all 0.12s ease !important;
}}
div.moodbar div[data-testid="stButton"] button:hover {{
    border-color: #3a3a44 !important;
    color: #e0e0e8 !important;
}}

.mood-pill-active {{
    background: {accent}1a !important;
    border: 1px solid {accent} !important;
    border-radius: 999px;
    color: {accent} !important;
    font-size: 0.78rem;
    font-weight: 700;
    padding: 7px 14px;
    text-align: center;
}}

/* ===== Empty state ===== */
.empty-wrap {{
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    min-height: 42vh; text-align: center;
}}
.empty-icon {{ font-size: 2.2rem; color: {accent}; margin-bottom: 14px; }}
.empty-title {{ font-size: 1.4rem; font-weight: 700; color: #f2f2f5; margin-bottom: 6px; }}
.empty-sub {{ font-size: 0.9rem; color: #6a6a76; }}

/* ===== Chat bubbles ===== */
.msg-row {{ display: flex; margin: 14px 0; max-width: 760px; margin-left: auto; margin-right: auto; }}
.msg-row.user {{ justify-content: flex-end; }}
.msg-row.bot {{ justify-content: flex-start; gap: 10px; }}

.avatar {{
    width: 30px; height: 30px; border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; flex-shrink: 0;
    background: {accent}22; border: 1px solid {accent}44; color: {accent};
}}

.bubble {{
    padding: 12px 16px; border-radius: 14px; font-size: 0.92rem; line-height: 1.65;
    max-width: 78%; word-wrap: break-word;
}}
.bubble.user {{
    background: #1d1d23; color: #f0f0f3; border: 1px solid #2a2a31;
    border-radius: 14px 14px 4px 14px;
}}
.bubble.bot {{
    background: transparent; color: #d6d6dd; padding-top: 6px;
}}

/* ===== Input bar — THE FIX ===== */
.input-shell {{ max-width: 760px; margin: 1.4rem auto 0.6rem; }}

div[data-testid="stForm"] {{
    border: 1px solid #2a2a31 !important;
    background: #1a1a1f !important;
    border-radius: 16px !important;
    padding: 6px 8px 6px 18px !important;
}}
div[data-testid="stForm"]:focus-within {{
    border-color: {accent}99 !important;
}}

/* Target the actual input element directly and forcefully */
div[data-testid="stForm"] input[type="text"] {{
    background-color: #1a1a1f !important;
    color: #f5f5f7 !important;
    -webkit-text-fill-color: #f5f5f7 !important;
    caret-color: {accent} !important;
    border: none !important;
    font-size: 0.95rem !important;
    padding: 12px 0 !important;
    box-shadow: none !important;
}}
div[data-testid="stForm"] input[type="text"]::placeholder {{
    color: #6a6a76 !important;
    -webkit-text-fill-color: #6a6a76 !important;
    opacity: 1 !important;
}}
div[data-testid="stForm"] .stTextInput > div {{
    background-color: transparent !important;
    border: none !important;
}}
div[data-testid="stForm"] .stTextInput > div > div {{
    background-color: transparent !important;
    border: none !important;
}}
div[data-testid="stForm"] [data-baseweb="input"] {{
    background-color: transparent !important;
    border: none !important;
}}

div[data-testid="stFormSubmitButton"] button {{
    background: {accent} !important;
    color: #0d0d10 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 10px 18px !important;
    font-size: 0.85rem !important;
}}
div[data-testid="stFormSubmitButton"] button:hover {{ opacity: 0.88 !important; }}

.input-hint {{
    text-align: center; font-size: 0.72rem; color: #44444e; margin-top: 8px; margin-bottom: 1rem;
}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="brand"><span class="dot">◆</span> Mood AI</div>', unsafe_allow_html=True)

    if st.button("➕  New chat", key="new_chat_btn"):
        st.session_state.messages = [SystemMessage(content=mood["prompt"])]
        st.session_state.chat_display = []
        st.rerun()

    st.markdown('<div class="sidebar-label">Personality</div>', unsafe_allow_html=True)
    for key, m in MOODS.items():
        if key == st.session_state.mood_key:
            st.markdown(f'<div class="mood-active">{m["icon"]} {m["label"]}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{m['icon']}  {m['label']}", key=f"side_pick_{key}"):
                st.session_state.mood_key = key
                st.session_state.messages = [SystemMessage(content=m["prompt"])]
                st.session_state.chat_display = []
                st.rerun()

    st.markdown('<div class="sidebar-label">History</div>', unsafe_allow_html=True)
    user_msgs = [m["text"] for m in st.session_state.chat_display if m["role"] == "user"]
    if not user_msgs:
        st.markdown('<div class="history-empty">No messages yet</div>', unsafe_allow_html=True)
    else:
        for um in user_msgs[-8:][::-1]:
            preview = um if len(um) <= 38 else um[:38] + "…"
            st.markdown(f'<div class="history-item">{preview}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sidebar-footer">Powered by Llama 3.3 70B via Groq</div>', unsafe_allow_html=True)

# ── Model (cached) ───────────────────────────────────────────────────────────
@st.cache_resource
def get_model():
    return ChatGroq(
        api_key=os.getenv('GROQ_API_KEY'),
        model_name='llama-3.3-70b-versatile',
        temperature=0.8,
    )

model = get_model()

# ── Top Mood Pill Bar ─────────────────────────────────────────────────────────
st.markdown('<div class="mood-bar-wrap">', unsafe_allow_html=True)
st.markdown('<div class="moodbar">', unsafe_allow_html=True)
cols = st.columns(len(MOODS))
for i, (key, m) in enumerate(MOODS.items()):
    with cols[i]:
        if key == st.session_state.mood_key:
            st.markdown(f'<div class="mood-pill-active">{m["icon"]} {m["label"]}</div>', unsafe_allow_html=True)
        else:
            if st.button(f"{m['icon']} {m['label']}", key=f"top_pick_{key}"):
                st.session_state.mood_key = key
                st.session_state.messages = [SystemMessage(content=m["prompt"])]
                st.session_state.chat_display = []
                st.rerun()
st.markdown('</div></div>', unsafe_allow_html=True)

# ── Chat Area ────────────────────────────────────────────────────────────────
if not st.session_state.chat_display:
    st.markdown(f"""
    <div class="empty-wrap">
        <div class="empty-icon">{mood['icon']}</div>
        <div class="empty-title">How can I help you today?</div>
        <div class="empty-sub">You're talking to the {mood['label'].lower()} version of the assistant.</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.chat_display:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="msg-row user">
                <div class="bubble user">{msg['text']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="msg-row bot">
                <div class="avatar">{mood['icon']}</div>
                <div class="bubble bot">{msg['text']}</div>
            </div>
            """, unsafe_allow_html=True)

# ── Input Form (Enter key submits, auto-clears, visible text) ───────────────
st.markdown('<div class="input-shell">', unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Ask anything",
            label_visibility="collapsed",
            key="user_msg"
        )
    with col2:
        submitted = st.form_submit_button("Send ↑")

st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<div class="input-hint">Mood AI can make mistakes. Verify important information.</div>', unsafe_allow_html=True)

# ── Handle Submission ──────────────────────────────────────────────────────
if submitted and user_input.strip():
    text = user_input.strip()
    st.session_state.chat_display.append({"role": "user", "text": text})
    st.session_state.messages.append(HumanMessage(content=text))

    with st.spinner("Thinking..."):
        response = model.invoke(st.session_state.messages)

    st.session_state.messages.append(AIMessage(content=response.content))
    st.session_state.chat_display.append({"role": "bot", "text": response.content})
    st.rerun()