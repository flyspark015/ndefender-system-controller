# Architecture 🧱

## Overview
The system controller is a FastAPI service that maintains a central in-memory state and publishes updates over REST and WebSocket. It is designed for Raspberry Pi 5 with UPS HAT (E) I2C telemetry.

## Core Components
- `Supervisor` orchestrates polling, state storage, and WS broadcasts.
- `SystemStatsCollector` gathers CPU/RAM/Disk/Temp/Uptime/Throttling.
- `UpsHatE` reads UPS registers and normalizes telemetry.
- `SystemdManager` queries service status and performs guarded restarts.
- `NetworkManager` reads SSID and IP addresses.
- `AudioManager` reads volume and mute state via ALSA.
- `PowerController` performs guarded reboot/shutdown when enabled.

## Data Flow
1. Supervisor runs polling loops on configurable intervals.
2. Each poll updates the in-memory snapshot.
3. WS broadcasts publish deltas using the standard envelope.
4. REST endpoints read the latest snapshot.

## Fault Handling
- Poller exceptions are caught and logged; the service continues.
- UPS and system stats return empty/partial models if read fails.
- Risky operations are blocked by default unless explicitly enabled.

## State Consistency
- Supervisor uses an async lock for snapshot updates.
- REST reads return consistent snapshot copies.

## Security and Safety
- Optional API key via `X-API-Key`.
- Risky endpoints require `{ "confirm": true }`.
- Cooldown rate limits block rapid repeats.
- Power actions require `NDEFENDER_ALLOW_UNSAFE=true`.
