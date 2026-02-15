# 🚀 N-Defender System Controller API

## 📌 Overview
N-Defender System Controller is a production-grade control plane for Raspberry Pi 5. It exposes a single API surface for UPS telemetry, system health, systemd supervision, network/audio visibility, and guarded power controls. The service is API-first, WS-capable, and safe-by-default for field deployment.

## 🧠 Architecture Summary
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

## 🔋 UPS HAT (E) Integration
- I2C bus: `/dev/i2c-1` @ `0x2d`
- Keepalive: write `0x55` to register `0x01`
- Telemetry normalized to a stable API model:
  - `pack_voltage_v`, `current_a`, `input_vbus_v`, `input_power_w`
  - `soc_percent`, `time_to_empty_s`, `time_to_full_s`
  - `per_cell_v[4]`, `state`

## 🖥 System Supervision
- System stats: CPU temp/usage, uptime, load, RAM, disk, throttling flags
- Services: systemd status + guarded restart endpoint

## 🌐 Network & Audio
- Network: SSID + IPs (read-only)
- Audio: volume + mute state via ALSA (read-only)

## 🔐 Security Model
- Optional API key header: `X-API-Key: <key>`
- Risky operations require `{ "confirm": true }`
- Cooldown rate limits prevent repeated triggers
- Power actions blocked unless `NDEFENDER_ALLOW_UNSAFE=true`

## 📡 WebSocket Model
Canonical envelope:
```json
{
  "type": "SYSTEM_STATUS",
  "timestamp_ms": 1700000000000,
  "source": "system",
  "data": {"cpu_temp_c": 45.2}
}
```

## 🧪 Testing & CI
- Lint: `ruff check .`
- Tests: `pytest`
- CI: GitHub Actions runs lint + tests on push/PR

## 🛠 Deployment
Systemd sample: `docs/systemd/ndefender-system-controller.service`

Example:
```ini
[Service]
ExecStart=/opt/ndefender-system-controller/.venv/bin/uvicorn ndefender_system_controller.main:app --host 0.0.0.0 --port 8000
Restart=always
```

## 🟢 GREEN Checklist
- [x] CI passed
- [x] Tests passed
- [x] UPS verified via decode + I2C path
- [x] Services verified via systemctl status
- [x] WebSocket verified (HELLO + SYSTEM_STATUS)
- [x] API endpoints verified (REST + WS)

## 📈 Roadmap
- Wi‑Fi connect/disconnect with guard rails
- Audio set/mute controls
- Extended UPS analytics and alerts
- Config-driven service allowlist

## 🔒 Release Locked
This version is production-frozen. All future changes must increment semantic versioning.

## API Examples
Health:
```bash
curl -s http://127.0.0.1:8000/api/v1/health
```

Status:
```bash
curl -s http://127.0.0.1:8000/api/v1/status
```

UPS:
```bash
curl -s http://127.0.0.1:8000/api/v1/ups
```

Reboot (guarded):
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/system/reboot \
  -H 'content-type: application/json' \
  -d '{"confirm": true}'
```

Sample UPS JSON:
```json
{
  "pack_voltage_v": 15.2,
  "current_a": -1.2,
  "input_vbus_v": 5.0,
  "input_power_w": 10.5,
  "soc_percent": 84,
  "time_to_empty_s": 3600,
  "time_to_full_s": null,
  "per_cell_v": [3.8, 3.8, 3.8, 3.8],
  "state": "DISCHARGING"
}
```

## 📚 Docs
- `ROADMAP.md`
- `progress.md`
- `docs/ARCHITECTURE.md`
- `docs/API.md`
- `docs/USAGE.md`
- `docs/TESTING.md`
- `docs/DEPLOYMENT.md`
- `docs/SYSTEM_CONTROLS.md`
- `docs/UPS_HAT_E.md`
- `docs/SERVICES.md`
- `docs/NETWORK.md`
- `docs/AUDIO.md`
- `docs/SECURITY.md`
