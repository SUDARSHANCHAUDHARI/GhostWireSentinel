"""Allow-list support for approved GhostWire Sentinel findings."""

from __future__ import annotations

from pathlib import Path
import json


def load_allowlist(path: Path | None) -> dict:
    """Load an allow-list document, returning an empty one when absent."""
    if path is None or not path.exists():
        return {"items": []}
    return json.loads(path.read_text(encoding="utf-8"))


def _matches_value(expected: object, actual: object) -> bool:
    if expected == "*":
        return True
    return str(expected) == str(actual)


def _matches_evidence(expected: dict, evidence: dict) -> bool:
    return all(_matches_value(value, evidence.get(key, "")) for key, value in expected.items())


def is_allowed(finding: dict, allowlist: dict) -> bool:
    """Return whether a finding matches an approved allow-list item."""
    for item in allowlist.get("items", []):
        if item.get("kind") != finding.get("kind"):
            continue
        expected_evidence = item.get("evidence", {})
        if _matches_evidence(expected_evidence, finding.get("evidence", {})):
            return True
    return False


def apply_allowlist(findings: list[dict], allowlist: dict) -> tuple[list[dict], list[dict]]:
    """Split findings into active and suppressed findings."""
    active: list[dict] = []
    suppressed: list[dict] = []
    for finding in findings:
        if is_allowed(finding, allowlist):
            copy = dict(finding)
            copy["suppressed"] = True
            suppressed.append(copy)
        else:
            active.append(finding)
    return active, suppressed
