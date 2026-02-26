# Audio 🔊

## Overview
Audio module provides volume and mute state plus guarded set endpoints via ALSA.

## Architecture
- Reads `amixer get Master` for percent and mute flags.

## API Examples
```bash
curl -s http://127.0.0.1:8000/api/v1/audio
```

Mute:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/audio/mute \
  -H 'content-type: application/json' \
  -d '{"payload":{"muted":true},"confirm":false}'
```

Volume:
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/audio/volume \
  -H 'content-type: application/json' \
  -d '{"payload":{"volume_percent":50},"confirm":false}'
```

## Failure Modes
- If `amixer` is missing, volume/mute may be null and commands return `409 invalid_state`.

## Safety Notes
- Audio commands are rate‑limited (10/min).

## Troubleshooting
- Verify ALSA: `amixer get Master`.

## Configuration
- No special configuration required.

## Performance Notes
- Polling interval defaults to 5 seconds.

## Security Notes
- Audio info is non‑sensitive; use API key based on network trust.
