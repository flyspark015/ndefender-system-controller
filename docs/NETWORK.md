# Network 🌐

## Overview
Network module provides read‑only visibility into SSID and IP addresses.

## Architecture
- SSID via `iwgetid -r`
- IPs via host interface resolution

## API Examples
```bash
curl -s http://127.0.0.1:8000/api/v1/network
```

## Failure Modes
- If `iwgetid` is missing, SSID may be null.
- If no interfaces are active, IPs may be null.

## Safety Notes
- Read‑only; no network changes are made.

## Troubleshooting
- Check Wi‑Fi state: `nmcli dev wifi` or `iwgetid -r`.
- Verify IP: `ip addr`.

## Configuration
- No special configuration required.

## Performance Notes
- Polling interval defaults to 5 seconds.

## Security Notes
- Network info is sensitive; use API key on untrusted networks.
