from fastapi import APIRouter, WebSocket

from .routes_status import hello_envelope

router = APIRouter()


@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    await ws.send_json(hello_envelope().model_dump())
    await ws.close()
