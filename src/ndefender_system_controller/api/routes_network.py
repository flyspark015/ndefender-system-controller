from fastapi import APIRouter, Depends, Request

from ..core.supervisor import Supervisor
from ..models import NetworkStatus

router = APIRouter()


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/network", response_model=NetworkStatus)
async def network_status(supervisor: Supervisor = Depends(get_supervisor)) -> NetworkStatus:
    snapshot = await supervisor.snapshot()
    return snapshot.network
