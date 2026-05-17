# Demo Walkthrough

GhostWire Sentinel ships with safe sample snapshots for a Linux kiosk-style device named `kiosk-01`.

## Scenario

The baseline snapshot represents a normal signage player:

- Chrome kiosk process
- Display agent service
- One approved backup cron job
- One approved SSH key
- One normal outbound HTTPS connection

The current snapshot adds suspicious drift:

- A new SSH key
- A new `reverse-tunnel.service`
- A cron job that downloads and executes a remote shell script
- A Python process with suspicious command-line behavior
- Repeated outbound connections to `198.51.100.77:4444`

## Run

```bash
python3 -m agent.cli analyze \
  --baseline data/baseline-snapshot.json \
  --current data/current-snapshot.json \
  --allowlist rules/allowlist.json \
  --findings reports/findings.json \
  --suppressed-findings reports/suppressed-findings.json \
  --report reports/incident-summary.md \
  --anomaly-report reports/anomaly-report.md \
  --timeline-report reports/timeline-report.md
```

Expected output:

```text
Wrote 9 findings to reports/findings.json
Suppressed 1 allow-listed finding(s)
Wrote report to reports/incident-summary.md
Wrote anomaly report to reports/anomaly-report.md
Wrote timeline report to reports/timeline-report.md
```

## What To Inspect

- `reports/incident-summary.md` for the full investigation queue
- `reports/anomaly-report.md` for a compact dashboard-style breakdown
- `reports/timeline-report.md` for investigation handoff
- `reports/findings.json` for machine-readable findings
- `reports/suppressed-findings.json` for allow-listed findings
