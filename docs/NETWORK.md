# Network 🌐

## Overview
Network module provides Wi‑Fi and Bluetooth state plus guarded control endpoints.

## Architecture
- Wi‑Fi via `nmcli`
- Bluetooth via `bluetoothctl`
- Snapshot includes Wi‑Fi and Bluetooth state plus last errors when degraded.

## API Examples
```bash
curl -s http://127.0.0.1:8000/api/v1/network
```

Wi‑Fi state:
```bash
curl -s http://127.0.0.1:8000/api/v1/network/wifi/state
```

Wi‑Fi scan:
```bash
curl -s http://127.0.0.1:8000/api/v1/network/wifi/scan
```

Bluetooth state:
```bash
curl -s http://127.0.0.1:8000/api/v1/network/bluetooth/state
```

Bluetooth devices:
```bash
curl -s http://127.0.0.1:8000/api/v1/network/bluetooth/devices
```

Wi‑Fi enable/disable:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/network/wifi/enable \
  -H 'content-type: application/json' \
  -d '{"payload":{"enabled":true},"confirm":false}'
```

Wi‑Fi connect:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/network/wifi/connect \
  -H 'content-type: application/json' \
  -d '{"payload":{"ssid":"MySSID","password":"secret","hidden":false},"confirm":false}'
```

Wi‑Fi disconnect:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/network/wifi/disconnect \
  -H 'content-type: application/json' \
  -d '{"payload":{},"confirm":false}'
```

Bluetooth enable:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/network/bluetooth/enable \
  -H 'content-type: application/json' \
  -d '{"payload":{"enabled":true},"confirm":false}'
```

Bluetooth scan start:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/network/bluetooth/scan/start \
  -H 'content-type: application/json' \
  -d '{"payload":{},"confirm":false}'
```

Bluetooth pair:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/network/bluetooth/pair \
  -H 'content-type: application/json' \
  -d '{"payload":{"addr":"AA:BB:CC:DD:EE:FF"},"confirm":false}'
```

## Failure Modes
- `nmcli_not_found` indicates NetworkManager tools missing.
- `bluetoothctl_not_found` indicates Bluetooth CLI missing.
- Commands return `409` with `{"detail":"invalid_state"}` when the OS call fails.

## Safety Notes
- Network commands are rate‑limited (10/min).
- For production deployments, keep unsafe controls disabled at the network edge.

## Troubleshooting
- Check Wi‑Fi state: `nmcli dev wifi` or `iwgetid -r`.
- Verify IP: `ip addr`.

## Configuration
- No special configuration required.

## Performance Notes
- Polling interval defaults to 5 seconds.

## Security Notes
- Network info is sensitive; use API key on untrusted networks.
