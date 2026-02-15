from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..config import AppConfig
from ..core.power_control import PowerController
from ..core.supervisor import Supervisor
from ..models import SystemStats, WsEnvelope
from ..util.rate_limit import Cooldown
from ..util.time import now_ms

router = APIRouter()
_reboot_cooldown = Cooldown(interval_s=30)
_shutdown_cooldown = Cooldown(interval_s=30)


class PowerRequest(BaseModel):
    confirm: bool = False


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


def get_config() -> AppConfig:
    return AppConfig.from_env()


@router.get("/system", response_model=SystemStats)
async def system_status(supervisor: Supervisor = Depends(get_supervisor)) -> SystemStats:
    snapshot = await supervisor.snapshot()
    return snapshot.system


@router.post("/system/reboot")
async def system_reboot(
    body: PowerRequest,
    config: AppConfig = Depends(get_config),
) -> WsEnvelope:
    if not body.confirm:
        raise HTTPException(status_code=400, detail="confirm must be true")
    if not _reboot_cooldown.allow():
        raise HTTPException(status_code=429, detail="cooldown active")
    ok, reason = PowerController(config).reboot()
    if not ok and reason == "unsafe_disabled":
        raise HTTPException(status_code=403, detail="unsafe operations disabled")
    return WsEnvelope(
        type="COMMAND_ACK",
        timestamp_ms=now_ms(),
        data={"command": "reboot", "ok": ok, "reason": reason},
    )


@router.post("/system/shutdown")
async def system_shutdown(
    body: PowerRequest,
    config: AppConfig = Depends(get_config),
) -> WsEnvelope:
    if not body.confirm:
        raise HTTPException(status_code=400, detail="confirm must be true")
    if not _shutdown_cooldown.allow():
        raise HTTPException(status_code=429, detail="cooldown active")
    ok, reason = PowerController(config).shutdown()
    if not ok and reason == "unsafe_disabled":
        raise HTTPException(status_code=403, detail="unsafe operations disabled")
    return WsEnvelope(
        type="COMMAND_ACK",
        timestamp_ms=now_ms(),
        data={"command": "shutdown", "ok": ok, "reason": reason},
    )
