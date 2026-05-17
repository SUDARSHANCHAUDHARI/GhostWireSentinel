"""Compare device snapshots against baselines."""

from __future__ import annotations


def _keyed(items: list[dict], fields: tuple[str, ...]) -> set[tuple[str, ...]]:
    return {tuple(str(item.get(field, "")) for field in fields) for item in items}


def compare_snapshot(current: dict, baseline: dict) -> dict:
    """Return baseline drift results."""
    comparisons = {
        "new_processes": ("processes", ("command", "args")),
        "new_services": ("services", ("name",)),
        "new_cron_jobs": ("cron_jobs", ("source", "command")),
        "new_ssh_keys": ("ssh_keys", ("source", "fingerprint")),
        "new_connections": ("connections", ("remote", "process")),
    }

    drift: dict[str, list[dict]] = {}
    for output_name, (section, fields) in comparisons.items():
        baseline_keys = _keyed(baseline.get(section, []), fields)
        current_items = current.get(section, [])
        drift[output_name] = []
        seen: set[tuple[str, ...]] = set()
        for item in current_items:
            key = tuple(str(item.get(field, "")) for field in fields)
            if key in baseline_keys or key in seen:
                continue
            seen.add(key)
            drift[output_name].append(item)
    return drift
