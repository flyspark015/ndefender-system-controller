import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..core.supervisor import Supervisor
from ..models import CommandResult, GpsState
from ..util.rate_limit import RateLimiter
from ..util.time import now_ms

router = APIRouter()
_gps_restart_rate = RateLimiter(limit=2, window_s=60)


class CommandRequest(BaseModel):
    payload: dict = {}
    confirm: bool = False


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/gps", response_model=GpsState)
async def gps_status(supervisor: Supervisor = Depends(get_supervisor)) -> GpsState:
    return supervisor.gps_manager().status()


@router.post("/gps/restart", response_model=CommandResult)
async def gps_restart(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not body.confirm:
        raise HTTPException(status_code=400, detail="confirm_required")
    if not _gps_restart_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok = supervisor.gps_manager().restart()
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="gps/restart",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )
