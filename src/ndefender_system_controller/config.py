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


@dataclass(frozen=True)
class SchedulerConfig:
    system_interval_s: float = 2.0
    ups_interval_s: float = 2.0
    services_interval_s: float = 5.0
    network_interval_s: float = 5.0
    audio_interval_s: float = 5.0

    @staticmethod
    def from_env() -> "SchedulerConfig":
        return SchedulerConfig(
            system_interval_s=float(os.getenv("NDEFENDER_SYSTEM_INTERVAL_S", "2")),
            ups_interval_s=float(os.getenv("NDEFENDER_UPS_INTERVAL_S", "2")),
            services_interval_s=float(os.getenv("NDEFENDER_SERVICES_INTERVAL_S", "5")),
            network_interval_s=float(os.getenv("NDEFENDER_NETWORK_INTERVAL_S", "5")),
            audio_interval_s=float(os.getenv("NDEFENDER_AUDIO_INTERVAL_S", "5")),
        )


@dataclass(frozen=True)
class UpsConfig:
    i2c_bus: int = 1
    i2c_addr: int = 0x2D
    keepalive_interval_s: float = 5.0

    @staticmethod
    def from_env() -> "UpsConfig":
        return UpsConfig(
            i2c_bus=int(os.getenv("NDEFENDER_UPS_I2C_BUS", "1")),
            i2c_addr=int(os.getenv("NDEFENDER_UPS_I2C_ADDR", "0x2d"), 0),
            keepalive_interval_s=float(os.getenv("NDEFENDER_UPS_KEEPALIVE_S", "5")),
        )
