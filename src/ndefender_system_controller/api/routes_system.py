import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..config import AppConfig
from ..core.power_control import PowerController
from ..core.supervisor import Supervisor
from ..models import CommandResult, SystemStats
from ..util.rate_limit import RateLimiter
from ..util.time import now_ms

router = APIRouter()
_danger_rate = RateLimiter(limit=2, window_s=60)


class PowerRequest(BaseModel):
    payload: dict = {}
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
) -> CommandResult:
    if not body.confirm:
        raise HTTPException(status_code=400, detail="confirm_required")
    if not _danger_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok, reason = PowerController(config).reboot()
    if not ok and reason == "unsafe_disabled":
        raise HTTPException(status_code=403, detail="unsafe_disabled")
    if not ok:
        raise HTTPException(status_code=409, detail=reason or "invalid_state")
    return CommandResult(
        command="system/reboot",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/system/shutdown")
async def system_shutdown(
    body: PowerRequest,
    config: AppConfig = Depends(get_config),
) -> CommandResult:
    if not body.confirm:
        raise HTTPException(status_code=400, detail="confirm_required")
    if not _danger_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok, reason = PowerController(config).shutdown()
    if not ok and reason == "unsafe_disabled":
        raise HTTPException(status_code=403, detail="unsafe_disabled")
    if not ok:
        raise HTTPException(status_code=409, detail=reason or "invalid_state")
    return CommandResult(
        command="system/shutdown",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )
