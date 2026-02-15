# Testing ✅

## Overview
Testing covers API contracts, WS envelope validation, UPS decode logic, rate limiting, and power guard rails.

## Architecture
- Unit tests run against FastAPI test client.
- No hardware access is required.

## API Examples
Run all tests:
```bash
pytest
```

Lint:
```bash
ruff check .
```

## Failure Modes
- If pytest fails, check dependency install and FastAPI version.
- If ruff fails, run with `--fix` to see formatting issues.

## Safety Notes
- Tests do not trigger real reboot/shutdown.
- Power controller is blocked unless unsafe mode is enabled.

## Troubleshooting
- Ensure `.venv` is active.
- Reinstall deps: `pip install -e .[dev]`.

## Configuration
- No additional config required.

## Performance Notes
- Test suite completes in under a few seconds on Pi 5.

## Security Notes
- Tests do not require API key by default.
