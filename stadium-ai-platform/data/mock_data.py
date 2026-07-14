"""
Mock real-time data feeds for the demo.

In a production deployment these would be replaced by:
  - Turnstile / CCTV people-counting feeds -> gate_density()
  - Transit agency APIs (metro/bus) -> transport_status()
  - Stadium IoT sensors (queues, restrooms, concessions) -> facility_status()
  - Weather API -> weather()
  - Incident management system -> live_incidents()

Kept deterministic-ish with slight randomness so the demo feels alive
across reruns without needing any external network calls.
"""

import random
from datetime import datetime

GATES = ["Gate A (North)", "Gate B (East)", "Gate C (South)", "Gate D (West)", "Gate E (VIP)"]
ZONES = ["Lower Bowl", "Upper Bowl", "Club Level", "Fan Fest Plaza", "Parking Deck 2"]
LANGUAGES = ["English", "Spanish", "Portuguese", "French", "Arabic", "Mandarin", "Hindi", "Japanese"]


def gate_density():
    random.seed(datetime.now().minute)  # changes each minute, stable within a run
    data = []
    for gate in GATES:
        pct = random.randint(20, 98)
        wait_min = round(pct / 6, 1)
        data.append({
            "gate": gate,
            "occupancy_pct": pct,
            "est_wait_min": wait_min,
            "status": "critical" if pct > 85 else "busy" if pct > 60 else "normal",
        })
    return data


def transport_status():
    return [
        {"line": "Metro Red Line", "status": "On time", "next_arrival_min": 4},
        {"line": "Shuttle Bus - Lot 7", "status": "Delayed 6 min", "next_arrival_min": 11},
        {"line": "Metro Blue Line", "status": "Crowded - extra cars added", "next_arrival_min": 7},
        {"line": "Rideshare Zone C", "status": "High demand surge", "next_arrival_min": 3},
    ]


def facility_status():
    return [
        {"facility": "Restrooms - Lower Bowl East", "status": "normal"},
        {"facility": "Concessions - Section 114", "status": "long queue"},
        {"facility": "Medical Station 2", "status": "normal"},
        {"facility": "Accessible Seating Lift - Gate D", "status": "out of service"},
        {"facility": "Water Stations", "status": "normal"},
    ]


def weather():
    return {"condition": "Partly cloudy", "temp_c": 29, "heat_index_c": 33, "advisory": "Elevated heat - hydration advised"}


def live_incidents():
    return [
        {"time": "17:42", "zone": "Gate B (East)", "type": "Congestion", "severity": "Medium"},
        {"time": "17:38", "zone": "Parking Deck 2", "type": "Vehicle blocking exit lane", "severity": "Low"},
        {"time": "17:30", "zone": "Section 114", "type": "Medical assist requested", "severity": "High"},
    ]
