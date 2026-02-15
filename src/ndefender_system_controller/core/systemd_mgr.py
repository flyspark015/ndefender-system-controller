import subprocess

from ..models import ServiceStatus


class SystemdManager:
    def __init__(self, services: list[str] | None = None) -> None:
        self._services = services or []

    def list_services(self) -> list[ServiceStatus]:
        services = self._services or self._discover_services()
        result: list[ServiceStatus] = []
        for name in services:
            status = self._read_status(name)
            if status:
                result.append(status)
        return result

    def restart(self, name: str) -> bool:
        try:
            subprocess.run(["systemctl", "restart", name], check=True)
            return True
        except Exception:
            return False

    def _discover_services(self) -> list[str]:
        # Fallback: no configured services
        return []

    def _read_status(self, name: str) -> ServiceStatus | None:
        try:
            output = subprocess.run(
                [
                    "systemctl",
                    "show",
                    name,
                    "-p",
                    "ActiveState",
                    "-p",
                    "SubState",
                    "-p",
                    "NRestarts",
                ],
                capture_output=True,
                text=True,
                check=False,
            ).stdout
            values = dict(
                line.split("=", 1)
                for line in output.strip().splitlines()
                if "=" in line
            )
            return ServiceStatus(
                name=name,
                active_state=values.get("ActiveState", "unknown"),
                sub_state=values.get("SubState", "unknown"),
                restart_count=int(values.get("NRestarts", "0") or 0),
            )
        except Exception:
            return None
