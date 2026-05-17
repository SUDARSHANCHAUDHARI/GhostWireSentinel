"""Detect baseline anomalies."""

from __future__ import annotations

from agent.baseline.compare import compare_snapshot


def detect_anomalies(current: dict, baseline: dict) -> list[dict]:
    """Return baseline drift findings."""
    drift = compare_snapshot(current, baseline)
    findings: list[dict] = []
    severity_by_section = {
        "new_processes": "medium",
        "new_services": "high",
        "new_cron_jobs": "high",
        "new_ssh_keys": "critical",
        "new_connections": "medium",
    }
    labels = {
        "new_processes": "New process observed outside baseline.",
        "new_services": "New service observed outside baseline.",
        "new_cron_jobs": "New cron job observed outside baseline.",
        "new_ssh_keys": "New SSH key observed outside baseline.",
        "new_connections": "New outbound connection observed outside baseline.",
    }
    for section, items in drift.items():
        for item in items:
            findings.append(
                {
                    "kind": f"baseline.{section}",
                    "severity": severity_by_section.get(section, "low"),
                    "summary": labels.get(section, "New baseline drift observed."),
                    "evidence": item,
                }
            )
    return findings
