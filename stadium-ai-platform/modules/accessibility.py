"""
Module 3: Accessibility Concierge

Generates personalized accessibility plans for fans and flags
accessibility-equipment outages to venue staff so they can be
fixed before they become a problem on match day.
"""

import streamlit as st
from utils.genai_client import ask_genai
from data.mock_data import facility_status

SYSTEM_PROMPT = """You are an accessibility-planning AI for a FIFA World Cup 2026 stadium.
Given a fan's stated accessibility needs, produce a short, practical personalized
plan covering: best gate/entrance, seating notes, route considerations (ramps vs
stairs, lift status), and any relevant staff contact point. Be respectful, specific,
and never make medical assumptions beyond what the fan stated. Max ~150 words."""

DEMO_FALLBACK = """**Personalized Access Plan**

- **Entrance:** Use Gate D (West) — has the widest accessible entry lane and shortest
  distance from designated accessible parking.
- **Note:** The accessible-seating lift at Gate D is currently flagged out of service —
  reroute via Gate A's ramp instead (adds ~4 min).
- **Seating:** Wheelchair-accessible seating with companion seats available in
  Sections 104, 118, and 210 — closest to a restroom with an accessible stall is 118.
- **Staff contact:** Accessibility Desk near Gate A, look for the blue-vest stewards.
- **Sensory note:** A quiet room (reduced light/sound) is available near Section 130
  if needed at halftime."""


def render():
    st.subheader("♿ Accessibility Concierge")
    st.caption("GenAI builds a personalized access plan, and flags equipment issues to staff in real time.")

    tab1, tab2 = st.tabs(["For Fans", "For Venue Staff"])

    with tab1:
        needs = st.multiselect(
            "Select relevant accessibility needs",
            ["Wheelchair user", "Limited mobility / uses cane", "Low vision", "Blind",
             "Deaf / hard of hearing", "Sensory sensitivity (autism-friendly space)",
             "Service animal", "Cognitive/intellectual disability support"],
        )
        notes = st.text_input("Anything else we should know? (optional)")

        if st.button("Generate My Access Plan", type="primary", key="acc_btn"):
            if not needs:
                st.warning("Select at least one need so the plan can be personalized.")
            else:
                with st.spinner("Building your access plan..."):
                    facilities = facility_status()
                    prompt = (
                        f"Fan needs: {', '.join(needs)}. Additional notes: {notes or 'none'}. "
                        f"Current facility status: {facilities}."
                    )
                    result = ask_genai(SYSTEM_PROMPT, prompt, demo_fallback=DEMO_FALLBACK)
                st.success("Your Access Plan")
                st.markdown(result)

    with tab2:
        st.markdown("**Live accessibility-equipment status**")
        for f in facility_status():
            icon = "🔴" if f["status"] not in ("normal",) else "🟢"
            st.write(f"{icon} {f['facility']} — {f['status']}")
        st.caption("Flagged items are auto-routed to the facilities team with priority "
                    "if they affect accessible seating, ramps, or lifts.")

    with st.expander("Why this matters for FIFA 2026"):
        st.write(
            "FIFA's accessibility guidelines require host venues to provide equitable "
            "access for fans with a wide range of needs. A GenAI concierge scales "
            "personalized guidance that would otherwise require large specialist teams, "
            "and real-time equipment monitoring prevents a broken lift from becoming a "
            "match-day access failure."
        )
