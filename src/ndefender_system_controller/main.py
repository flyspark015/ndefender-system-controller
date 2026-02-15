from fastapi import FastAPI

from .api.routes_status import router as status_router
from .api.ws import router as ws_router
from .util.logging import configure_logging


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="N-Defender System Controller API")
    app.include_router(status_router, prefix="/api/v1", tags=["status"])
    app.include_router(ws_router, prefix="/api/v1", tags=["ws"])
    return app


app = create_app()
