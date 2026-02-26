import json
import subprocess
import time

from ..models import GpsState
from ..util.time import now_ms


class GpsManager:
    def status(self) -> GpsState:
        timestamp_ms = now_ms()
        if not self._gpspipe_available():
            return GpsState(
                timestamp_ms=timestamp_ms,
                fix="NO_FIX",
                satellites={"in_view": 0, "in_use": 0},
                last_update_ms=timestamp_ms,
                source="gpsd",
                last_error="gpspipe_not_found",
            )
        data = self._read_gpspipe()
        if not data:
            return GpsState(
                timestamp_ms=timestamp_ms,
                fix="NO_FIX",
                satellites={"in_view": 0, "in_use": 0},
                last_update_ms=timestamp_ms,
                source="gpsd",
                last_error="gpsd_no_data",
            )
        return data

    def restart(self) -> bool:
        try:
            subprocess.run(
                ["systemctl", "restart", "gpsd"],
                check=False,
                capture_output=True,
                text=True,
            )
            return True
        except Exception:
            return False

    def _gpspipe_available(self) -> bool:
        return subprocess.call(["/bin/sh", "-c", "command -v gpspipe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

    def _read_gpspipe(self) -> GpsState | None:
        timestamp_ms = now_ms()
        try:
            proc = subprocess.run(
                ["gpspipe", "-w", "-n", "5"],
                capture_output=True,
                text=True,
                check=False,
                timeout=3,
            )
        except Exception:
            return None
        if proc.returncode != 0:
            return None
        tpv = None
        sky = None
        for line in proc.stdout.splitlines():
            try:
                payload = json.loads(line)
            except Exception:
                continue
            if payload.get("class") == "TPV":
                tpv = payload
            elif payload.get("class") == "SKY":
                sky = payload
        fix_mode = "NO_FIX"
        if tpv:
            mode = int(tpv.get("mode") or 0)
            if mode == 2:
                fix_mode = "FIX_2D"
            elif mode == 3:
                fix_mode = "FIX_3D"
        satellites = {"in_view": 0, "in_use": 0}
        if sky and isinstance(sky.get("satellites"), list):
            sats = sky.get("satellites")
            satellites["in_view"] = len(sats)
            satellites["in_use"] = sum(1 for s in sats if s.get("used"))
        return GpsState(
            timestamp_ms=timestamp_ms,
            fix=fix_mode,
            satellites=satellites,
            hdop=tpv.get("hdop") if tpv else None,
            vdop=tpv.get("vdop") if tpv else None,
            pdop=tpv.get("pdop") if tpv else None,
            latitude=tpv.get("lat") if tpv else None,
            longitude=tpv.get("lon") if tpv else None,
            altitude_m=tpv.get("alt") if tpv else None,
            speed_m_s=tpv.get("speed") if tpv else None,
            heading_deg=tpv.get("track") if tpv else None,
            last_update_ms=timestamp_ms,
            age_ms=0,
            source="gpsd",
        )
