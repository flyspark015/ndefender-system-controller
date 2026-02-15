# Services 🧰

## Overview
The controller reads systemd status and exposes a guarded restart endpoint.

## Status Fields
- `active_state`
- `sub_state`
- `restart_count`

## Endpoints
- `GET /api/v1/services`
- `POST /api/v1/services/{name}/restart`

Restart requirements:
- Body: `{ "confirm": true }`
- Cooldown: 10 seconds

## Notes
- If a service cannot be queried, it is omitted.
- Restart commands return a COMMAND_ACK envelope.
