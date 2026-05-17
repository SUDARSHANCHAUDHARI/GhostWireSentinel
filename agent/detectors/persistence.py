"""Detect suspicious persistence mechanisms."""

from __future__ import annotations


SUSPICIOUS_TERMS = (
    "curl ",
    "wget ",
    "bash -c",
    "nc ",
    "netcat",
    "/tmp/",
    "python -c",
    "base64",
    "nohup",
)


def _finding(kind: str, severity: str, summary: str, evidence: dict) -> dict:
    return {
        "kind": kind,
        "severity": severity,
        "summary": summary,
        "evidence": evidence,
    }


def detect_persistence(snapshot: dict) -> list[dict]:
    """Return suspicious persistence findings."""
    findings: list[dict] = []

    for job in snapshot.get("cron_jobs", []):
        command = str(job.get("command", "")).lower()
        if any(term in command for term in SUSPICIOUS_TERMS):
            findings.append(
                _finding(
                    "persistence.cron",
                    "high",
                    "Cron job executes a command pattern commonly used for persistence or remote execution.",
                    job,
                )
            )

    for service in snapshot.get("services", []):
        name = str(service.get("name", "")).lower()
        if any(marker in name for marker in ("reverse", "tunnel", "miner", "payload", "backdoor")):
            findings.append(
                _finding(
                    "persistence.service",
                    "high",
                    "Startup service name matches a suspicious persistence pattern.",
                    service,
                )
            )

    for process in snapshot.get("processes", []):
        args = str(process.get("args", "")).lower()
        if any(term in args for term in SUSPICIOUS_TERMS):
            findings.append(
                _finding(
                    "persistence.process",
                    "medium",
                    "Running process includes command-line behavior worth investigating.",
                    process,
                )
            )

    return findings
