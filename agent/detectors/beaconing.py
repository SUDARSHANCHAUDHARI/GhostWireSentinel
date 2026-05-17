"""Detect beaconing-like outbound traffic."""

from __future__ import annotations


SUSPICIOUS_PORTS = {"4444", "5555", "6666", "8081", "9001", "9050", "1337"}
SUSPICIOUS_REMOTE_MARKERS = ("tor", "proxy", "onion")


def _remote_port(remote: str) -> str:
    if ":" not in remote:
        return ""
    return remote.rsplit(":", 1)[-1]


def detect_beaconing(connections: list[dict]) -> list[dict]:
    """Return suspicious periodic connection findings."""
    findings: list[dict] = []
    seen_remotes: dict[str, int] = {}
    flagged_remotes: set[str] = set()
    for connection in connections:
        remote = str(connection.get("remote", "")).lower()
        port = _remote_port(remote)
        seen_remotes[remote] = seen_remotes.get(remote, 0) + 1
        if (
            remote not in flagged_remotes
            and (port in SUSPICIOUS_PORTS or any(marker in remote for marker in SUSPICIOUS_REMOTE_MARKERS))
        ):
            flagged_remotes.add(remote)
            findings.append(
                {
                    "kind": "connection.suspicious",
                    "severity": "high",
                    "summary": "Outbound connection targets a suspicious remote marker or port.",
                    "evidence": connection,
                }
            )

    for remote, count in seen_remotes.items():
        if remote and count >= 3:
            findings.append(
                {
                    "kind": "connection.repeated_remote",
                    "severity": "medium",
                    "summary": "Repeated outbound connections to the same remote may indicate beaconing.",
                    "evidence": {"remote": remote, "count": count},
                }
            )
    return findings
