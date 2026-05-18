"""Baseline approval and history helpers."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def snapshot_hash(snapshot: dict) -> str:
    """Return a stable hash for a snapshot payload."""
    payload = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def approval_record(snapshot: dict, approved_by: str, reason: str) -> dict:
    """Build a baseline approval record."""
    metadata = snapshot.get("metadata", {})
    return {
        "approved_at": datetime.now(timezone.utc).isoformat(),
        "approved_by": approved_by,
        "reason": reason,
        "snapshot_hash": snapshot_hash(snapshot),
        "hostname": metadata.get("hostname", "unknown"),
        "captured_at": metadata.get("captured_at", "unknown"),
    }


def approve_snapshot(snapshot: dict, approved_by: str, reason: str) -> tuple[dict, dict]:
    """Return a snapshot copy with approval metadata plus its ledger record."""
    record = approval_record(snapshot, approved_by, reason)
    approved = dict(snapshot)
    metadata = dict(snapshot.get("metadata", {}))
    metadata["baseline_approval"] = record
    approved["metadata"] = metadata
    return approved, record


def load_history(path: Path) -> list[dict]:
    """Load baseline approval history."""
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def append_history(path: Path, record: dict) -> list[dict]:
    """Append or replace a baseline approval record in history."""
    history = load_history(path)
    history = [item for item in history if item.get("snapshot_hash") != record.get("snapshot_hash")]
    history.append(record)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(history, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return history
