# Audio 🔊

## Status
- `GET /api/v1/audio`

Fields:
- `volume_percent`
- `muted`

## Implementation Notes
- Reads ALSA Master via `amixer`.
- Read-only for now; set/mute controls are planned.
