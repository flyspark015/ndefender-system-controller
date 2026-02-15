from fastapi import APIRouter, Depends, Request

from ..core.supervisor import Supervisor
from ..models import SystemStats

router = APIRouter()


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/system", response_model=SystemStats)
async def system_status(supervisor: Supervisor = Depends(get_supervisor)) -> SystemStats:
    snapshot = await supervisor.snapshot()
    return snapshot.system
