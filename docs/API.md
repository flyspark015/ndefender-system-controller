# API 📘

Base path: `/api/v1`

## REST
- `GET /health`
- `GET /status`
- `GET /system`
- `GET /ups`
- `GET /services`
- `POST /services/{name}/restart`
- `GET /network`
- `GET /audio`
- `POST /system/reboot`
- `POST /system/shutdown`

## Auth
- Optional API key header: `X-API-Key: <key>`

## WebSocket
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
