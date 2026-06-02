# GhostWire Sentinel

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#requirements)
[![Status](https://img.shields.io/badge/status-MVP-green)](#status)
[![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#safe-use)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Endpoint threat hunting agent for Linux devices, kiosks, and edge systems. Detects stealth persistence, baseline drift, suspicious outbound behavior, and silent attacker tradecraft (unauthorized cron, modified binaries, hidden SSH keys, reverse proxies).

---

## Overview

GhostWire Sentinel is a defensive analysis agent that captures a security-relevant snapshot of a Linux host — processes, services, cron jobs, SSH keys, outbound connections — then compares it to an approved baseline to detect drift. It also runs anomaly, beaconing, and persistence detectors on the live snapshot for immediate alerts.

Target environments: Linux kiosks, signage players, IoT/edge devices, and unattended servers where stealth persistence and silent backdoors are the primary threat.

## Features

- Collects processes, services, cron jobs, SSH keys, and outbound connections
- Snapshot baseline with approval workflow and history
- Compares live snapshot against approved baseline (drift detection)
- Anomaly detector for unexpected processes and services
- Beaconing detector for periodic outbound callbacks
- Persistence detector (cron, startup, modified binaries, suspicious SSH keys)
- Allowlist for trusted processes and services
- Markdown report, timeline report, anomaly report, and dashboard summary JSON

## Requirements

- Python 3.10 or newer
- Linux (full feature support); macOS / Windows (partial)
- No third-party Python packages (standard library only)
- Optional: Docker for the demo container

## Installation

```bash
git clone https://github.com/SUDARSHANCHAUDHARI/GhostWireSentinel.git
cd GhostWireSentinel
pip install .
```

This registers the `ghost-wire` CLI command.

To run without installing:

```bash
python3 main.py --help
```

## Usage

Capture and analyze a snapshot using the included sample data:

```bash
python3 main.py --out-dir reports
```

Generated outputs in `reports/`:

- `snapshot.json` — collected telemetry
- `baseline-diff.json` — drift findings vs approved baseline
- `anomalies.json` — detected anomalies
- `beaconing.json` — periodic outbound callback findings
- `persistence.json` — persistence mechanism findings
- `report.md` — Markdown threat hunting report
- `timeline.md` — chronological timeline of findings
- `triage.md` — analyst triage checklist

## Project Structure

```
GhostWireSentinel/
├── agent/
│   ├── collectors/   Processes, services, cron, SSH keys, connections, USB
│   ├── detectors/    Anomaly, beaconing, persistence
│   ├── baseline/     Snapshot, compare, approve workflow
│   ├── allowlist.py  Trusted-entity allowlist
│   ├── main.py       Agent entry
│   └── report.py     Markdown report builders
├── apps/             FastAPI/React dashboard scaffold (planned)
├── data/             Safe sample snapshots and baselines
├── rules/            Detection rule definitions
├── docs/             Architecture, security notes, demo
├── tests/            Unit tests
├── main.py           CLI entrypoint
├── pyproject.toml    Package metadata
└── LICENSE
```

## Testing

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## Docker Demo

```bash
docker compose run --rm ghost-wire-demo
```

## Safe Use

This project is defensive and analysis-focused. Run only on devices and lab environments you own or have explicit written permission to monitor. The sample data is synthetic and safe for public demo use.

## Status

Working CLI agent MVP with collectors, detectors, baseline workflow, tests, and Docker support. Web dashboard scaffold present but not yet implemented.

## Roadmap

- Live collection on real Linux hosts (read `/proc`, `/etc`, `ss`, `crontab`)
- Encrypted snapshot upload to a central collector
- Signed baseline approvals
- Web dashboard for fleet drift visualization
- GitHub release `v0.1.0-mvp`

## License

Released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software with attribution.

## Author

**Sudarshan Chaudhari** — [SudarshanTechLabs](https://github.com/SUDARSHANCHAUDHARI)
Bangkok, Thailand

For inquiries: open an issue on [GitHub](https://github.com/SUDARSHANCHAUDHARI/GhostWireSentinel/issues).
