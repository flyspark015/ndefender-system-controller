# Deployment 🚀

## Systemd Unit (Sample)
Path: `docs/systemd/ndefender-system-controller.service`

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

## Install Steps
1. Copy repo to `/opt/ndefender-system-controller`
2. Create venv and install deps: `python3 -m venv .venv && . .venv/bin/activate && pip install -e .[dev]`
3. Copy the unit file to `/etc/systemd/system/ndefender-system-controller.service`
4. `sudo systemctl daemon-reload`
5. `sudo systemctl enable --now ndefender-system-controller`

## Logs
- `journalctl -u ndefender-system-controller -f`
