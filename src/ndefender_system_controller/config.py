import os
from dataclasses import dataclass

from . import __version__


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class AppConfig:
    name: str = "ndefender-system-controller"
    version: str = __version__
    api_key: str | None = None
    allow_unsafe: bool = False

    @staticmethod
    def from_env() -> "AppConfig":
        return AppConfig(
            name=os.getenv("NDEFENDER_APP_NAME", "ndefender-system-controller"),
            version=os.getenv("NDEFENDER_APP_VERSION", __version__),
            api_key=os.getenv("NDEFENDER_API_KEY") or None,
            allow_unsafe=_env_bool("NDEFENDER_ALLOW_UNSAFE", False),
        )
