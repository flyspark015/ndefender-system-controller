import time
from dataclasses import dataclass


@dataclass
class Cooldown:
    interval_s: float
    _last_ts: float = 0.0

    def allow(self) -> bool:
        now = time.time()
        if now - self._last_ts >= self.interval_s:
            self._last_ts = now
            return True
        return False
