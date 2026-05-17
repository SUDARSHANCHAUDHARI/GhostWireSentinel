# Deployment

The MVP has two useful deployment modes: local Python and Docker demo. Both are analysis-only and safe for portfolio demonstration.

## Local Python Demo

```bash
python3 -m agent.cli analyze \
  --baseline data/baseline-snapshot.json \
  --current data/current-snapshot.json \
  --findings reports/findings.json \
  --report reports/incident-summary.md \
  --anomaly-report reports/anomaly-report.md
```

## Local Collection

```bash
python3 -m agent.cli collect --output data/current-snapshot.json
```

Run collection only on devices you own or are authorized to monitor.

## Docker Demo

```bash
docker compose run --rm ghostwire-demo
```

This runs the included synthetic baseline/current snapshots and writes reports to `reports/`.

## Future Deployment Direction

- Agent service on Linux devices
- FastAPI ingestion service
- PostgreSQL event and baseline storage
- Redis/Celery for async scoring
- React dashboard for investigation queues
- Optional Kubernetes after the local Docker path is stable
