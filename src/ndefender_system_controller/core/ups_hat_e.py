from ..models import UpsStatus


class UpsHatE:
    def __init__(self) -> None:
        self._initialized = False

    def read_status(self) -> UpsStatus:
        if not self._initialized:
            return UpsStatus()
        return UpsStatus()
