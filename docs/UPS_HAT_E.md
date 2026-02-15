# UPS HAT (E) 🔋

## Overview
UPS HAT (E) telemetry is collected over SMBus and normalized into a stable API model.

## Architecture
- I2C bus: `/dev/i2c-1`
- Address: `0x2d`
- Keepalive write: register `0x01` ← `0x55`

## API Examples
UPS snapshot:
```bash
curl -s http://127.0.0.1:8000/api/v1/ups
```

## Register Map
- `0x02` (1 byte): status flags
  - `0x40` fast charging
  - `0x80` charging
  - `0x20` discharging
- `0x10` (6 bytes): VBUS voltage/current/power
- `0x20` (12 bytes): pack voltage/current/SOC/time‑to‑empty/full
- `0x30` (8 bytes): per‑cell voltages

## Failure Modes
- If I2C read fails, an empty UPS model is returned.
- If bus cannot be opened, keepalive and reads are skipped.

## Safety Notes
- No automatic shutdown is triggered by this module.
- External policy can decide on low‑battery actions.

## Troubleshooting
- Check I2C bus: `i2cdetect -y 1`.
- Ensure `smbus2` is installed.

## Configuration
- `NDEFENDER_UPS_I2C_BUS` (default: 1)
- `NDEFENDER_UPS_I2C_ADDR` (default: 0x2d)
- `NDEFENDER_UPS_KEEPALIVE_S` (default: 5)

## Performance Notes
- Polling interval defaults to 2 seconds.

## Security Notes
- UPS reads are local hardware operations and are not network‑exposed.
