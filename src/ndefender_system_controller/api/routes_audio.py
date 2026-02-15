from fastapi import APIRouter, Depends, Request

from ..core.supervisor import Supervisor
from ..models import AudioStatus

router = APIRouter()


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/audio", response_model=AudioStatus)
async def audio_status(supervisor: Supervisor = Depends(get_supervisor)) -> AudioStatus:
    snapshot = await supervisor.snapshot()
    return snapshot.audio
