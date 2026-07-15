import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest

from utils.status_icons import facility_ok_icon, gate_status_icon, severity_icon


class TestGateStatusIcon(unittest.TestCase):
    def test_critical(self):
        self.assertEqual(gate_status_icon("critical"), "🔴")

    def test_busy(self):
        self.assertEqual(gate_status_icon("busy"), "🟡")

    def test_normal(self):
        self.assertEqual(gate_status_icon("normal"), "🟢")

    def test_unknown_status_defaults_to_normal_icon(self):
        self.assertEqual(gate_status_icon("something-unexpected"), "🟢")


class TestSeverityIcon(unittest.TestCase):
    def test_high(self):
        self.assertEqual(severity_icon("High"), "🔴")

    def test_medium(self):
        self.assertEqual(severity_icon("Medium"), "🟡")

    def test_low(self):
        self.assertEqual(severity_icon("Low"), "🟢")

    def test_unknown_severity_defaults_to_low_icon(self):
        self.assertEqual(severity_icon("Unknown"), "🟢")


class TestFacilityOkIcon(unittest.TestCase):
    def test_normal_is_green(self):
        self.assertEqual(facility_ok_icon("normal"), "🟢")

    def test_any_other_status_is_red(self):
        self.assertEqual(facility_ok_icon("out of service"), "🔴")
        self.assertEqual(facility_ok_icon("long queue"), "🔴")


if __name__ == "__main__":
    unittest.main()
