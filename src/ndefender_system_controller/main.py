from contextlib import asynccontextmanager

from fastapi import FastAPI

from .api.routes_audio import router as audio_router
from .api.routes_network import router as network_router
from .api.routes_services import router as services_router
from .api.routes_status import router as status_router
from .api.routes_system import router as system_router
from .api.routes_ups import router as ups_router
from .api.ws import WsManager
from .api.ws import router as ws_router
from .config import SchedulerConfig
from .core.supervisor import Supervisor
from .util.logging import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await app.state.supervisor.start()
    try:
        yield
    finally:
        await app.state.supervisor.stop()


def create_app() -> FastAPI:
    app = FastAPI(title="N-Defender System Controller API", lifespan=lifespan)
    ws_manager = WsManager()
    supervisor = Supervisor(SchedulerConfig.from_env(), ws_manager)
    app.state.ws_manager = ws_manager
    app.state.supervisor = supervisor
    app.include_router(status_router, prefix="/api/v1", tags=["status"])
    app.include_router(system_router, prefix="/api/v1", tags=["system"])
    app.include_router(ups_router, prefix="/api/v1", tags=["ups"])
    app.include_router(services_router, prefix="/api/v1", tags=["services"])
    app.include_router(network_router, prefix="/api/v1", tags=["network"])
    app.include_router(audio_router, prefix="/api/v1", tags=["audio"])
    app.include_router(ws_router, prefix="/api/v1", tags=["ws"])
    return app


app = create_app()
