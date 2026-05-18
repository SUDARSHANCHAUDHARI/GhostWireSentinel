# GhostWire Sentinel Anomaly Report

Host: kiosk-01
Current snapshot: 2026-05-17T00:15:00+00:00
Baseline snapshot: 2026-05-17T00:00:00+00:00
Baseline approved: 2026-05-18T03:45:21.505119+00:00
Suppressed findings: 1

## Detection Breakdown

- `baseline.new_ssh_keys`: 1
- `baseline.new_services`: 1
- `baseline.new_cron_jobs`: 1
- `persistence.cron`: 1
- `persistence.service`: 1
- `connection.suspicious`: 1
- `baseline.new_connections`: 1
- `persistence.process`: 1
- `connection.repeated_remote`: 1

## Triage Notes

- Prioritize SSH key drift, startup services, and suspicious remote execution first.
- Compare finding timestamps with deployment windows and approved change records.
- Preserve the current snapshot before removing evidence from the endpoint.
