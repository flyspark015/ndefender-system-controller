from fastapi import APIRouter, Depends

from ..config import AppConfig
from ..models import HealthResponse, StatusSnapshot, WsEnvelope
from ..util.auth import ApiKeyAuth
from ..util.time import now_ms

router = APIRouter()


def get_config() -> AppConfig:
    return AppConfig.from_env()


def get_auth(config: AppConfig = Depends(get_config)) -> ApiKeyAuth:
    return ApiKeyAuth(config)


@router.get("/health", response_model=HealthResponse)
def health(config: AppConfig = Depends(get_config)) -> HealthResponse:
    return HealthResponse(ok=True, timestamp_ms=now_ms(), version=config.version)


@router.get("/status", response_model=StatusSnapshot, dependencies=[Depends(get_auth)])
def status() -> StatusSnapshot:
    return StatusSnapshot(timestamp_ms=now_ms())


def hello_envelope() -> WsEnvelope:
    return WsEnvelope(type="LOG_EVENT", timestamp_ms=now_ms(), data={"message": "HELLO"})
