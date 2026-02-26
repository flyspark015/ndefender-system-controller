# Usage 📗

## Overview
This guide shows common usage patterns for REST and WebSocket clients.

## Architecture
- REST for snapshots
- WS for incremental updates

## API Examples
Health:
```bash
curl -s http://127.0.0.1:8000/api/v1/health
```

Status:
```bash
curl -s http://127.0.0.1:8000/api/v1/status
```

UPS:
```bash
curl -s http://127.0.0.1:8000/api/v1/ups
```

Services:
```bash
curl -s http://127.0.0.1:8000/api/v1/services
```

Restart (guarded):
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/services/ndefender-backend/restart \
  -H 'content-type: application/json' \
  -d '{"payload":{},"confirm":true}'
```

WebSocket:
```bash
python3 tools/dev_client.py ws --base-url http://127.0.0.1:8000
```

## Failure Modes
- 400 indicates confirm required.
- 403 indicates unsafe operations disabled.
- 429 indicates rate limited.

## Safety Notes
- Always send `{ "payload": {}, "confirm": true }` for risky endpoints.
- Power actions are disabled unless explicitly enabled.

## Troubleshooting
- Check service status: `systemctl status ndefender-system-controller`.
- Tail logs: `journalctl -u ndefender-system-controller -f`.

## Configuration
- `NDEFENDER_ALLOW_UNSAFE=true` to enable reboot/shutdown.

## Performance Notes
- For high‑frequency clients, use WS updates instead of polling.

## Security Notes
- Keep unsafe operations disabled in production.
