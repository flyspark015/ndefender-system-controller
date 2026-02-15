import asyncio

from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from ..core.supervisor import WsBroadcaster
from ..models import WsEnvelope
from .routes_status import hello_envelope

router = APIRouter()


class WsManager(WsBroadcaster):
    def __init__(self) -> None:
        self._connections: dict[WebSocket, asyncio.Lock] = {}
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket) -> None:
        await ws.accept()
        async with self._lock:
            self._connections[ws] = asyncio.Lock()

    async def disconnect(self, ws: WebSocket) -> None:
        async with self._lock:
            self._connections.pop(ws, None)

    async def broadcast(self, envelope: WsEnvelope) -> None:
        payload = envelope.model_dump()
        async with self._lock:
            items = list(self._connections.items())
        for ws, send_lock in items:
            try:
                async with send_lock:
                    await ws.send_json(payload)
            except Exception:
                await self.disconnect(ws)

    async def send(self, ws: WebSocket, envelope: WsEnvelope) -> None:
        async with self._lock:
            send_lock = self._connections.get(ws)
        if send_lock is None:
            return
        async with send_lock:
            await ws.send_json(envelope.model_dump())


@router.websocket("/ws")
async def ws_endpoint(ws: WebSocket) -> None:
    manager: WsManager = ws.app.state.ws_manager
    supervisor = ws.app.state.supervisor
    await manager.connect(ws)
    await manager.send(ws, hello_envelope())
    snapshot = await supervisor.snapshot()
    await manager.send(
        ws,
        WsEnvelope(
            type="SYSTEM_STATUS",
            timestamp_ms=snapshot.timestamp_ms,
            data=snapshot.system.model_dump(exclude_none=True) if snapshot.system else {},
        ),
    )
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        await manager.disconnect(ws)
