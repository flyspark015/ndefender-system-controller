# Services 🧰

## Overview
The controller can read systemd service status and perform guarded restarts.

## API
- `GET /api/v1/services`
- `POST /api/v1/services/{name}/restart`
  - Body: `{ "confirm": true }`
  - Cooldown: 10s between restarts

## Status Fields
- `active_state`
- `sub_state`
- `restart_count`

## Notes
- Service list is config-driven in later steps.
- If a service cannot be queried, it is omitted from the response.
