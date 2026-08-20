# GhostWire Sentinel

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](#requirements)
[![Status](https://img.shields.io/badge/status-MVP-green)](#status)
[![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#safe-use)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Endpoint threat hunting agent for Linux devices, kiosks, and edge systems. Detects stealth persistence, baseline drift, suspicious outbound behavior, and silent attacker tradecraft (unauthorized cron, modified binaries, hidden SSH keys, reverse proxies).

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Docker Demo](#docker-demo)
- [Safe Use](#safe-use)
- [Status](#status)
- [Roadmap](#roadmap)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [License](#license)
- [About](#about)

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

## Documentation

Full project documentation lives in [`docs/`](docs/):

- [Architecture](docs/ARCHITECTURE.md) — component design and data flow
- [Demo](docs/DEMO.md) — step-by-step demo walkthrough
- [Production Readiness](docs/PRODUCTION_READINESS.md) — gaps between MVP and production

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) and the [Code of Conduct](CODE_OF_CONDUCT.md) before opening a pull request. To report a security issue, see [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE). You are free to use, modify, and distribute this software with attribution.

---

## About

I'm Sudarshan Chaudhari, a Senior Quality Engineer, Test Automation specialist, and AI systems builder based in Bangkok, Thailand.

I have 13+ years of experience in software quality engineering, working across SaaS, fintech, gaming, web, mobile, cloud, and digital signage platforms. My background combines hands-on test automation with QA leadership, test strategy, CI/CD, release quality, production investigation, and cross-platform validation.

Alongside my professional QA career, I run [SudarshanTechLabs](https://sudarshantechlabs.com/), my independent engineering and product lab where I design, build, test, and ship software across Android, web, AI, cybersecurity, developer tooling, and cross-platform applications.

### What I work on

- ⚙️ **Quality Engineering & Test Automation** — Playwright, Selenium, Cypress, Appium, API testing, automation frameworks, end-to-end testing, CI/CD, release gates, GitHub Actions, risk-based testing, and production validation
- 🤖 **AI Systems & Automation** — AI agents, multi-agent orchestration, MCP servers, AI-assisted QA, prompt tooling, developer workflows, automation systems, and Claude Code plugins
- 📱 **Mobile & Cross-Platform Applications** — Android applications built with Kotlin and Jetpack Compose, Google Play releases, automated build and publishing pipelines, and cross-platform development spanning iOS, web, Windows, and macOS
- 🌐 **Web Applications & Platforms** — Full-stack applications using Next.js, TypeScript, Firebase, Cloudflare, REST APIs, and modern web infrastructure
- 🛠️ **Developer Tooling & CLI Engineering** — Rust, Python, TypeScript, CLI utilities, multi-repository tooling, build automation, release tooling, and engineering productivity systems
- 🛡️ **Cybersecurity & Observability** — Threat detection, log analysis, security auditing, vulnerability assessment, monitoring, and security-focused developer tools
- 📺 **Digital Signage & Device Platforms** — Content validation, playback testing, device compatibility, production investigation, monitoring, and QA across diverse hardware and operating-system environments

My work sits at the intersection of quality engineering, automation, AI, and software development. I approach products with a QA mindset from the beginning: understanding failure modes, designing for testability, automating repetitive work, and building release confidence into the engineering process.

Through SudarshanTechLabs, I also build products and tools from idea to production, covering architecture, development, testing, CI/CD, release automation, monitoring, and ongoing maintenance.

🌐 [sudarshantechlabs.com](https://sudarshantechlabs.com/) · 💼 [LinkedIn](https://linkedin.com/in/sudarshan-chaudhari) · 🐙 [GitHub](https://github.com/SUDARSHANCHAUDHARI) · ✉️ [sunny.sudarshan@gmail.com](mailto:sunny.sudarshan@gmail.com)
