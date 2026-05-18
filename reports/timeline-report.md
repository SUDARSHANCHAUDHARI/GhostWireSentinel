# GhostWire Sentinel Timeline Report

Host: kiosk-01

## Timeline

1. Baseline captured: `2026-05-17T00:00:00+00:00`
2. Baseline approved: `2026-05-18T03:45:21.505119+00:00`
3. Current snapshot captured: `2026-05-17T00:15:00+00:00`
4. Active findings generated: `9`
5. Allow-listed findings suppressed: `1`

## Investigation Order

1. `critical` baseline.new_ssh_keys - New SSH key observed outside baseline.
2. `high` baseline.new_services - New service observed outside baseline.
3. `high` baseline.new_cron_jobs - New cron job observed outside baseline.
4. `high` persistence.cron - Cron job executes a command pattern commonly used for persistence or remote execution.
5. `high` persistence.service - Startup service name matches a suspicious persistence pattern.
6. `high` connection.suspicious - Outbound connection targets a suspicious remote marker or port.
7. `medium` baseline.new_connections - New outbound connection observed outside baseline.
8. `medium` persistence.process - Running process includes command-line behavior worth investigating.
9. `medium` connection.repeated_remote - Repeated outbound connections to the same remote may indicate beaconing.

## Suppressed

- `baseline.new_processes` - New process observed outside baseline.
