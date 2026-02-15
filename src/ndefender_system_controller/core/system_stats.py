import os
import subprocess
import time

import psutil

from ..models import SystemStats

_THERMAL_PATHS = (
    "/sys/class/thermal/thermal_zone0/temp",
    "/sys/class/hwmon/hwmon0/temp1_input",
)


class SystemStatsCollector:
    def __init__(self) -> None:
        self._boot_time = psutil.boot_time()

    def read(self) -> SystemStats:
        return SystemStats(
            uptime_s=self._uptime_s(),
            cpu_temp_c=self._cpu_temp_c(),
            cpu_usage_percent=psutil.cpu_percent(interval=None),
            load_1m=self._load_avg(0),
            load_5m=self._load_avg(1),
            load_15m=self._load_avg(2),
            ram_used_mb=self._ram_used_mb(),
            ram_total_mb=self._ram_total_mb(),
            disk_used_gb=self._disk_used_gb(),
            disk_total_gb=self._disk_total_gb(),
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
