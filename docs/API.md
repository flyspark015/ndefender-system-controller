# API 📘

Base path: `/api/v1`

## Authentication
Optional API key header:
- `X-API-Key: <key>`

If no API key is configured, requests are allowed without auth.

## REST Endpoints

### `GET /health`
Response:
```
{
  "ok": true,
  "timestamp_ms": 0,
  "version": "0.1.0"
}
```

### `GET /status`
Combined snapshot of all modules.

Response:
```
{
  "timestamp_ms": 0,
  "system": { ... },
  "ups": { ... },
  "services": [ ... ],
  "network": { ... },
  "audio": { ... }
}
```

### `GET /system`
Response:
```
{
  "uptime_s": 0,
  "cpu_temp_c": 45.2,
  "cpu_usage_percent": 12.3,
  "load_1m": 0.12,
  "load_5m": 0.08,
  "load_15m": 0.05,
  "ram_used_mb": 512,
  "ram_total_mb": 4096,
  "disk_used_gb": 12,
  "disk_total_gb": 64,
  "throttled_flags": 0
}
```

### `GET /ups`
Response:
```
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

### `GET /services`
Response:
```
[
  {
    "name": "ndefender-backend.service",
    "active_state": "active",
    "sub_state": "running",
    "restart_count": 0
  }
]
```

### `POST /services/{name}/restart`
Body:
```
{ "confirm": true }
```

Response:
```
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 0,
  "source": "system",
  "data": {
    "command": "service_restart",
    "name": "ndefender-backend",
    "ok": true
  }
}
```

### `GET /network`
Response:
```
{
  "connected": true,
  "ssid": "MyWifi",
  "ip_v4": "192.168.1.10",
  "ip_v6": null
}
```

### `GET /audio`
Response:
```
{
  "volume_percent": 70,
  "muted": false
}
```

### `POST /system/reboot`
Body:
```
{ "confirm": true }
```

Response:
```
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 0,
  "source": "system",
  "data": {
    "command": "reboot",
    "ok": false,
    "reason": "unsafe_disabled"
  }
}
```

### `POST /system/shutdown`
Body:
```
{ "confirm": true }
```

Response:
```
{
  "type": "COMMAND_ACK",
  "timestamp_ms": 0,
  "source": "system",
  "data": {
    "command": "shutdown",
    "ok": false,
    "reason": "unsafe_disabled"
  }
}
```

## WebSocket
Endpoint:
- `WS /ws`

Envelope:
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

## Error Codes
- `400` missing confirmation
- `401` invalid API key
- `403` unsafe operations disabled
- `429` cooldown active
