# GhostWire Sentinel

[![Python](https://img.shields.io/badge/Python-3.12-blue)](#) [![Status](https://img.shields.io/badge/status-MVP-green)](#) [![Security](https://img.shields.io/badge/security-defensive%20lab-purple)](#)

AI-assisted endpoint threat hunting platform for stealth persistence, baseline drift, and suspicious outbound behavior.

- **Portfolio group:** Flagship cybersecurity product project
- **Status:** MVP implemented, tested, committed, and pushed to GitHub
- **GitHub:** https://github.com/SUDARSHANCHAUDHARI/GhostWireSentinel
- **Local path:** `/Users/screencloudsudarshan/SUDARSHAN_CODE/sudarshan_repos/CyberSecurity/GhostWireSentinel`

## MVP Snapshot

This repository includes a working MVP with safe sample data, deterministic detection or analysis logic, local tests, and generated output reports where relevant. It is ready for README/demo polish or deeper product work.

## Safe Use

This project is defensive and analysis-focused. Use only with logs, systems, repositories, and lab environments you own or have permission to assess.

## Overview

GhostWire Sentinel is an AI-powered stealth persistence and anomaly detection platform.

This is an advanced cybersecurity startup-style idea focused on silent suspicious behavior, not just basic uptime or health monitoring.

## Core Concept

Most monitoring tools detect:

- crashes
- CPU spikes
- offline devices

GhostWire Sentinel focuses on:

> silent suspicious behavior

Examples:

- unusual persistence mechanisms
- hidden scheduled tasks
- suspicious startup scripts
- strange outbound connections
- modified system binaries
- stealthy background processes
- unauthorized cron jobs
- suspicious SSH keys
- hidden tunnels and reverse proxies

## Positioning

Lightweight AI-assisted threat hunting platform for Linux devices, kiosks, edge systems, and remote infrastructure.

This is aligned with:

- SOC monitoring
- threat hunting
- DFIR
- endpoint security
- Linux device monitoring
- kiosk and signage security

## MVP

Install an agent on a Linux device.

The agent collects:

- running processes
- startup services
- cron jobs
- SSH keys
- outbound connections
- system changes

Then the platform:

- compares device state against a baseline
- flags anomalies
- generates AI explanations
- builds an incident timeline

## Killer Features

### Persistence Detection

Detect:

- suspicious systemd services
- unknown cron jobs
- modified startup scripts
- hidden binaries

### Connection Intelligence

Flag:

- unusual outbound IPs
- TOR/proxy usage
- reverse shell patterns
- strange beaconing intervals

### Baseline Drift

Detect:

- new apps installed
- config changes
- permission changes
- new users and groups

### AI Threat Explanations

Instead of:

> Cron modified.

GhostWire Sentinel explains:

> A new scheduled task was added outside the normal deployment window and executes a remote shell script every 15 minutes.

## Suggested Stack

Backend:

- FastAPI
- PostgreSQL
- Redis
- Celery

Agent:

- Python or Go

Frontend:

- React
- Tailwind
- shadcn/ui

Detection:

- YARA
- Sigma-like rules
- anomaly scoring

AI:

- OpenAI
- Claude

Deployment:

- Docker
- Kubernetes later

## Why This Is Strong

GhostWire Sentinel combines cybersecurity, monitoring, AI, automation, Linux internals, threat hunting, and endpoint visibility.

It can evolve into:

- open-source security platform
- homelab tool
- SOC utility
- kiosk/signage security product
- lightweight EDR-style platform

## Status

Working CLI MVP.

## Quick Start

Run the demo analysis against the included safe sample snapshots:

```bash
python3 -m agent.cli analyze \
  --baseline data/baseline-snapshot.json \
  --current data/current-snapshot.json \
  --findings reports/findings.json \
  --report reports/incident-summary.md
```

Collect a local host snapshot:

```bash
python3 -m agent.cli collect --output data/current-snapshot.json
```

Run tests:

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```

## MVP Capabilities

- Collect running processes, cron jobs, SSH authorized key metadata, startup services, and outbound connections.
- Compare current device state against a baseline snapshot.
- Detect new services, cron jobs, SSH keys, processes, and outbound connections.
- Flag suspicious cron commands, startup services, process arguments, unusual outbound ports, and repeated remote connections.
- Generate JSON findings and a Markdown incident report.

## Roadmap

- Polish sample output screenshots or terminal demos
- Add architecture diagram and deeper implementation notes
- Expand test coverage around edge cases
- Add Docker or local demo workflow where useful
- Prepare `v0.1.0-mvp` release notes
