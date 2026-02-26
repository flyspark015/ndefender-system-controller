import time
from collections import deque
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


class RateLimiter:
    def __init__(self, limit: int, window_s: float) -> None:
        self._limit = limit
        self._window_s = window_s
        self._hits: deque[float] = deque()

    def allow(self) -> bool:
        now = time.time()
        cutoff = now - self._window_s
        while self._hits and self._hits[0] < cutoff:
            self._hits.popleft()
        if len(self._hits) >= self._limit:
            return False
        self._hits.append(now)
        return True
