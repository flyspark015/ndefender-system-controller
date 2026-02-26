from fastapi import APIRouter, Depends, Request

from ..config import AppConfig
from ..core.supervisor import Supervisor
from ..models import HealthResponse, StatusSnapshot, WsEnvelope
from ..util.time import now_ms

router = APIRouter()


def get_config() -> AppConfig:
    return AppConfig.from_env()


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/health", response_model=HealthResponse)
def health(config: AppConfig = Depends(get_config)) -> HealthResponse:
    return HealthResponse(ok=True, timestamp_ms=now_ms(), version=config.version)


@router.get("/status", response_model=StatusSnapshot)
async def status(supervisor: Supervisor = Depends(get_supervisor)) -> StatusSnapshot:
    return await supervisor.snapshot()


def hello_envelope() -> WsEnvelope:
    return WsEnvelope(type="LOG_EVENT", timestamp_ms=now_ms(), data={"message": "HELLO"})
