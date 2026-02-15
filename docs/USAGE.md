# Usage 📗

## REST Examples
Health:
```
curl -s http://127.0.0.1:8000/api/v1/health
```

Status snapshot:
```
curl -s http://127.0.0.1:8000/api/v1/status
```

UPS:
```
curl -s http://127.0.0.1:8000/api/v1/ups
```

Services:
```
curl -s http://127.0.0.1:8000/api/v1/services
```

Restart a service (guarded):
```
curl -s -X POST http://127.0.0.1:8000/api/v1/services/ndefender-backend/restart \
  -H 'content-type: application/json' \
  -d '{"confirm": true}'
```

Reboot (guarded, unsafe disabled by default):
```
curl -s -X POST http://127.0.0.1:8000/api/v1/system/reboot \
  -H 'content-type: application/json' \
  -d '{"confirm": true}'
```

## WebSocket
Listen for updates:
```
python3 tools/dev_client.py ws --base-url http://127.0.0.1:8000
```

## Auth
If `NDEFENDER_API_KEY` is set, add:
```
-H 'X-API-Key: <key>'
```
