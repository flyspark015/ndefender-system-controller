# Architecture 🧱

## Overview
The system controller is a FastAPI service with background pollers feeding a central in‑memory snapshot. REST endpoints read from this snapshot; WebSocket broadcasts publish incremental updates.

## Architecture
```
+-----------------------------+
|         FastAPI App         |
|  REST + WebSocket /api/v1   |
+--------------+--------------+
               |
               v
+-----------------------------+
|         Supervisor          |
|  Pollers + State Snapshot   |
+----+----+----+----+----+-----+
     |    |    |    |    |
     v    v    v    v    v
  System  UPS Services Network Audio
  Stats   HAT  systemd   WiFi   ALSA
```

## API Examples
- REST reads: `/api/v1/status`
- WS: `/api/v1/ws`

## Failure Modes
- Individual poller failures do not stop the process.
- WS sends best‑effort updates; failed clients are disconnected.

## Safety Notes
- Risky operations are protected by confirm + cooldown + unsafe gate.

## Troubleshooting
- Confirm pollers are running by watching WS updates.
- Logs show poller errors with module context.

## Configuration
- Poll intervals: `NDEFENDER_*_INTERVAL_S`
- UPS settings: `NDEFENDER_UPS_I2C_*`

## Performance Notes
- Snapshot updates are protected by an async lock.
- WS fan‑out uses per‑socket send locks to avoid interleaving.

## Security Notes
- Optional API key is enforced at REST endpoints.
- WS currently does not enforce API key and is intended for LAN use.
