# Security 🔒

## Overview
Security is enforced via optional API key authentication and safety gates on risky operations.

## Architecture
- REST auth uses `X-API-Key` if configured.
- Guard rails enforce confirm + cooldown on sensitive actions.
- Power actions require `NDEFENDER_ALLOW_UNSAFE=true`.

## API Examples
Protected request:
```bash
curl -s http://127.0.0.1:8000/api/v1/status \
  -H 'X-API-Key: <key>'
```

## Failure Modes
- `401` invalid API key
- `403` unsafe operations disabled
- `429` cooldown active

## Safety Notes
- Keep unsafe operations disabled in production.
- Use firewall or LAN isolation where possible.

## Troubleshooting
- Check `NDEFENDER_API_KEY` matches client header.
- Verify env vars in systemd unit.

## Configuration
- `NDEFENDER_API_KEY`
- `NDEFENDER_ALLOW_UNSAFE`

## Performance Notes
- API key check is constant time.

## Security Notes
- WebSocket does not enforce API key by default; use LAN or reverse proxy if needed.
