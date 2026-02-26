import subprocess

from ..models import AudioStatus
from ..util.time import now_ms


class AudioManager:
    def status(self) -> AudioStatus:
        volume = self._get_volume()
        muted = self._get_mute()
        status = "ok" if volume is not None or muted is not None else "degraded"
        last_error = None if status == "ok" else "audio_unavailable"
        return AudioStatus(
            timestamp_ms=now_ms(),
            status=status,
            volume_percent=volume,
            muted=muted,
            last_error=last_error,
        )

    def set_mute(self, muted: bool) -> bool:
        try:
            subprocess.run(
                ["amixer", "set", "Master", "mute" if muted else "unmute"],
                check=False,
                capture_output=True,
                text=True,
            )
            return True
        except Exception:
            return False

    def set_volume(self, volume_percent: int) -> bool:
        try:
            volume = max(0, min(100, int(volume_percent)))
            subprocess.run(
                ["amixer", "set", "Master", f"{volume}%"],
                check=False,
                capture_output=True,
                text=True,
            )
            return True
        except Exception:
            return False

    @staticmethod
    def _get_volume() -> int | None:
        try:
            output = subprocess.run(
                ["amixer", "get", "Master"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout
            for line in output.splitlines():
                if "%" in line:
                    start = line.find("[")
                    end = line.find("%", start)
                    if start != -1 and end != -1:
                        return int(line[start + 1 : end])
        except Exception:
            return None
        return None

    @staticmethod
    def _get_mute() -> bool | None:
        try:
            output = subprocess.run(
                ["amixer", "get", "Master"],
                capture_output=True,
                text=True,
                check=False,
            ).stdout
            for line in output.splitlines():
                if "[off]" in line:
                    return True
                if "[on]" in line:
                    return False
        except Exception:
            return None
        return None
