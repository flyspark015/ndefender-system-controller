# Network 🌐

## Status
- `GET /api/v1/network`

Fields:
- `connected`
- `ssid`
- `ip_v4`
- `ip_v6`

## Implementation Notes
- SSID is read via `iwgetid -r`.
- IPs are resolved from host interfaces.
- Endpoint is read-only.
