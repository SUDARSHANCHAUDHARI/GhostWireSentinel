"""Build human-readable GhostWire Sentinel reports."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone


SEVERITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}
NEXT_STEPS = {
    "baseline.new_ssh_keys": "Validate the key owner, rotate affected credentials, and remove unauthorized keys.",
    "baseline.new_services": "Inspect the unit file, check enablement history, and disable unknown startup services.",
    "baseline.new_cron_jobs": "Review the cron source, confirm change ownership, and remove unapproved scheduled execution.",
    "baseline.new_connections": "Validate the remote destination and block suspicious egress while investigating.",
    "baseline.new_processes": "Inspect process ancestry, binary path, environment, and persistence relationship.",
    "persistence.cron": "Treat remote script execution in cron as high priority until proven authorized.",
    "persistence.service": "Check service file contents, install time, and whether it launches a tunnel or payload.",
    "persistence.process": "Capture process details and compare against deployment history.",
    "connection.suspicious": "Isolate the host if this remote is unexpected and preserve connection evidence.",
    "connection.repeated_remote": "Check for periodic callbacks, tunnel processes, and firewall logs for recurrence.",
}


def sort_findings(findings: list[dict]) -> list[dict]:
    """Return findings sorted by severity."""
    return sorted(
        findings,
        key=lambda finding: SEVERITY_ORDER.get(str(finding.get("severity", "")).lower(), 0),
        reverse=True,
    )


def severity_counts(findings: list[dict]) -> Counter:
    """Return finding counts grouped by severity."""
    return Counter(str(item.get("severity", "unknown")) for item in findings)


def top_priorities(findings: list[dict], limit: int = 3) -> list[dict]:
    """Return the highest priority findings to investigate first."""
    return sort_findings(findings)[:limit]


def _format_evidence(evidence: dict) -> str:
    return ", ".join(f"{key}={value}" for key, value in evidence.items()) or "no evidence"


def build_markdown_report(
    findings: list[dict],
    current: dict,
    baseline: dict | None = None,
    suppressed: list[dict] | None = None,
) -> str:
    """Return a Markdown incident report."""
    sorted_findings = sort_findings(findings)
    counts = severity_counts(sorted_findings)
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
            f"- Suppressed allow-listed findings: {len(suppressed or [])}",
            f"- Critical: {counts.get('critical', 0)}",
            f"- High: {counts.get('high', 0)}",
            f"- Medium: {counts.get('medium', 0)}",
            f"- Low: {counts.get('low', 0)}",
            "",
            "## Priority Queue",
            "",
        ]
    )

    if not sorted_findings:
        lines.append("No immediate investigation queue was generated.")
    for index, finding in enumerate(top_priorities(sorted_findings), start=1):
        kind = finding.get("kind", "unknown")
        lines.append(f"{index}. **{finding.get('severity', 'unknown')}** - {finding.get('summary', 'Finding')} ({kind})")

    lines.extend(["", "## Findings", ""])
    if not sorted_findings:
        lines.append("No suspicious drift or persistence indicators were detected.")
    for index, finding in enumerate(sorted_findings, start=1):
        kind = str(finding.get("kind", "unknown"))
        lines.extend(
            [
                f"### {index}. {finding.get('summary', 'Finding')}",
                "",
                f"- Severity: `{finding.get('severity', 'unknown')}`",
                f"- Type: `{kind}`",
                f"- Evidence: `{_format_evidence(finding.get('evidence', {}))}`",
                f"- Recommended next step: {NEXT_STEPS.get(kind, 'Review the finding and validate against expected device behavior.')}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def build_anomaly_report(
    findings: list[dict],
    current: dict,
    baseline: dict | None = None,
    suppressed: list[dict] | None = None,
) -> str:
    """Return a compact anomaly-focused report for dashboards or triage."""
    sorted_findings = sort_findings(findings)
    metadata = current.get("metadata", {})
    baseline_metadata = (baseline or {}).get("metadata", {})
    by_kind = Counter(str(finding.get("kind", "unknown")) for finding in sorted_findings)
    lines = [
        "# GhostWire Sentinel Anomaly Report",
        "",
        f"Host: {metadata.get('hostname', 'unknown')}",
        f"Current snapshot: {metadata.get('captured_at', 'unknown')}",
        f"Baseline snapshot: {baseline_metadata.get('captured_at', 'unknown')}",
        f"Suppressed findings: {len(suppressed or [])}",
        "",
        "## Detection Breakdown",
        "",
    ]
    for kind, count in by_kind.most_common():
        lines.append(f"- `{kind}`: {count}")
    lines.extend(["", "## Triage Notes", ""])
    if not sorted_findings:
        lines.append("- No anomalous persistence, baseline drift, or suspicious outbound behavior was found.")
    else:
        lines.extend(
            [
                "- Prioritize SSH key drift, startup services, and suspicious remote execution first.",
                "- Compare finding timestamps with deployment windows and approved change records.",
                "- Preserve the current snapshot before removing evidence from the endpoint.",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def build_timeline_report(
    findings: list[dict],
    current: dict,
    baseline: dict | None = None,
    suppressed: list[dict] | None = None,
) -> str:
    """Return an investigation timeline report."""
    metadata = current.get("metadata", {})
    baseline_metadata = (baseline or {}).get("metadata", {})
    lines = [
        "# GhostWire Sentinel Timeline Report",
        "",
        f"Host: {metadata.get('hostname', 'unknown')}",
        "",
        "## Timeline",
        "",
        f"1. Baseline captured: `{baseline_metadata.get('captured_at', 'unknown')}`",
        f"2. Current snapshot captured: `{metadata.get('captured_at', 'unknown')}`",
        f"3. Active findings generated: `{len(findings)}`",
        f"4. Allow-listed findings suppressed: `{len(suppressed or [])}`",
        "",
        "## Investigation Order",
        "",
    ]
    if not findings:
        lines.append("- No active findings require investigation.")
    for index, finding in enumerate(top_priorities(findings, limit=10), start=1):
        lines.append(
            f"{index}. `{finding.get('severity', 'unknown')}` {finding.get('kind', 'unknown')} - {finding.get('summary', 'Finding')}"
        )
    if suppressed:
        lines.extend(["", "## Suppressed", ""])
        for item in suppressed:
            lines.append(f"- `{item.get('kind', 'unknown')}` - {item.get('summary', 'Finding')}")
    return "\n".join(lines).rstrip() + "\n"
