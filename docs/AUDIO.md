# Audio 🔊

## Overview
Audio module provides read‑only volume and mute state via ALSA.

## Architecture
- Reads `amixer get Master` for percent and mute flags.

## API Examples
```bash
curl -s http://127.0.0.1:8000/api/v1/audio
```

## Failure Modes
- If `amixer` is missing, volume/mute may be null.

## Safety Notes
- Read‑only; no volume changes are applied.

## Troubleshooting
- Verify ALSA: `amixer get Master`.

## Configuration
- No special configuration required.

## Performance Notes
- Polling interval defaults to 5 seconds.

## Security Notes
- Audio info is non‑sensitive; use API key based on network trust.
