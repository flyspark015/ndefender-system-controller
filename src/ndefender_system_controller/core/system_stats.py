from ..models import SystemStats


class SystemStatsCollector:
    def read(self) -> SystemStats:
        return SystemStats()
