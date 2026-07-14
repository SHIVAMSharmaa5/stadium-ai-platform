import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from data.mock_data import gate_density, transport_status, facility_status, weather, live_incidents, GATES


class TestMockData(unittest.TestCase):

    def test_gate_density_covers_all_gates(self):
        data = gate_density()
        gates_returned = {d["gate"] for d in data}
        self.assertEqual(gates_returned, set(GATES))

    def test_gate_density_fields_and_ranges(self):
        for entry in gate_density():
            self.assertIn("occupancy_pct", entry)
            self.assertTrue(0 <= entry["occupancy_pct"] <= 100)
            self.assertIn(entry["status"], {"normal", "busy", "critical"})
            self.assertGreaterEqual(entry["est_wait_min"], 0)

    def test_gate_status_thresholds_consistent(self):
        for entry in gate_density():
            pct = entry["occupancy_pct"]
            if pct > 85:
                self.assertEqual(entry["status"], "critical")
            elif pct > 60:
                self.assertEqual(entry["status"], "busy")
            else:
                self.assertEqual(entry["status"], "normal")

    def test_transport_status_nonempty(self):
        self.assertGreater(len(transport_status()), 0)
        for t in transport_status():
            self.assertIn("line", t)
            self.assertIn("status", t)

    def test_facility_status_nonempty(self):
        self.assertGreater(len(facility_status()), 0)

    def test_weather_has_required_fields(self):
        wx = weather()
        for key in ("condition", "temp_c", "heat_index_c", "advisory"):
            self.assertIn(key, wx)

    def test_live_incidents_have_severity(self):
        for i in live_incidents():
            self.assertIn(i["severity"], {"Low", "Medium", "High"})


if __name__ == "__main__":
    unittest.main()
