"""Command line interface for the GhostWire Sentinel MVP."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent.baseline.snapshot import build_snapshot
from agent.detectors.anomaly import detect_anomalies
from agent.detectors.beaconing import detect_beaconing
from agent.detectors.persistence import detect_persistence
from agent.report import build_anomaly_report, build_markdown_report, sort_findings


def load_json(path: Path) -> dict:
    """Load a JSON object from disk."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict | list[dict]) -> None:
    """Write a formatted JSON payload."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def collect_command(args: argparse.Namespace) -> None:
    """Collect a host snapshot."""
    snapshot = build_snapshot()
    write_json(args.output, snapshot)
    print(f"Wrote snapshot to {args.output}")


def analyze_command(args: argparse.Namespace) -> None:
    """Analyze current state against a baseline."""
    current = load_json(args.current)
    baseline = load_json(args.baseline)
    findings = sort_findings(
        [
            *detect_anomalies(current, baseline),
            *detect_persistence(current),
            *detect_beaconing(current.get("connections", [])),
        ]
    )
    write_json(args.findings, findings)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(build_markdown_report(findings, current, baseline), encoding="utf-8")
    args.anomaly_report.parent.mkdir(parents=True, exist_ok=True)
    args.anomaly_report.write_text(build_anomaly_report(findings, current, baseline), encoding="utf-8")
    print(f"Wrote {len(findings)} findings to {args.findings}")
    print(f"Wrote report to {args.report}")
    print(f"Wrote anomaly report to {args.anomaly_report}")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(description="GhostWire Sentinel MVP")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collect = subparsers.add_parser("collect", help="Collect a local device snapshot")
    collect.add_argument("--output", type=Path, default=Path("data/current-snapshot.json"))
    collect.set_defaults(func=collect_command)

    analyze = subparsers.add_parser("analyze", help="Analyze a current snapshot against a baseline")
    analyze.add_argument("--baseline", type=Path, required=True)
    analyze.add_argument("--current", type=Path, required=True)
    analyze.add_argument("--findings", type=Path, default=Path("reports/findings.json"))
    analyze.add_argument("--report", type=Path, default=Path("reports/incident-summary.md"))
    analyze.add_argument("--anomaly-report", type=Path, default=Path("reports/anomaly-report.md"))
    analyze.set_defaults(func=analyze_command)

    return parser


def main() -> None:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
