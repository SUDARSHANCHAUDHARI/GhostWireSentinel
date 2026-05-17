"""Tests for GhostWire Sentinel MVP detection behavior."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from agent.allowlist import apply_allowlist, load_allowlist
from agent.detectors.anomaly import detect_anomalies
from agent.detectors.beaconing import detect_beaconing
from agent.detectors.persistence import detect_persistence
from agent.report import build_anomaly_report, build_markdown_report, build_timeline_report, top_priorities


ROOT = Path(__file__).resolve().parents[1]


def load_sample(name: str) -> dict:
    return json.loads((ROOT / "data" / name).read_text(encoding="utf-8"))


class DetectionTests(unittest.TestCase):
    """MVP detection tests."""

    def test_detects_baseline_drift(self) -> None:
        baseline = load_sample("baseline-snapshot.json")
        current = load_sample("current-snapshot.json")

        findings = detect_anomalies(current, baseline)

        kinds = {finding["kind"] for finding in findings}
        self.assertIn("baseline.new_cron_jobs", kinds)
        self.assertIn("baseline.new_ssh_keys", kinds)
        self.assertIn("baseline.new_services", kinds)

    def test_detects_persistence_patterns(self) -> None:
        current = load_sample("current-snapshot.json")

        findings = detect_persistence(current)

        self.assertTrue(any(finding["kind"] == "persistence.cron" for finding in findings))
        self.assertTrue(any(finding["kind"] == "persistence.service" for finding in findings))

    def test_detects_suspicious_connection_and_repetition(self) -> None:
        current = load_sample("current-snapshot.json")

        findings = detect_beaconing(current["connections"])

        self.assertTrue(any(finding["kind"] == "connection.suspicious" for finding in findings))
        self.assertTrue(any(finding["kind"] == "connection.repeated_remote" for finding in findings))

    def test_report_contains_findings_summary(self) -> None:
        baseline = load_sample("baseline-snapshot.json")
        current = load_sample("current-snapshot.json")
        findings = [
            *detect_anomalies(current, baseline),
            *detect_persistence(current),
            *detect_beaconing(current["connections"]),
        ]

        report = build_markdown_report(findings, current, baseline)

        self.assertIn("GhostWire Sentinel Incident Report", report)
        self.assertIn("Total findings", report)
        self.assertIn("Priority Queue", report)
        self.assertIn("Recommended next step", report)
        self.assertIn("New SSH key observed outside baseline", report)

    def test_report_builds_anomaly_breakdown(self) -> None:
        baseline = load_sample("baseline-snapshot.json")
        current = load_sample("current-snapshot.json")
        findings = [
            *detect_anomalies(current, baseline),
            *detect_persistence(current),
            *detect_beaconing(current["connections"]),
        ]

        report = build_anomaly_report(findings, current, baseline)
        priorities = top_priorities(findings)

        self.assertEqual("critical", priorities[0]["severity"])
        self.assertIn("Detection Breakdown", report)
        self.assertIn("baseline.new_ssh_keys", report)

    def test_allowlist_suppresses_matching_finding(self) -> None:
        baseline = load_sample("baseline-snapshot.json")
        current = load_sample("current-snapshot.json")
        findings = detect_anomalies(current, baseline)

        active, suppressed = apply_allowlist(findings, load_allowlist(ROOT / "rules/allowlist.json"))

        self.assertTrue(any(item["kind"] == "baseline.new_processes" for item in suppressed))
        self.assertFalse(any(item["kind"] == "baseline.new_processes" for item in active))

    def test_timeline_report_includes_suppressed_count(self) -> None:
        baseline = load_sample("baseline-snapshot.json")
        current = load_sample("current-snapshot.json")
        findings = [
            *detect_anomalies(current, baseline),
            *detect_persistence(current),
            *detect_beaconing(current["connections"]),
        ]
        active, suppressed = apply_allowlist(findings, load_allowlist(ROOT / "rules/allowlist.json"))

        report = build_timeline_report(active, current, baseline, suppressed)

        self.assertIn("GhostWire Sentinel Timeline Report", report)
        self.assertIn("Allow-listed findings suppressed", report)


if __name__ == "__main__":
    unittest.main()
