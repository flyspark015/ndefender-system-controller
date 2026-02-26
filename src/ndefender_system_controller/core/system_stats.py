import os
import subprocess
import time

import psutil

from ..models import CpuStats, RamStats, StorageState, StorageStats, SystemStats, SystemVersion
from ..util.time import now_ms

_THERMAL_PATHS = (
    "/sys/class/thermal/thermal_zone0/temp",
    "/sys/class/hwmon/hwmon0/temp1_input",
)


class SystemStatsCollector:
    def __init__(self) -> None:
        self._boot_time = psutil.boot_time()

    def read(self) -> SystemStats:
        cpu_temp = self._cpu_temp_c()
        cpu_usage = psutil.cpu_percent(interval=None)
        load_1m = self._load_avg(0)
        load_5m = self._load_avg(1)
        load_15m = self._load_avg(2)
        ram_used = self._ram_used_mb()
        ram_total = self._ram_total_mb()
        disk_used = self._disk_used_gb()
        disk_total = self._disk_total_gb()
        return SystemStats(
            timestamp_ms=now_ms(),
            status="ok",
            uptime_s=self._uptime_s(),
            version=SystemVersion(app="ndefender-system-controller"),
            cpu=CpuStats(
                temp_c=cpu_temp,
                load1=load_1m,
                load5=load_5m,
                load15=load_15m,
                usage_percent=cpu_usage,
            ),
            ram=RamStats(total_mb=ram_total, used_mb=ram_used, free_mb=self._ram_free_mb()),
            storage=StorageState(
                root=StorageStats(
                    total_gb=self._disk_total_gb_float(),
                    used_gb=self._disk_used_gb_float(),
                    free_gb=self._disk_free_gb_float(),
                )
            ),
            cpu_temp_c=cpu_temp,
            cpu_usage_percent=cpu_usage,
            load_1m=load_1m,
            load_5m=load_5m,
            load_15m=load_15m,
            ram_used_mb=ram_used,
            ram_total_mb=ram_total,
            disk_used_gb=disk_used,
            disk_total_gb=disk_total,
            throttled_flags=self._throttled_flags(),
        )

    def _uptime_s(self) -> int:
        return int(time.time() - self._boot_time)

    def _cpu_temp_c(self) -> float | None:
        for path in _THERMAL_PATHS:
            if not os.path.exists(path):
                continue
            try:
                raw = open(path, "r", encoding="utf-8").read().strip()
                if not raw:
                    continue
                value = float(raw)
                if value > 1000:
                    value = value / 1000.0
                return round(value, 1)
            except Exception:
                continue
        return None

    @staticmethod
    def _load_avg(index: int) -> float | None:
        try:
            return os.getloadavg()[index]
        except OSError:
            return None

    @staticmethod
    def _ram_used_mb() -> int | None:
        try:
            return int(psutil.virtual_memory().used / (1024 * 1024))
        except Exception:
            return None

    @staticmethod
    def _ram_total_mb() -> int | None:
        try:
            return int(psutil.virtual_memory().total / (1024 * 1024))
        except Exception:
            return None

    @staticmethod
    def _disk_used_gb() -> int | None:
        try:
            return int(psutil.disk_usage("/").used / (1024 * 1024 * 1024))
        except Exception:
            return None

    @staticmethod
    def _disk_total_gb() -> int | None:
        try:
            return int(psutil.disk_usage("/").total / (1024 * 1024 * 1024))
        except Exception:
            return None

    @staticmethod
    def _throttled_flags() -> int | None:
        try:
            result = subprocess.run(
                ["vcgencmd", "get_throttled"],
                check=False,
                capture_output=True,
                text=True,
                timeout=0.5,
            )
            if result.returncode != 0:
                return None
            output = result.stdout.strip()
            if "0x" not in output:
                return None
            value = output.split("0x", 1)[1].strip()
            return int(value, 16)
        except Exception:
            return None

    @staticmethod
    def _ram_free_mb() -> int | None:
        try:
            return int(psutil.virtual_memory().available / (1024 * 1024))
        except Exception:
            return None

    @staticmethod
    def _disk_used_gb_float() -> float | None:
        try:
            return round(psutil.disk_usage("/").used / (1024 * 1024 * 1024), 3)
        except Exception:
            return None

    @staticmethod
    def _disk_total_gb_float() -> float | None:
        try:
            return round(psutil.disk_usage("/").total / (1024 * 1024 * 1024), 3)
        except Exception:
            return None

    @staticmethod
    def _disk_free_gb_float() -> float | None:
        try:
            return round(psutil.disk_usage("/").free / (1024 * 1024 * 1024), 3)
        except Exception:
            return None
