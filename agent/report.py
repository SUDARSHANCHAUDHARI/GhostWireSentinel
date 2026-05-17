"""Build human-readable GhostWire Sentinel reports."""

from __future__ import annotations

from datetime import datetime, timezone


SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def sort_findings(findings: list[dict]) -> list[dict]:
    """Return findings sorted by severity."""
    return sorted(
        findings,
        key=lambda finding: SEVERITY_ORDER.get(str(finding.get("severity", "")).lower(), 0),
        reverse=True,
    )


def build_markdown_report(findings: list[dict], current: dict, baseline: dict | None = None) -> str:
    """Return a Markdown incident report."""
    sorted_findings = sort_findings(findings)
    metadata = current.get("metadata", {})
    baseline_metadata = (baseline or {}).get("metadata", {})
    lines = [
        "# GhostWire Sentinel Incident Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        f"Host: {metadata.get('hostname', 'unknown')}",
        f"Snapshot captured: {metadata.get('captured_at', 'unknown')}",
    ]
    if baseline_metadata:
        lines.append(f"Baseline captured: {baseline_metadata.get('captured_at', 'unknown')}")
    lines.extend(
        [
            "",
            "## Summary",
            "",
            f"- Total findings: {len(sorted_findings)}",
            f"- Critical: {sum(1 for item in sorted_findings if item.get('severity') == 'critical')}",
            f"- High: {sum(1 for item in sorted_findings if item.get('severity') == 'high')}",
            f"- Medium: {sum(1 for item in sorted_findings if item.get('severity') == 'medium')}",
            "",
            "## Findings",
            "",
        ]
    )

    if not sorted_findings:
        lines.append("No suspicious drift or persistence indicators were detected.")
    for index, finding in enumerate(sorted_findings, start=1):
        lines.extend(
            [
                f"### {index}. {finding.get('summary', 'Finding')}",
                "",
                f"- Severity: `{finding.get('severity', 'unknown')}`",
                f"- Type: `{finding.get('kind', 'unknown')}`",
                f"- Evidence: `{finding.get('evidence', {})}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"
