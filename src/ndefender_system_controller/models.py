from typing import Any, Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    ok: bool
    timestamp_ms: int
    version: str


class SystemStats(BaseModel):
    uptime_s: int | None = None
    cpu_temp_c: float | None = None
    cpu_usage_percent: float | None = None
    load_1m: float | None = None
    load_5m: float | None = None
    load_15m: float | None = None
    ram_used_mb: int | None = None
    ram_total_mb: int | None = None
    disk_used_gb: int | None = None
    disk_total_gb: int | None = None
    throttled_flags: int | None = None


class UpsStatus(BaseModel):
    pack_voltage_v: float | None = None
    current_a: float | None = None
    input_vbus_v: float | None = None
    input_power_w: float | None = None
    soc_percent: int | None = None
    time_to_empty_s: int | None = None
    time_to_full_s: int | None = None
    per_cell_v: list[float] = Field(default_factory=list)
    state: Literal[
        "IDLE", "CHARGING", "FAST_CHARGING", "DISCHARGING", "UNKNOWN"
    ] = "UNKNOWN"


class ServiceStatus(BaseModel):
    name: str
    active_state: str
    sub_state: str
    restart_count: int = 0


class NetworkStatus(BaseModel):
    connected: bool | None = None
    ssid: str | None = None
    ip_v4: str | None = None
    ip_v6: str | None = None


class AudioStatus(BaseModel):
    volume_percent: int | None = None
    muted: bool | None = None


class StatusSnapshot(BaseModel):
    timestamp_ms: int
    system: SystemStats | None = None
    ups: UpsStatus | None = None
    services: list[ServiceStatus] = Field(default_factory=list)
    network: NetworkStatus | None = None
    audio: AudioStatus | None = None


class WsEnvelope(BaseModel):
    type: str
    timestamp_ms: int
    source: Literal["system"] = "system"
    data: dict[str, Any] = Field(default_factory=dict)
