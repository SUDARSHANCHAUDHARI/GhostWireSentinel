FROM python:3.12-slim

WORKDIR /app
COPY . .

CMD ["python", "-m", "agent.cli", "analyze", "--baseline", "data/baseline-snapshot.json", "--current", "data/current-snapshot.json", "--findings", "reports/findings.json", "--report", "reports/incident-summary.md", "--anomaly-report", "reports/anomaly-report.md"]
