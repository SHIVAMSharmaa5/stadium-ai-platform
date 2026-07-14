import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from unittest.mock import patch

from utils.genai_client import ask_genai, ask_genai_json, is_live


class TestGenAIClientDemoMode(unittest.TestCase):
    """
    These tests force demo mode (no API key) so they run without any
    network access or credentials - suitable for CI.
    """

    @patch.dict(os.environ, {}, clear=True)
    def test_is_live_false_without_key(self):
        self.assertFalse(is_live())

    @patch.dict(os.environ, {}, clear=True)
    def test_ask_genai_returns_fallback_when_no_key(self):
        result = ask_genai("system", "prompt", demo_fallback="FALLBACK_TEXT")
        self.assertIn("FALLBACK_TEXT", result)
        self.assertIn("DEMO MODE", result)

    @patch.dict(os.environ, {}, clear=True)
    def test_ask_genai_json_returns_fallback_dict(self):
        fallback = {"status": "ok"}
        result = ask_genai_json("system", "prompt", demo_fallback=fallback)
        self.assertEqual(result, fallback)

    @patch.dict(os.environ, {}, clear=True)
    def test_ask_genai_json_empty_fallback_default(self):
        result = ask_genai_json("system", "prompt")
        self.assertEqual(result, {})


if __name__ == "__main__":
    unittest.main()
