# N-Defender System Controller API ⚙️🛡️

Production-grade system control plane for Raspberry Pi 5. This service provides a single API surface for UPS telemetry, system health, services, network, audio, and safe power controls.

## Quick Start 🚀
```
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn ndefender_system_controller.main:app --host 0.0.0.0 --port 8000
```

## API Base 🌐
- Base path: `/api/v1`
- Health: `GET /api/v1/health`
- Status: `GET /api/v1/status`
- WebSocket: `WS /api/v1/ws`

## Status 🧭
See `ROADMAP.md` for the phased plan and `progress.md` for live status.

## Safety & Auth 🔒
Optional API key auth via `X-API-Key`. Risky endpoints are guarded with confirmation and cooldown rate limits.

## Development ✅
```
ruff check .
pytest
```
