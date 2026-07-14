"""
Module 4: Operational Intelligence & Real-Time Decision Support

Aggregates all live feeds (gates, transport, facilities, weather,
incidents) and asks GenAI to produce an executive-style operations
briefing with prioritized recommended actions - the kind a control
room commander would want every 10-15 minutes on match day.
"""

import streamlit as st
from data.mock_data import gate_density, transport_status, facility_status, weather, live_incidents
from utils.genai_client import ask_genai

SYSTEM_PROMPT = """You are the operations-intelligence AI for a FIFA World Cup 2026
stadium control room. You receive live feeds from gates, transit, facilities, weather,
and incident logs. Produce a concise command briefing with:
1. Overall status (Green/Yellow/Red) with one-line justification
2. Top 3 prioritized actions the operations team should take right now
3. Any single most urgent item needing immediate escalation
Be direct and operational - this is read by trained staff, not the public.
Max ~180 words."""

DEMO_FALLBACK = """**Status: 🟡 YELLOW** — one high-severity incident and one critical gate; overall flow still manageable.

**Top 3 actions:**
1. Divert arriving fans from Gate B (91% capacity) to Gate C via updated signage and
   steward redirection — Gate B will hit critical/unsafe density within ~15 min at
   current inflow rate.
2. Dispatch a second medical team to Section 114 to support the active medical assist
   and clear the concession queue backing into the concourse.
3. Add capacity/extra cars on the Metro Blue Line partnership feed — current crowding
   there is a leading indicator of the Gate B surge.

**Escalate now:** Medical assist request in Section 114 (17:30, High severity) —
confirm response team ETA.

**Note:** Heat index at 33°C — trigger hydration-station announcement stadium-wide."""


def render():
    st.subheader("📊 Operational Intelligence Dashboard")
    st.caption("Live control-room view with an AI-generated briefing and prioritized action list.")

    density = gate_density()
    transit = transport_status()
    facilities = facility_status()
    wx = weather()
    incidents = live_incidents()

    c1, c2, c3, c4 = st.columns(4)
    critical_gates = sum(1 for g in density if g["status"] == "critical")
    c1.metric("Critical gates", critical_gates)
    c2.metric("Open incidents", len(incidents))
    high_sev = sum(1 for i in incidents if i["severity"] == "High")
    c3.metric("High-severity", high_sev)
    c4.metric("Heat index", f"{wx['heat_index_c']}°C")

    with st.expander("Live incident log", expanded=True):
        for i in incidents:
            sev_icon = "🔴" if i["severity"] == "High" else "🟡" if i["severity"] == "Medium" else "🟢"
            st.write(f"{sev_icon} `{i['time']}` **{i['zone']}** — {i['type']} ({i['severity']})")

    with st.expander("Transit feed"):
        for t in transit:
            st.write(f"🚆 **{t['line']}** — {t['status']} (next: {t['next_arrival_min']} min)")

    with st.expander("Facility status"):
        for f in facilities:
            icon = "🟢" if f["status"] == "normal" else "🔴"
            st.write(f"{icon} {f['facility']} — {f['status']}")

    if st.button("Generate Command Briefing", type="primary", key="ops_btn"):
        with st.spinner("Synthesizing live feeds into a briefing..."):
            prompt = (
                f"Gate density: {density}\nTransit: {transit}\nFacilities: {facilities}\n"
                f"Weather: {wx}\nIncidents: {incidents}"
            )
            result = ask_genai(SYSTEM_PROMPT, prompt, demo_fallback=DEMO_FALLBACK)
        st.success("AI Command Briefing")
        st.markdown(result)

    with st.expander("Why this matters for FIFA 2026"):
        st.write(
            "Control rooms during World Cup matches ingest dozens of disconnected data "
            "feeds. Human operators can miss correlations across systems under pressure. "
            "This module fuses every feed into a single GenAI-generated briefing every "
            "few minutes, so commanders spend their attention on decisions, not on "
            "manually cross-referencing dashboards."
        )
