from ..models import AudioStatus


class AudioManager:
    def status(self) -> AudioStatus:
        return AudioStatus()
