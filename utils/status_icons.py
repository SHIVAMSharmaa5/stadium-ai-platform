"""
Shared status -> emoji-icon mapping.

Centralizes the "🔴 critical / 🟡 busy / 🟢 normal" style lookups that were
previously duplicated as inline ternary chains in navigation.py,
operations.py, and accessibility.py.
"""

from __future__ import annotations

_GATE_ICONS: dict[str, str] = {
    "critical": "🔴",
    "busy": "🟡",
    "normal": "🟢",
}

_SEVERITY_ICONS: dict[str, str] = {
    "High": "🔴",
    "Medium": "🟡",
    "Low": "🟢",
}


def gate_status_icon(status: str) -> str:
    """Icon for a gate/facility occupancy status (critical/busy/normal)."""
    return _GATE_ICONS.get(status, "🟢")


def severity_icon(severity: str) -> str:
    """Icon for an incident severity level (High/Medium/Low)."""
    return _SEVERITY_ICONS.get(severity, "🟢")


def facility_ok_icon(status: str) -> str:
    """Icon for a binary facility status: 'normal' vs anything else."""
    return "🟢" if status == "normal" else "🔴"
