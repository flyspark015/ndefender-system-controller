import subprocess

from ..config import AppConfig


class PowerController:
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def reboot(self) -> tuple[bool, str]:
        if not self._config.allow_unsafe:
            return False, "unsafe_disabled"
        return self._run(["systemctl", "reboot"])

    def shutdown(self) -> tuple[bool, str]:
        if not self._config.allow_unsafe:
            return False, "unsafe_disabled"
        return self._run(["systemctl", "poweroff"])

    @staticmethod
    def _run(cmd: list[str]) -> tuple[bool, str]:
        try:
            subprocess.run(cmd, check=True)
            return True, "ok"
        except Exception:
            return False, "failed"
