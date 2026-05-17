"""Build device baseline snapshots."""

from __future__ import annotations

from datetime import datetime, timezone
from platform import node, platform

from agent.collectors.connections import collect_connections
from agent.collectors.cron import collect_cron_jobs
from agent.collectors.processes import collect_processes
from agent.collectors.services import collect_services
from agent.collectors.ssh_keys import collect_ssh_keys


def build_snapshot() -> dict:
    """Return a current device state snapshot."""
    return {
        "metadata": {
            "hostname": node(),
            "platform": platform(),
            "captured_at": datetime.now(timezone.utc).isoformat(),
        },
        "processes": collect_processes(),
        "services": collect_services(),
        "cron_jobs": collect_cron_jobs(),
        "ssh_keys": collect_ssh_keys(),
        "connections": collect_connections(),
    }
