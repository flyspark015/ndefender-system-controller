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
Example response:
```json
{
  "pack_voltage_v": 16.64,
  "current_a": -0.01,
  "input_vbus_v": 0.0,
  "input_power_w": 0.0,
  "soc_percent": 98,
  "state": "IDLE",
  "time_to_empty_s": 0,
  "time_to_full_s": 0,
  "status": "ok"
}
```
Units:
- Voltage in volts (`_v`)
- Current in amps (`_a`)
- Power in watts (`_w`)
- Percent in 0–100

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
- `WS /ws`

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
- `400` when confirmation payload is missing
- `401` invalid API key
- `403` unsafe operations disabled
- `429` cooldown active
- `5xx` when underlying system commands fail

## Safety Notes
- All risky operations require `{ "confirm": true }`.
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
- API key is optional for LAN usage.
- Sensitive operations are guarded with confirm + cooldown.
