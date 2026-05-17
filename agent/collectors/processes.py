"""Collect running process information using standard library tools."""

from __future__ import annotations

import subprocess


def collect_processes() -> list[dict[str, str]]:
    """Return running process metadata."""
    try:
        result = subprocess.run(
            ["ps", "-axo", "pid=,ppid=,user=,comm=,args="],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    processes: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.strip().split(None, 4)
        if len(parts) < 5:
            continue
        pid, ppid, user, command, args = parts
        processes.append(
            {
                "pid": pid,
                "ppid": ppid,
                "user": user,
                "command": command,
                "args": args,
            }
        )
    return processes
