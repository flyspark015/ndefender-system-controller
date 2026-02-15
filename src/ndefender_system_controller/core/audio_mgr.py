import subprocess

from ..models import AudioStatus


class AudioManager:
    def status(self) -> AudioStatus:
        volume = self._get_volume()
        muted = self._get_mute()
        return AudioStatus(volume_percent=volume, muted=muted)

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
