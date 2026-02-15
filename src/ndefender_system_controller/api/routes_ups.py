from fastapi import APIRouter, Depends, Request

from ..core.supervisor import Supervisor
from ..models import UpsStatus

router = APIRouter()


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/ups", response_model=UpsStatus)
async def ups_status(supervisor: Supervisor = Depends(get_supervisor)) -> UpsStatus:
    snapshot = await supervisor.snapshot()
    return snapshot.ups
