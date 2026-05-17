# Threat Model

GhostWire Sentinel focuses on quiet endpoint compromise patterns that can be missed by uptime or health monitoring.

## Protected Assets

- Linux kiosk and signage devices
- Edge systems with long-running unattended sessions
- SSH access paths and authorized keys
- Startup services and scheduled jobs
- Outbound network behavior
- Known-good operational baseline

## In-Scope Defensive Signals

- New SSH authorized keys
- New startup services
- New cron jobs
- Suspicious shell, curl, wget, netcat, Python, or base64 command patterns
- New outbound destinations
- Repeated outbound connections to the same remote
- Remote ports commonly used in lab reverse-shell or proxy patterns

## Out of Scope

- Exploit execution
- Malware payload generation
- Credential theft
- Offensive persistence installation
- Scanning systems without authorization

## Safety Position

Use only on devices, logs, snapshots, and lab environments you own or are authorized to monitor. The sample data uses synthetic evidence and documentation IP ranges.

## Expected Operator Workflow

1. Capture a known-good baseline after a trusted deployment.
2. Capture current snapshots on a schedule or during investigation.
3. Compare current state against the baseline.
4. Investigate high-priority drift first: SSH keys, startup services, cron jobs, suspicious outbound connections.
5. Preserve snapshots before remediation.
