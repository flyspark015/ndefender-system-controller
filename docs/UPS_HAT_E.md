# UPS HAT (E) 🔋

## Interface
- I2C bus: `/dev/i2c-1`
- Address: `0x2d`
- Keepalive: write `0x55` to register `0x01`

## Register Map
- `0x02` (1 byte): status flags
  - `0x40` fast charging
  - `0x80` charging
  - `0x20` discharging
- `0x10` (6 bytes): VBUS
  - voltage (mV), current (mA), power (mW)
- `0x20` (12 bytes): battery
  - pack voltage (mV)
  - current (mA, signed)
  - SOC (%)
  - remaining capacity (mAh)
  - time to empty (min)
  - time to full (min)
- `0x30` (8 bytes): cell voltages (mV)

## Normalized Output
- `pack_voltage_v`, `current_a`, `input_vbus_v`, `input_power_w`
- `soc_percent`, `time_to_empty_s`, `time_to_full_s`
- `per_cell_v[4]`, `state`

## Notes
- Keepalive is sent on a timer and does not block polling.
- Read failures return empty UPS models rather than crashing the service.
