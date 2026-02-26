# API 📘

## Overview
This document defines the production REST and WebSocket API for the N‑Defender System Controller. All endpoints are under `/api/v1` and return JSON. Timestamps are integer milliseconds.

## Architecture
- FastAPI routes read from the Supervisor snapshot.
- WebSocket pushes incremental updates from the Supervisor broadcaster.
- All payloads use a stable, normalized schema to avoid client breakage.

## API Examples
Base path: `/api/v1`

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

WebSocket (dev client):
```bash
python3 tools/dev_client.py ws --base-url http://127.0.0.1:8000
```

## REST Endpoints
- `GET /health`
- `GET /status`
- `GET /system`
- `GET /ups`
- `GET /services`
- `POST /services/{name}/restart`
- `GET /network`
- `GET /audio`
- `POST /system/reboot`
- `POST /system/shutdown`

## WebSocket
Endpoint:
- `WS /api/v1/ws`

Envelope:
```json
{
  "type": "SYSTEM_STATUS",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"cpu_temp_c": 45.2}
}
```

Allowed types:
- `SYSTEM_STATUS`
- `UPS_UPDATE`
- `SERVICE_UPDATE`
- `NETWORK_UPDATE`
- `AUDIO_UPDATE`
- `LOG_EVENT`
- `COMMAND_ACK`

## Failure Modes
- `400` `{"detail":"confirm_required"}`
- `403` `{"detail":"unsafe_disabled"}`
- `429` `{"detail":"rate_limited"}`
- `5xx` `{"detail":"internal_error"}`

## Safety Notes
- All risky operations require `{ "payload": {}, "confirm": true }`.
- Reboot/shutdown are disabled unless `NDEFENDER_ALLOW_UNSAFE=true`.

## Troubleshooting
- Verify service is running: `systemctl status ndefender-system-controller`.
- Check logs: `journalctl -u ndefender-system-controller -f`.
- Confirm API key matches configuration if 401 occurs.

## Configuration
- `NDEFENDER_API_KEY` (optional)
- `NDEFENDER_ALLOW_UNSAFE` (default: false)

## Performance Notes
- Status snapshot reads are constant time.
- Polling intervals are configurable (see `README.md`).

## Security Notes
- No auth required in current deployment.
- Sensitive operations are guarded with confirm + cooldown.
