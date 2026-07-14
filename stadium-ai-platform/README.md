# ⚽ Stadium Ops AI — FIFA World Cup 2026

A GenAI-enabled platform that enhances stadium operations and the fan
tournament experience across **four** of the challenge's focus areas in a
single unified app:

| Module | Focus Area | What it does |
|---|---|---|
| 🧭 Navigation & Crowd | Navigation, Crowd Management | Reads live gate-occupancy data and generates a plain-language routing recommendation for a fan, avoiding congested gates in real time |
| 🌐 Multilingual Assistant | Multilingual Assistance | A GenAI chat assistant that answers fan questions (tickets, food, transit, policy) in 8+ languages, grounded in venue facts to avoid hallucination |
| ♿ Accessibility Concierge | Accessibility | Builds a personalized access plan for fans with disabilities and gives staff a live view of accessibility-equipment (lifts/ramps) status |
| 📊 Operational Intelligence | Operational Intelligence, Real-Time Decision Support | Fuses gate, transit, facility, weather, and incident feeds into a single AI-generated control-room briefing with prioritized actions |

## Why GenAI (not just rules/lookups)

Each module hands live, structured stadium data to an LLM (Claude) with a
task-specific system prompt, and the model produces **reasoned, situational,
natural-language output** — a routing decision that weighs multiple gates
against a fan's specific entry point, a briefing that prioritizes across five
unrelated data feeds, a multilingual answer grounded in venue policy. This is
qualitatively different from a static FAQ or a simple threshold alert, and is
the core "mandatory GenAI" requirement of the challenge.

## Architecture

```
stadium-ai-platform/
├── app.py                  # Streamlit entrypoint, tab layout
├── modules/
│   ├── navigation.py        # Module 1
│   ├── multilingual.py       # Module 2
│   ├── accessibility.py      # Module 3
│   └── operations.py         # Module 4
├── utils/
│   └── genai_client.py       # Single wrapper around the Anthropic API,
│                              # shared by all 4 modules, with demo-mode
│                              # fallback so the app runs without a key
├── data/
│   └── mock_data.py          # Simulated real-time sensor/transit/incident
│                              # feeds (swap for real IoT/transit APIs in prod)
├── requirements.txt
├── .env.example
└── .streamlit/config.toml
```

**Production swap-in path:** `data/mock_data.py` is the only file that would
be replaced with real integrations — turnstile people-counters, transit
agency APIs, IoT facility sensors, and an incident-management system. Every
other file is integration-agnostic.

## Setup

```bash
git clone <this-repo>
cd stadium-ai-platform
python -m venv venv && source venv/bin/activate   # optional but recommended
pip install -r requirements.txt

cp .env.example .env
# edit .env and add your ANTHROPIC_API_KEY

streamlit run app.py
```

The app runs in **demo mode** with realistic fallback responses if no API key
is set, so it's fully explorable without any setup — set `ANTHROPIC_API_KEY`
to enable live model calls.

## Design choices & evaluation criteria

- **Code quality:** modular by concern (one file per feature), a single
  shared GenAI client to avoid duplicated API logic, docstrings throughout.
- **Security:** API key loaded from environment only, never hardcoded;
  `.env` is gitignored; no secrets committed.
- **Efficiency:** one lightweight shared client, mock data generation is
  O(1) per render, no unnecessary re-renders of unrelated tabs.
- **Testing:** see `tests/` for unit tests on the mock data generator and
  the GenAI client's demo-mode fallback behavior (no network required).
- **Accessibility:** module 3 is dedicated to accessibility; the UI itself
  uses Streamlit's native components (screen-reader friendly), high-contrast
  theme, and text-first output rather than icon-only signals.
- **Problem statement alignment:** table above maps each module directly to
  a focus area named in the challenge brief (navigation, crowd management,
  accessibility, multilingual assistance, operational intelligence,
  real-time decision support).

## Limitations & next steps

- Data feeds are simulated; a production version integrates real turnstile,
  transit, and IoT sensor APIs.
- No persistence layer yet — briefings/plans are generated fresh each call;
  a production system would log briefings for audit and trend analysis.
- Multilingual module currently supports 8 languages; expandable by editing
  `data/mock_data.py::LANGUAGES`.
- Transportation and sustainability focus areas from the brief are natural
  next modules (e.g., AI-optimized shuttle dispatch, carbon-aware routing).
