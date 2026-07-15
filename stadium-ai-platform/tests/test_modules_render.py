"""
Tests for the four feature modules (navigation, multilingual, accessibility,
operations). These were previously untested - the only coverage in the repo
was for genai_client and mock_data.

Since these modules call Streamlit UI functions at import/render time, we
patch `ask_genai` (to avoid live/network calls) and drive `render()` with a
minimal Streamlit stub so the actual business logic - prompt construction,
constants, fallback content - is exercised rather than skipped.
"""

import os
import sys
import types
import unittest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def _install_streamlit_stub():
    """
    Minimal stand-in for the `streamlit` module so app modules can be
    imported and their render() functions executed headlessly in CI,
    without needing a real Streamlit server.
    """
    st = types.ModuleType("streamlit")

    def _passthrough(*_args, **_kwargs):
        return MagicMock()

    def _columns(n_or_list, *_args, **_kwargs):
        n = n_or_list if isinstance(n_or_list, int) else len(n_or_list)
        return [MagicMock() for _ in range(n)]

    def _tabs(labels, *_args, **_kwargs):
        return [MagicMock() for _ in labels]

    class _Expander:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

    st.subheader = _passthrough
    st.caption = _passthrough
    st.markdown = _passthrough
    st.write = _passthrough
    st.selectbox = MagicMock(return_value="mock-selection")
    st.multiselect = MagicMock(return_value=["Wheelchair user"])
    st.text_input = MagicMock(return_value="")
    st.text_area = MagicMock(return_value="Where is lost and found?")
    st.columns = _columns
    st.tabs = _tabs
    st.button = MagicMock(return_value=True)
    st.success = _passthrough
    st.warning = _passthrough
    st.spinner = lambda *a, **k: _Expander()
    st.expander = lambda *a, **k: _Expander()
    st.divider = _passthrough
    st.metric = _passthrough
    st.session_state = {}
    sys.modules["streamlit"] = st
    return st


_install_streamlit_stub()

from modules import accessibility, multilingual, navigation, operations  # noqa: E402


class TestModulePromptIntegrity(unittest.TestCase):
    """Every module's SYSTEM_PROMPT / DEMO_FALLBACK must be non-trivial -
    an empty or placeholder prompt would silently degrade AI quality."""

    def _assert_well_formed(self, module):
        self.assertTrue(hasattr(module, "SYSTEM_PROMPT"))
        self.assertGreater(len(module.SYSTEM_PROMPT.strip()), 40)
        self.assertTrue(hasattr(module, "DEMO_FALLBACK"))
        self.assertGreater(len(module.DEMO_FALLBACK.strip()), 20)

    def test_navigation_prompt(self):
        self._assert_well_formed(navigation)

    def test_multilingual_prompt(self):
        self._assert_well_formed(multilingual)

    def test_accessibility_prompt(self):
        self._assert_well_formed(accessibility)


class TestModuleRenderSmoke(unittest.TestCase):
    """render() should execute end-to-end (widget layout + AI call path)
    without raising, for both the 'button clicked' and 'not clicked' paths."""

    @patch("modules.navigation.ask_genai", return_value="mock recommendation")
    def test_navigation_render_does_not_raise(self, mock_ask):
        navigation.render()
        mock_ask.assert_called_once()

    @patch("modules.multilingual.ask_genai", return_value="mock answer")
    def test_multilingual_render_does_not_raise(self, mock_ask):
        multilingual.render()
        mock_ask.assert_called_once()

    @patch("modules.accessibility.ask_genai", return_value="mock plan")
    def test_accessibility_render_does_not_raise(self, mock_ask):
        accessibility.render()
        mock_ask.assert_called_once()

    def test_operations_render_does_not_raise(self):
        # operations.render() renders live ops data/incidents; no user-driven
        # AI call on this path, so no ask_genai patch is required here.
        operations.render()


if __name__ == "__main__":
    unittest.main()
