"""Collect SSH authorized key information without exposing full keys."""

from __future__ import annotations

import hashlib
from pathlib import Path


def _fingerprint(key_line: str) -> str:
    return hashlib.sha256(key_line.encode("utf-8")).hexdigest()[:16]


def collect_ssh_keys(home_root: Path = Path("/home")) -> list[dict[str, str]]:
    """Return SSH key metadata."""
    candidates = [Path("/root/.ssh/authorized_keys")]
    if home_root.exists():
        candidates.extend(home_root.glob("*/.ssh/authorized_keys"))

    keys: list[dict[str, str]] = []
    for path in candidates:
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            key_type = stripped.split()[0] if stripped.split() else "unknown"
            keys.append(
                {
                    "source": str(path),
                    "line": str(index),
                    "type": key_type,
                    "fingerprint": _fingerprint(stripped),
                }
            )
    return keys
