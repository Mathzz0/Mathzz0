"""Offline ITSM incident triage example, not connected to ServiceNow."""
from __future__ import annotations
import argparse
import json
from dataclasses import dataclass, asdict
from typing import Sequence

GROUPS = {"access": "Identity & Access", "hardware": "Workplace Support", "software": "Application Support"}
MATRIX = (("P1", "P2", "P3"), ("P2", "P3", "P4"), ("P3", "P4", "P4"))

@dataclass(frozen=True)
class TriageResult:
    category: str
    assignment_group: str
    impact: int
    urgency: int
    priority: str
    state: str = "new"

def triage_incident(category: str, impact: int, urgency: int) -> TriageResult:
    """Apply a fictional category routing and impact/urgency priority matrix."""
    if not isinstance(category, str):
        raise TypeError("category must be a string")
    category = category.strip().lower()
    if category not in GROUPS:
        raise ValueError(f"unknown category: {category!r}")
    for name, value in (("impact", impact), ("urgency", urgency)):
        if isinstance(value, bool) or not isinstance(value, int) or value not in (1, 2, 3):
            raise ValueError(f"{name} must be an integer in [1, 3]")
    return TriageResult(category, GROUPS[category], impact, urgency, MATRIX[impact - 1][urgency - 1])

def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Educational ITSM demo; no production connection.")
    parser.add_argument("--category", required=True, choices=sorted(GROUPS))
    parser.add_argument("--impact", required=True, type=int, choices=(1, 2, 3))
    parser.add_argument("--urgency", required=True, type=int, choices=(1, 2, 3))
    args = parser.parse_args(argv)
    print(json.dumps(asdict(triage_incident(args.category, args.impact, args.urgency)), indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
