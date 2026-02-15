#!/usr/bin/env python3
import argparse
import asyncio
import json
import os

import httpx
import websockets


def _headers(api_key: str | None) -> dict[str, str]:
    if not api_key:
        return {}
    return {"X-API-Key": api_key}


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2))


def call_rest(base_url: str, path: str, api_key: str | None) -> None:
    url = f"{base_url.rstrip('/')}{path}"
    with httpx.Client(timeout=5.0, headers=_headers(api_key)) as client:
        resp = client.get(url)
        resp.raise_for_status()
        _print_json(resp.json())


async def ws_listen(base_url: str, api_key: str | None) -> None:
    ws_url = base_url.replace("http://", "ws://").replace("https://", "wss://")
    ws_url = f"{ws_url.rstrip('/')}/api/v1/ws"
    headers = _headers(api_key)
    async with websockets.connect(ws_url, extra_headers=headers) as ws:
        while True:
            msg = await ws.recv()
            print(msg)


def main() -> None:
    parser = argparse.ArgumentParser(description="N-Defender System Controller dev client")
    parser.add_argument(
        "command",
        choices=["health", "status", "system", "ups", "services", "network", "audio", "ws"],
    )
    parser.add_argument("--base-url", default=os.getenv("NDEFENDER_BASE_URL", "http://127.0.0.1:8000"))
    parser.add_argument("--api-key", default=os.getenv("NDEFENDER_API_KEY"))
    args = parser.parse_args()

    if args.command == "ws":
        asyncio.run(ws_listen(args.base_url, args.api_key))
        return

    call_rest(args.base_url, f"/api/v1/{args.command}", args.api_key)


if __name__ == "__main__":
    main()
