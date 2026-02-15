# Services 🧰

## Overview
Systemd services are monitored and can be restarted via a guarded endpoint.

## Architecture
- Supervisor polls `systemctl show` for ActiveState/SubState/NRestarts.
- Restart uses `systemctl restart <name>`.

## API Examples
List services:
```bash
curl -s http://127.0.0.1:8000/api/v1/services
```

Restart service (guarded):
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/services/ndefender-backend/restart \
  -H 'content-type: application/json' \
  -d '{"confirm": true}'
```

## Failure Modes
- Missing service returns ok=false in COMMAND_ACK.
- Cooldown returns 429 for rapid repeats.

## Safety Notes
- Restart requires `{ "confirm": true }`.
- Cooldown is 10 seconds by default.

## Troubleshooting
- Verify service name with `systemctl list-units --type=service`.
- Check systemd logs for failures.

## Configuration
- Service allowlist is planned; currently none is enforced.

## Performance Notes
- Polling interval defaults to 5 seconds.

## Security Notes
- Guard rails protect restarts from accidental or repeated triggers.
