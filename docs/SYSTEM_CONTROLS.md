# System Controls ⚡

## System Stats ✅
Endpoint:
- `GET /api/v1/system`

Fields include CPU temp, uptime, load averages, RAM/disk usage, and throttling flags when available.

## Power Controls 🔒
Endpoints:
- `POST /api/v1/system/reboot`
- `POST /api/v1/system/shutdown`

Requirements:
- Body: `{ "confirm": true }`
- Cooldown: 30 seconds
- Unsafe actions are blocked unless `NDEFENDER_ALLOW_UNSAFE=true`

Responses use COMMAND_ACK-like envelopes.
