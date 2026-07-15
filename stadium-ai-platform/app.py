"""
Stadium Ops AI — a GenAI-enabled platform for FIFA World Cup 2026
stadium operations and fan experience.

Run with:
    streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

from modules import accessibility, multilingual, navigation, operations
from utils.genai_client import is_live

load_dotenv()

st.set_page_config(
    page_title="Stadium Ops AI — FIFA World Cup 2026",
    page_icon="⚽",
    layout="wide",
)

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("⚽ Stadium Ops AI")
st.caption("A GenAI-enabled solution for stadium operations & fan experience — built for FIFA World Cup 2026")

with st.sidebar:
    st.header("About")
    st.write(
        "One platform, four GenAI-powered modules covering navigation, "
        "multilingual support, accessibility, and operational intelligence "
        "for FIFA World Cup 2026 host venues."
    )
    st.divider()
    if is_live():
        st.success("GenAI: Live (Anthropic API connected)")
    else:
        st.warning("GenAI: Demo mode (no API key set)")
        st.caption("Add ANTHROPIC_API_KEY to a `.env` file to enable live model calls.")
    st.divider()
    st.caption("Built for the AI Code Submission Challenge — Challenge 4")

tab1, tab2, tab3, tab4 = st.tabs([
    "🧭 Navigation & Crowd",
    "🌐 Multilingual Assistant",
    "♿ Accessibility",
    "📊 Operational Intelligence",
])

with tab1:
    navigation.render()

with tab2:
    multilingual.render()

with tab3:
    accessibility.render()

with tab4:
    operations.render()

st.divider()
st.caption(
    "Stadium Ops AI · Prototype for demonstration purposes · All stadium data shown is simulated."
)
