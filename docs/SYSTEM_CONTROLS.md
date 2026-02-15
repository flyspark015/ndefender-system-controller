# System Controls ⚡

## Overview
System controls include system stats and guarded power actions.

## Architecture
- System stats are polled by Supervisor and cached in memory.
- Power controls are handled by `PowerController` with safety gates.

## API Examples
Stats:
```bash
curl -s http://127.0.0.1:8000/api/v1/system
```

Reboot (guarded):
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/system/reboot \
  -H 'content-type: application/json' \
  -d '{"confirm": true}'
```

## Failure Modes
- Power actions return 403 if unsafe operations disabled.
- Cooldown returns 429 on repeated requests.

## Safety Notes
- Always require `{ "confirm": true }`.
- Keep `NDEFENDER_ALLOW_UNSAFE=false` unless required.

## Troubleshooting
- If stats are empty, check `psutil` installation.
- If throttling flags are missing, verify `vcgencmd` exists.

## Configuration
- `NDEFENDER_ALLOW_UNSAFE` controls power endpoints.
- Poll intervals via `NDEFENDER_SYSTEM_INTERVAL_S`.

## Performance Notes
- Stats polling uses lightweight `psutil` calls.

## Security Notes
- Power actions are protected by confirmation and cooldown.
