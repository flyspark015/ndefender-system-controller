from fastapi import Header, HTTPException, status

from ..config import AppConfig


class ApiKeyAuth:
    def __init__(self, config: AppConfig):
        self._config = config

    def __call__(self, x_api_key: str | None = Header(default=None)) -> None:
        if not self._config.api_key:
            return
        if x_api_key != self._config.api_key:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
