from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..core.supervisor import Supervisor
from ..models import ServiceStatus, WsEnvelope
from ..util.rate_limit import Cooldown
from ..util.time import now_ms

router = APIRouter()
_restart_cooldown = Cooldown(interval_s=10)


class RestartRequest(BaseModel):
    payload: dict = {}
    confirm: bool = False


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/services", response_model=list[ServiceStatus])
async def list_services(supervisor: Supervisor = Depends(get_supervisor)) -> list[ServiceStatus]:
    snapshot = await supervisor.snapshot()
    return snapshot.services


@router.post("/services/{name}/restart")
async def restart_service(
    name: str,
    body: RestartRequest,
    supervisor: Supervisor = Depends(get_supervisor),
) -> WsEnvelope:
    if not body.confirm:
        raise HTTPException(status_code=400, detail="confirm_required")
    if not _restart_cooldown.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok = supervisor.services_restart(name)
    return WsEnvelope(
        type="COMMAND_ACK",
        timestamp_ms=now_ms(),
        data={"command": "service_restart", "name": name, "ok": ok, "reason": None},
    )
