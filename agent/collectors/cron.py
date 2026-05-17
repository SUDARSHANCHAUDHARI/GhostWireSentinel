"""Collect cron job information from common Linux cron locations."""

from __future__ import annotations

from pathlib import Path


CRON_PATHS = [
    Path("/etc/crontab"),
    Path("/etc/cron.d"),
    Path("/var/spool/cron"),
    Path("/var/spool/cron/crontabs"),
]


def _read_cron_file(path: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return entries

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        entries.append({"source": str(path), "line": str(index), "command": stripped})
    return entries


def collect_cron_jobs(paths: list[Path] | None = None) -> list[dict[str, str]]:
    """Return user and system cron entries."""
    entries: list[dict[str, str]] = []
    for cron_path in paths or CRON_PATHS:
        if cron_path.is_file():
            entries.extend(_read_cron_file(cron_path))
        elif cron_path.is_dir():
            for child in sorted(cron_path.iterdir()):
                if child.is_file():
                    entries.extend(_read_cron_file(child))
    return entries
