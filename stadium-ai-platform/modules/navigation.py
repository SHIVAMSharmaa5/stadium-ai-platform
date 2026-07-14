"""
Module 1: Smart Navigation & Crowd Management

Uses GenAI to turn raw occupancy sensor data into a plain-language,
prioritized recommendation for a fan trying to enter/move through
the stadium right now - including which gate to use, expected wait,
and an alternate if their preferred gate is congested.
"""

import streamlit as st
from data.mock_data import gate_density, ZONES
from utils.genai_client import ask_genai

SYSTEM_PROMPT = """You are the crowd-management AI for a FIFA World Cup 2026 host stadium.
You receive live gate occupancy data and must give fans and stewards clear,
safety-first, non-technical guidance. Always:
- Recommend the single best gate/route given the fan's situation
- Give a realistic wait-time estimate
- Flag any gate that is at critical capacity and should be avoided
- Keep the tone calm, concise, and actionable (max ~120 words)
"""

DEMO_FALLBACK = """**Recommended: Gate C (South)** — est. wait 6 min, currently at 42% capacity.

Avoid **Gate B (East)** — 91% capacity, waits over 15 min, stewards are actively
metering entry there.

If you're coming from the Metro Blue Line, exit toward the South plaza and
follow the green wayfinding signs — this route also avoids the Fan Fest Plaza
bottleneck currently forming near the big screen.

Reassess in ~10 minutes if conditions change."""


def render():
    st.subheader("🧭 Smart Navigation & Crowd Management")
    st.caption("Real-time, GenAI-generated routing that reacts to live crowd density across gates and zones.")

    col1, col2 = st.columns([1, 1])
    with col1:
        entry_point = st.selectbox("Where are you arriving from?", [
            "Metro Red Line", "Metro Blue Line", "Shuttle Bus - Lot 7",
            "Rideshare Zone C", "Parking Deck 2", "Walking - City Center"
        ])
    with col2:
        destination = st.selectbox("Your seating zone", ZONES)

    density = gate_density()
    st.markdown("**Live gate occupancy**")
    cols = st.columns(len(density))
    for c, g in zip(cols, density):
        emoji = "🔴" if g["status"] == "critical" else "🟡" if g["status"] == "busy" else "🟢"
        c.metric(g["gate"], f"{g['occupancy_pct']}%", f"{g['est_wait_min']} min wait")
        c.caption(f"{emoji} {g['status']}")

    if st.button("Get AI Route Recommendation", type="primary", key="nav_btn"):
        with st.spinner("Analyzing live gate data..."):
            prompt = (
                f"Fan is arriving via: {entry_point}. Their seating zone is: {destination}. "
                f"Live gate data: {density}. Recommend the best gate and route."
            )
            result = ask_genai(SYSTEM_PROMPT, prompt, demo_fallback=DEMO_FALLBACK)
        st.success("AI Recommendation")
        st.markdown(result)

    with st.expander("Why this matters for FIFA 2026"):
        st.write(
            "World Cup host stadiums see entry surges of 40,000+ fans within a 90-minute "
            "window. Static signage can't react to real-time bottlenecks. This module lets "
            "operators broadcast AI-generated, situation-specific guidance to fans' phones "
            "and stadium screens as conditions change minute to minute."
        )
