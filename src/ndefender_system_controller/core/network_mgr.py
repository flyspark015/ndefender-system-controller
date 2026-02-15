from ..models import NetworkStatus


class NetworkManager:
    def status(self) -> NetworkStatus:
        return NetworkStatus()
