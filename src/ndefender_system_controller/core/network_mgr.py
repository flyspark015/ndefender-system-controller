import socket
import subprocess

from ..models import NetworkStatus


class NetworkManager:
    def status(self) -> NetworkStatus:
        ssid = self._read_ssid()
        ip_v4, ip_v6 = self._read_ips()
        return NetworkStatus(
            connected=bool(ssid) or bool(ip_v4) or bool(ip_v6),
            ssid=ssid,
            ip_v4=ip_v4,
            ip_v6=ip_v6,
        )

    @staticmethod
    def _read_ssid() -> str | None:
        try:
            output = subprocess.run(
                ["iwgetid", "-r"],
                capture_output=True,
                text=True,
                check=False,
                timeout=1,
            ).stdout.strip()
            return output or None
        except Exception:
            return None

    @staticmethod
    def _read_ips() -> tuple[str | None, str | None]:
        ip_v4 = None
        ip_v6 = None
        try:
            hostname = socket.gethostname()
            for info in socket.getaddrinfo(hostname, None):
                family, _, _, _, sockaddr = info
                if family == socket.AF_INET and ip_v4 is None:
                    ip_v4 = sockaddr[0]
                if family == socket.AF_INET6 and ip_v6 is None:
                    ip_v6 = sockaddr[0]
        except Exception:
            return None, None
        return ip_v4, ip_v6
