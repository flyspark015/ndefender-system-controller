# Network 🌐

## Status
- `GET /api/v1/network`

Fields:
- `connected`
- `ssid`
- `ip_v4`
- `ip_v6`

## Notes
- Wi-Fi connect/disconnect hooks are deferred until Step 6+ hardening.
- This endpoint is read-only for now.
