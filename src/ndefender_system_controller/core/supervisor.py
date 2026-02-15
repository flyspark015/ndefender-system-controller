import asyncio
import logging
from dataclasses import dataclass, field

from ..config import SchedulerConfig, UpsConfig
from ..models import (
    AudioStatus,
    NetworkStatus,
    ServiceStatus,
    StatusSnapshot,
    SystemStats,
    UpsStatus,
    WsEnvelope,
)
from ..util.time import now_ms
from .audio_mgr import AudioManager
from .network_mgr import NetworkManager
from .system_stats import SystemStatsCollector
from .systemd_mgr import SystemdManager
from .ups_hat_e import UpsHatE

logger = logging.getLogger(__name__)


@dataclass
class SupervisorState:
    system: SystemStats = field(default_factory=SystemStats)
    ups: UpsStatus = field(default_factory=UpsStatus)
    services: list[ServiceStatus] = field(default_factory=list)
    network: NetworkStatus = field(default_factory=NetworkStatus)
    audio: AudioStatus = field(default_factory=AudioStatus)


class Supervisor:
    def __init__(self, scheduler: SchedulerConfig, broadcaster: "WsBroadcaster") -> None:
        self._scheduler = scheduler
        self._broadcaster = broadcaster
        self._lock = asyncio.Lock()
        self._tasks: list[asyncio.Task] = []
        self._state = SupervisorState()
        self._system = SystemStatsCollector()
        self._ups = UpsHatE(UpsConfig.from_env())
        self._services = SystemdManager()
        self._network = NetworkManager()
        self._audio = AudioManager()
        self._running = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._tasks = [
            asyncio.create_task(self._poll_system_loop(), name="poll_system"),
            asyncio.create_task(self._poll_ups_loop(), name="poll_ups"),
            asyncio.create_task(self._poll_services_loop(), name="poll_services"),
            asyncio.create_task(self._poll_network_loop(), name="poll_network"),
            asyncio.create_task(self._poll_audio_loop(), name="poll_audio"),
        ]

    async def stop(self) -> None:
        if not self._running:
            return
        for task in self._tasks:
            task.cancel()
        await asyncio.gather(*self._tasks, return_exceptions=True)
        self._tasks = []
        self._running = False

    async def snapshot(self) -> StatusSnapshot:
        async with self._lock:
            return StatusSnapshot(
                timestamp_ms=now_ms(),
                system=self._state.system.model_copy(),
                ups=self._state.ups.model_copy(),
                services=[svc.model_copy() for svc in self._state.services],
                network=self._state.network.model_copy(),
                audio=self._state.audio.model_copy(),
            )

    async def _update_system(self, stats: SystemStats) -> None:
        async with self._lock:
            self._state.system = stats
        await self._broadcaster.broadcast(
            WsEnvelope(
                type="SYSTEM_STATUS",
                timestamp_ms=now_ms(),
                data=stats.model_dump(exclude_none=True),
            )
        )

    async def _update_ups(self, ups: UpsStatus) -> None:
        async with self._lock:
            self._state.ups = ups
        await self._broadcaster.broadcast(
            WsEnvelope(
                type="UPS_UPDATE",
                timestamp_ms=now_ms(),
                data=ups.model_dump(exclude_none=True),
            )
        )

    async def _update_services(self, services: list[ServiceStatus]) -> None:
        async with self._lock:
            self._state.services = services
        await self._broadcaster.broadcast(
            WsEnvelope(
                type="SERVICE_UPDATE",
                timestamp_ms=now_ms(),
                data={"services": [svc.model_dump(exclude_none=True) for svc in services]},
            )
        )

    async def _update_network(self, network: NetworkStatus) -> None:
        async with self._lock:
            self._state.network = network
        await self._broadcaster.broadcast(
            WsEnvelope(
                type="NETWORK_UPDATE",
                timestamp_ms=now_ms(),
                data=network.model_dump(exclude_none=True),
            )
        )

    async def _update_audio(self, audio: AudioStatus) -> None:
        async with self._lock:
            self._state.audio = audio
        await self._broadcaster.broadcast(
            WsEnvelope(
                type="AUDIO_UPDATE",
                timestamp_ms=now_ms(),
                data=audio.model_dump(exclude_none=True),
            )
        )

    async def _poll_system_loop(self) -> None:
        while True:
            try:
                await self._update_system(self._system.read())
            except Exception:
                logger.exception("System stats poll failed")
            await asyncio.sleep(self._scheduler.system_interval_s)

    async def _poll_ups_loop(self) -> None:
        while True:
            try:
                await self._update_ups(self._ups.read_status())
            except Exception:
                logger.exception("UPS poll failed")
            await asyncio.sleep(self._scheduler.ups_interval_s)

    async def _poll_services_loop(self) -> None:
        while True:
            try:
                await self._update_services(self._services.list_services())
            except Exception:
                logger.exception("Services poll failed")
            await asyncio.sleep(self._scheduler.services_interval_s)

    async def _poll_network_loop(self) -> None:
        while True:
            try:
                await self._update_network(self._network.status())
            except Exception:
                logger.exception("Network poll failed")
            await asyncio.sleep(self._scheduler.network_interval_s)

    async def _poll_audio_loop(self) -> None:
        while True:
            try:
                await self._update_audio(self._audio.status())
            except Exception:
                logger.exception("Audio poll failed")
            await asyncio.sleep(self._scheduler.audio_interval_s)


class WsBroadcaster:
    async def broadcast(self, envelope: WsEnvelope) -> None:  # pragma: no cover - interface
        raise NotImplementedError
