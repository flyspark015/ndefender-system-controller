# System Controls ⚡

## System Stats ✅
The system stats endpoint is live:
- `GET /api/v1/system`

Fields include CPU temp, uptime, load averages, RAM/disk usage, and throttling flags when available.

## Power Controls 🔒
Guarded power endpoints:
- `POST /api/v1/system/reboot`
- `POST /api/v1/system/shutdown`

Requirements:
- Body: `{ "confirm": true }`
- Cooldown: 30s
- Unsafe actions are blocked unless `NDEFENDER_ALLOW_UNSAFE=true`

Responses use COMMAND_ACK-like envelopes.
