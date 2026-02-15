# Security 🔒

## API Key
Set `NDEFENDER_API_KEY` and send `X-API-Key` with requests.

## Risky Operations
- Restart, reboot, and shutdown require `{"confirm": true}`
- Cooldown rate limits are enforced
- Power controls are disabled unless `NDEFENDER_ALLOW_UNSAFE=true`
