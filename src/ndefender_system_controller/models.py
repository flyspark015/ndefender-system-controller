from typing import Any, Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    ok: bool
    timestamp_ms: int
    version: str


class SystemVersion(BaseModel):
    app: str | None = None
    git_sha: str | None = None
    build_ts: int | None = None


class CpuStats(BaseModel):
    temp_c: float | None = None
    load1: float | None = None
    load5: float | None = None
    load15: float | None = None
    usage_percent: float | None = None


class RamStats(BaseModel):
    total_mb: int | None = None
    used_mb: int | None = None
    free_mb: int | None = None


class StorageStats(BaseModel):
    total_gb: float | None = None
    used_gb: float | None = None
    free_gb: float | None = None


class StorageState(BaseModel):
    root: StorageStats | None = None
    logs: StorageStats | None = None


class SystemStats(BaseModel):
    timestamp_ms: int | None = None
    status: Literal["ok", "degraded", "offline"] | None = None
    uptime_s: int | None = None
    version: SystemVersion | None = None
    cpu: CpuStats | None = None
    ram: RamStats | None = None
    storage: StorageState | None = None
    last_error: str | None = None
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
    timestamp_ms: int | None = None
    status: Literal["ok", "degraded", "offline"] | None = None
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
    last_error: str | None = None


class ServiceStatus(BaseModel):
    name: str
    active_state: str
    sub_state: str
    restart_count: int = 0
    uptime_s: int | None = None
    last_restart_ms: int | None = None
    last_error: str | None = None


class WifiState(BaseModel):
    timestamp_ms: int | None = None
    enabled: bool | None = None
    connected: bool | None = None
    ssid: str | None = None
    bssid: str | None = None
    ip: str | None = None
    rssi_dbm: int | None = None
    link_quality: int | None = None
    last_update_ms: int | None = None
    last_error: str | None = None


class WifiScanResult(BaseModel):
    timestamp_ms: int | None = None
    networks: list[dict[str, Any]] = Field(default_factory=list)
    last_error: str | None = None


class BluetoothState(BaseModel):
    timestamp_ms: int | None = None
    enabled: bool | None = None
    scanning: bool | None = None
    paired_count: int | None = None
    connected_devices: list[dict[str, Any]] = Field(default_factory=list)
    last_update_ms: int | None = None
    last_error: str | None = None


class BluetoothDeviceList(BaseModel):
    timestamp_ms: int | None = None
    devices: list[dict[str, Any]] = Field(default_factory=list)


class GpsState(BaseModel):
    timestamp_ms: int | None = None
    fix: Literal["NO_FIX", "FIX_2D", "FIX_3D"] | None = None
    satellites: dict[str, int] | None = None
    hdop: float | None = None
    vdop: float | None = None
    pdop: float | None = None
    latitude: float | None = None
    longitude: float | None = None
    altitude_m: float | None = None
    speed_m_s: float | None = None
    heading_deg: float | None = None
    last_update_ms: int | None = None
    age_ms: int | None = None
    source: str | None = None
    last_error: str | None = None


class NetworkStatus(BaseModel):
    connected: bool | None = None
    ssid: str | None = None
    ip_v4: str | None = None
    ip_v6: str | None = None
    wifi: WifiState | None = None
    bluetooth: BluetoothState | None = None


class AudioStatus(BaseModel):
    timestamp_ms: int | None = None
    status: Literal["ok", "degraded", "offline"] | None = None
    volume_percent: int | None = None
    muted: bool | None = None
    last_error: str | None = None


class StatusSnapshot(BaseModel):
    timestamp_ms: int
    system: SystemStats | None = None
    ups: UpsStatus | None = None
    services: list[ServiceStatus] = Field(default_factory=list)
    network: NetworkStatus | None = None
    gps: GpsState | None = None
    audio: AudioStatus | None = None


class CommandResult(BaseModel):
    command: str
    command_id: str
    accepted: bool
    detail: str | None = None
    timestamp_ms: int


class WsEnvelope(BaseModel):
    type: str
    timestamp_ms: int
    source: Literal["system"] = "system"
    data: dict[str, Any] = Field(default_factory=dict)
