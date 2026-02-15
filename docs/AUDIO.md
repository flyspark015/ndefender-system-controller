# Audio 🔊

## Status
- `GET /api/v1/audio`

Fields:
- `volume_percent`
- `muted`

## Notes
- Uses `amixer` to read ALSA Master channel.
- Set/mute controls are planned for Step 7+ hardening.
