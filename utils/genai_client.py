"""
Centralized GenAI client for the Stadium Operations Platform.

All four modules (Navigation, Multilingual Assistant, Accessibility,
Operational Intelligence) route their AI calls through this single
wrapper so the app has one place to:
  - swap models/providers
  - enforce consistent system prompts
  - handle retries / graceful degradation when no API key is present
    (useful for judges running the demo without setting up billing)
"""

from __future__ import annotations

import json
import logging
import os

import streamlit as st

try:
    import anthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:
    _ANTHROPIC_AVAILABLE = False

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-5"
DEMO_MODE_NOTICE = (
    "⚠️ Running in DEMO MODE (no ANTHROPIC_API_KEY set). "
    "Showing a realistic sample response instead of a live model call. "
    "Add your key to `.env` to enable live GenAI responses."
)
GENAI_FAILURE_NOTICE = (
    "⚠️ GenAI call failed. Showing fallback response instead. "
    "(Details were logged server-side.)"
)


@st.cache_resource(show_spinner=False)
def _get_client() -> anthropic.Anthropic | None:
    """
    Cached with st.cache_resource: Streamlit reruns the entire script on
    every widget interaction, so without caching this would construct a
    brand-new HTTP client/connection pool on every single click. Caching
    it as a resource means the client (and its underlying connection
    pool) is built once per session and reused.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key or not _ANTHROPIC_AVAILABLE:
        return None
    return anthropic.Anthropic(api_key=api_key)


def is_live() -> bool:
    return _get_client() is not None


def ask_genai(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 800,
    demo_fallback: str = "",
) -> str:
    """
    Single entry point every module uses to call the GenAI model.
    Falls back to a supplied demo string if no API key is configured,
    so the app is fully demoable out of the box.
    """
    client = _get_client()
    if client is None:
        return f"{DEMO_MODE_NOTICE}\n\n{demo_fallback}"

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        return response.content[0].text
    except Exception:
        # Log full details server-side only - never surface raw exception
        # text (which can include request internals) directly to the UI.
        logger.exception("GenAI call failed")
        return f"{GENAI_FAILURE_NOTICE}\n\n{demo_fallback}"


def ask_genai_json(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 800,
    demo_fallback: dict | None = None,
) -> dict:
    """
    Same as ask_genai but expects/parses a JSON object back from the model.
    Used for structured outputs (e.g. route steps, alert lists).
    """
    client = _get_client()
    if client is None:
        return demo_fallback or {}

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system_prompt + "\nRespond with ONLY valid JSON, no prose, no markdown fences.",
            messages=[{"role": "user", "content": user_prompt}],
        )
        text = response.content[0].text.strip()
        text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(text)
    except Exception:
        logger.exception("GenAI JSON call failed")
        return demo_fallback or {}
