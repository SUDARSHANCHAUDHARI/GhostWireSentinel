FROM python:3.12-slim

WORKDIR /app
COPY . .

CMD ["python", "-m", "agent.cli", "analyze", "--baseline", "data/baseline-snapshot.json", "--current", "data/current-snapshot.json", "--allowlist", "rules/allowlist.json", "--findings", "reports/findings.json", "--suppressed-findings", "reports/suppressed-findings.json", "--report", "reports/incident-summary.md", "--anomaly-report", "reports/anomaly-report.md", "--timeline-report", "reports/timeline-report.md"]
