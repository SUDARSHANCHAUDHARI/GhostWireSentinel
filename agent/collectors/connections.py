"""Collect outbound connection information using common host commands."""

from __future__ import annotations

import subprocess


def collect_connections() -> list[dict[str, str]]:
    """Return active network connection metadata."""
    commands = [
        ["ss", "-tunp"],
        ["netstat", "-tunp"],
    ]
    output = ""
    for command in commands:
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
            )
            output = result.stdout
            break
        except (OSError, subprocess.CalledProcessError):
            continue

    connections: list[dict[str, str]] = []
    for line in output.splitlines():
        if not line or line.lower().startswith(("state", "proto", "netid")):
            continue
        parts = line.split()
        if len(parts) < 5:
            continue
        connections.append(
            {
                "protocol": parts[0],
                "state": parts[1] if parts[0].lower() != "tcp" else parts[0],
                "local": parts[-3] if len(parts) >= 6 else "",
                "remote": parts[-2] if len(parts) >= 6 else parts[-1],
                "process": parts[-1] if len(parts) >= 6 else "",
            }
        )
    return connections
