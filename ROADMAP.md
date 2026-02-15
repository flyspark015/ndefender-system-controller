# ROADMAP 🧭

## Scope ✅
N-Defender System Controller API is a production-grade control plane for Raspberry Pi 5. It provides UPS telemetry, system health, service supervision, network/audio control, and safe power actions behind a single API surface.

## Phased Plan 📌
- Step 0: Roadmap + APIs/models + GREEN checklist
- Step 1: Skeleton app + CI + minimal endpoints
- Step 2: Supervisor state store + scheduler + WS fan-out
- Step 3: System stats module + /api/v1/system
- Step 4: UPS HAT (E) module + keepalive + /api/v1/ups
- Step 5: Systemd service manager + restart guard + /api/v1/services
- Step 6: Network manager + /api/v1/network
- Step 7: Audio manager + /api/v1/audio
- Step 8: Power controls (guarded reboot/shutdown)
- Step 9: Docs hardening + deployment + dev tools
- Step 10: Release lock + v1.0.0 tag

## API Surface (v1) 🌐
Base path: `/api/v1`

REST:
- `GET /health` → liveness/ready status
- `GET /status` → combined snapshot
- `GET /ups` → UPS telemetry
- `GET /system` → system stats
- `GET /services` → systemd services list + status
- `POST /services/{name}/restart` → guarded restart
- `GET /network` → Wi‑Fi/IP status + link
- `POST /network/connect` → optional guarded connect
- `POST /network/disconnect` → optional guarded disconnect
- `GET /audio` → volume/mute
- `POST /audio/volume` → guarded set
- `POST /audio/mute` → guarded set
- `POST /system/reboot` → guarded
- `POST /system/shutdown` → guarded

WebSocket:
- `WS /ws` → push updates

WS envelope (all messages):
```
{
  "type": "...",
  "timestamp_ms": 0,
  "source": "system",
  "data": {}
}
```
Allowed WS types:
- `SYSTEM_STATUS`
- `UPS_UPDATE`
- `SERVICE_UPDATE`
- `NETWORK_UPDATE`
- `AUDIO_UPDATE`
- `LOG_EVENT`
- `COMMAND_ACK`

## Data Models (Normalized) 🧩
Common:
- `timestamp_ms` (int)
- `source` ("system")

`HealthResponse`:
- `ok` (bool)
- `timestamp_ms` (int)
- `version` (str)

`StatusSnapshot`:
- `timestamp_ms` (int)
- `system` (SystemStats)
- `ups` (UpsStatus)
- `services` (list[ServiceStatus])
- `network` (NetworkStatus)
- `audio` (AudioStatus)

`SystemStats`:
- `uptime_s` (int)
- `cpu_temp_c` (float)
- `cpu_usage_percent` (float)
- `load_1m` (float)
- `load_5m` (float)
- `load_15m` (float)
- `ram_used_mb` (int)
- `ram_total_mb` (int)
- `disk_used_gb` (int)
- `disk_total_gb` (int)

`UpsStatus`:
- `pack_voltage_v` (float)
- `current_a` (float)  # +charge / -discharge
- `input_vbus_v` (float)
- `input_power_w` (float)
- `soc_percent` (int)
- `time_to_empty_s` (int | null)
- `time_to_full_s` (int | null)
- `per_cell_v` (list[float])  # len 4
- `state` ("IDLE"|"CHARGING"|"FAST_CHARGING"|"DISCHARGING"|"UNKNOWN")

`ServiceStatus`:
- `name` (str)
- `active_state` (str)
- `sub_state` (str)
- `restart_count` (int)

`NetworkStatus`:
- `connected` (bool)
- `ssid` (str | null)
- `ip_v4` (str | null)
- `ip_v6` (str | null)

`AudioStatus`:
- `volume_percent` (int)
- `muted` (bool)

## Update Cadence (Initial) ⏱️
- System stats: every 2s
- UPS telemetry: every 2s
- Services: every 5s
- Network: every 5s
- Audio: every 5s
- WS broadcast: on change + periodic heartbeat every 10s

## Auth & Safety Guards 🔒
- Optional API key via `X-API-Key`
- Risky endpoints require:
  - `{"confirm": true}`
  - cooldown rate-limit
  - COMMAND_ACK-style response

## GREEN Verification Checklist ✅
- App boots with `uvicorn` without errors
- `GET /api/v1/health` returns `ok: true`
- `GET /api/v1/status` returns a valid schema
- WS endpoint accepts a client and sends HELLO/STATUS
- Lint passes (ruff)
- Tests pass (pytest)
- Docs exist for all modules and deployment
- systemd unit sample works on Pi
- All guarded endpoints enforce `confirm` + rate limit
