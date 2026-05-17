"""Collect startup service information from systemd when available."""

from __future__ import annotations

import subprocess


def collect_services() -> list[dict[str, str]]:
    """Return systemd and startup service metadata."""
    try:
        result = subprocess.run(
            ["systemctl", "list-unit-files", "--type=service", "--no-pager", "--no-legend"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return []

    services: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) < 2:
            continue
        services.append({"name": parts[0], "state": parts[1]})
    return services
