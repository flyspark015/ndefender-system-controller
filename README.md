# N-Defender System Controller API ⚙️🛡️

Production-grade system control plane for Raspberry Pi 5. This service provides a single API surface for UPS telemetry, system health, services, network, audio, and safe power controls.

## System Overview 🧭
- FastAPI app with background pollers and a central state snapshot
- WebSocket fan-out for incremental updates
- Guarded power controls and rate limits for risky actions
- Optional API key authentication

## Quick Start 🚀
```
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn ndefender_system_controller.main:app --host 0.0.0.0 --port 8000
```

## Configuration 🧩
Environment variables:
- `NDEFENDER_API_KEY` (optional)
- `NDEFENDER_ALLOW_UNSAFE` (default: false)
- `NDEFENDER_SYSTEM_INTERVAL_S` (default: 2)
- `NDEFENDER_UPS_INTERVAL_S` (default: 2)
- `NDEFENDER_SERVICES_INTERVAL_S` (default: 5)
- `NDEFENDER_NETWORK_INTERVAL_S` (default: 5)
- `NDEFENDER_AUDIO_INTERVAL_S` (default: 5)
- `NDEFENDER_UPS_I2C_BUS` (default: 1)
- `NDEFENDER_UPS_I2C_ADDR` (default: 0x2d)
- `NDEFENDER_UPS_KEEPALIVE_S` (default: 5)

## API Base 🌐
- Base path: `/api/v1`
- Health: `GET /api/v1/health`
- Status: `GET /api/v1/status`
- WS: `WS /api/v1/ws`

## Dev Tools 🧰
- `tools/dev_client.py` (REST + WS)
- `tools/ups_dump.py` (direct UPS read)

## Verification ✅
```
ruff check .
pytest
```

## GREEN Checklist ✅
- App boots with `uvicorn`
- `/api/v1/health` returns ok
- `/api/v1/status` returns snapshot
- WS accepts a client and sends HELLO/STATUS
- `ruff` passes
- `pytest` passes
- Docs present for all modules
- systemd unit sample works on Pi
- Guarded endpoints enforce `confirm` + cooldown

## Docs 📘
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
