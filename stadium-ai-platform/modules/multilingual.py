"""
Module 2: Multilingual Fan Assistant

A GenAI chat assistant that answers fan questions (tickets, food,
transit, rules, first aid, lost & found, etc.) in the fan's own
language, grounded in a small stadium knowledge base so answers
stay accurate to this specific venue instead of hallucinated.
"""

import streamlit as st
from utils.genai_client import ask_genai
from data.mock_data import LANGUAGES

STADIUM_FACTS = """
Venue: MetLife-style Host Stadium, Capacity 82,500.
Gates: A (North), B (East), C (South), D (West), E (VIP).
Bag policy: Clear bags only, max 30x30x15cm.
Re-entry: Not permitted once inside.
Alcohol: Sold until end of 3rd quarter equivalent / 75th minute, ID required (21+ or local law).
Lost & Found: Guest Services booths at Gate A and Gate C.
Accessible seating: Available in all sections, request via Gate D accessibility desk.
Prohibited items: Outside food/drink, professional cameras, drones, weapons, laser pointers.
Nearest hospital: 2.1 km, stadium has 3 on-site medical stations.
Wifi: Free "FIFA2026-FanWifi" network, no password.
"""

SYSTEM_PROMPT = f"""You are a multilingual fan-assistance AI for a FIFA World Cup 2026 stadium.
Ground every answer in these venue facts, never invent policies not listed here:
{STADIUM_FACTS}
Always respond in the language the fan selected, in a warm, concise, helpful tone
(max ~100 words). If the question isn't covered by the facts, say so honestly and
direct them to the nearest Guest Services booth."""

DEMO_FALLBACK = (
    "Lost & Found is located at the Guest Services booths near Gate A and Gate C. "
    "If you lost an item inside your seating section, a steward nearby can also radio "
    "it in immediately. Booths are open from 2 hours before kickoff until 1 hour after "
    "the match ends."
)


def render():
    st.subheader("🌐 Multilingual Fan Assistant")
    st.caption("Ask any stadium question and get an accurate answer in your language, grounded in venue policy.")

    lang = st.selectbox("Respond in:", LANGUAGES)
    question = st.text_area(
        "Your question",
        placeholder="e.g. Where is lost and found? / ¿Dónde puedo comprar comida sin gluten? / أين أقرب مخرج؟",
        height=80,
    )

    if st.button("Ask", type="primary", key="ml_btn") and question.strip():
        with st.spinner("Thinking..."):
            prompt = f"Fan's question (answer in {lang}): {question}"
            result = ask_genai(SYSTEM_PROMPT, prompt, demo_fallback=DEMO_FALLBACK)
        st.success(f"Answer ({lang})")
        st.markdown(result)

    st.divider()
    st.markdown("**Quick-ask templates**")
    qcols = st.columns(3)
    templates = ["Where can I refill water bottles?", "Is there a prayer/quiet room?", "What's the bag policy?"]
    for c, t in zip(qcols, templates):
        c.button(t, key=f"tmpl_{t}", on_click=lambda t=t: st.session_state.update({"ml_prefill": t}))

    with st.expander("Why this matters for FIFA 2026"):
        st.write(
            "The 2026 tournament spans the US, Mexico, and Canada and expects fans from "
            "over 100 countries. Human staff can't cover every language at every gate — "
            "a grounded GenAI assistant gives instant, accurate, native-language support "
            "at scale without stadiums needing to hire specialist interpreters per language."
        )
