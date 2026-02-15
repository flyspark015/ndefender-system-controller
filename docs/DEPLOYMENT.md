# Deployment 🚀

## Overview
This document describes production deployment using systemd.

## Architecture
- Service runs as a simple systemd unit
- Uvicorn hosts the FastAPI app on port 8000

## API Examples
Health check after deploy:
```bash
curl -s http://127.0.0.1:8000/api/v1/health
```

## Failure Modes
- Missing venv or deps will prevent service start.
- Wrong WorkingDirectory will fail import resolution.

## Safety Notes
- Keep `NDEFENDER_ALLOW_UNSAFE=false` unless required.

## Troubleshooting
- `systemctl status ndefender-system-controller`
- `journalctl -u ndefender-system-controller -f`

## Configuration
Sample unit: `docs/systemd/ndefender-system-controller.service`

```
[Unit]
Description=N-Defender System Controller API
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/ndefender-system-controller
ExecStart=/opt/ndefender-system-controller/.venv/bin/uvicorn ndefender_system_controller.main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=3
Environment=NDEFENDER_API_KEY=
Environment=NDEFENDER_ALLOW_UNSAFE=false

[Install]
WantedBy=multi-user.target
```

Install steps:
1. Copy repo to `/opt/ndefender-system-controller`
2. Create venv: `python3 -m venv .venv`
3. Install deps: `. .venv/bin/activate && pip install -e .[dev]`
4. Copy unit to `/etc/systemd/system/ndefender-system-controller.service`
5. Reload: `sudo systemctl daemon-reload`
6. Enable: `sudo systemctl enable --now ndefender-system-controller`

## Performance Notes
- Use `uvicorn` with `--workers 1` on Pi for consistent CPU usage.

## Security Notes
- Use API key on untrusted networks.
- Restrict firewall to LAN if possible.
