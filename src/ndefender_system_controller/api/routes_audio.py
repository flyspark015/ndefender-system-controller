import uuid

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..core.supervisor import Supervisor
from ..models import AudioStatus, CommandResult
from ..util.rate_limit import RateLimiter
from ..util.time import now_ms

router = APIRouter()
_audio_rate = RateLimiter(limit=10, window_s=60)


class CommandRequest(BaseModel):
    payload: dict = {}
    confirm: bool = False


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/audio", response_model=AudioStatus)
async def audio_status(supervisor: Supervisor = Depends(get_supervisor)) -> AudioStatus:
    snapshot = await supervisor.snapshot()
    return snapshot.audio


@router.post("/audio/mute", response_model=CommandResult)
async def audio_mute(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _audio_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    if "muted" not in body.payload:
        raise HTTPException(status_code=400, detail="invalid_payload")
    muted = bool(body.payload.get("muted"))
    ok = supervisor.audio_manager().set_mute(muted)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="audio/mute",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/audio/volume", response_model=CommandResult)
async def audio_volume(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _audio_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    if "volume_percent" not in body.payload:
        raise HTTPException(status_code=400, detail="invalid_payload")
    volume = body.payload.get("volume_percent")
    if not isinstance(volume, int) or not (0 <= volume <= 100):
        raise HTTPException(status_code=400, detail="invalid_payload")
    ok = supervisor.audio_manager().set_volume(volume)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="audio/volume",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )
