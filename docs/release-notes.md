# Release Notes

## v0.1.0-mvp

Initial portfolio MVP for GhostWire Sentinel.

## Added

- Python CLI for collecting local Linux snapshots
- Baseline comparison for process, service, cron, SSH key, and connection drift
- Persistence detectors for suspicious cron, service, and process behavior
- Suspicious outbound connection and repeated remote detection
- Safe synthetic sample snapshots
- JSON findings output
- Markdown incident report
- Markdown anomaly report
- Markdown timeline report
- Operator allow-list for approved findings
- Unit tests and GitHub Actions CI
- Docker Compose demo path

## Safety

- No exploit code
- No payload generation
- SSH collector stores key metadata and short fingerprints, not full key material
- Sample data uses synthetic evidence and documentation IP ranges
