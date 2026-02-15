import logging
import time
from dataclasses import dataclass

from smbus2 import SMBus

from ..config import UpsConfig
from ..models import UpsStatus

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class UpsRaw:
    status: int
    vbus: list[int]
    battery: list[int]
    cells: list[int]


class UpsHatE:
    def __init__(self, config: UpsConfig) -> None:
        self._config = config
        self._bus: SMBus | None = None
        self._last_keepalive_ts = 0.0

    def read_status(self) -> UpsStatus:
        try:
            raw = self._read_raw()
            if raw is None:
                return UpsStatus()
            return self.decode(raw)
        except Exception:
            logger.exception("UPS read failed")
            return UpsStatus()

    def _read_raw(self) -> UpsRaw | None:
        bus = self._ensure_bus()
        if bus is None:
            return None
        self._keepalive_if_needed(bus)
        status = self._read_block(bus, 0x02, 0x01)[0]
        vbus = self._read_block(bus, 0x10, 0x06)
        battery = self._read_block(bus, 0x20, 0x0C)
        cells = self._read_block(bus, 0x30, 0x08)
        return UpsRaw(status=status, vbus=vbus, battery=battery, cells=cells)

    def _ensure_bus(self) -> SMBus | None:
        if self._bus is not None:
            return self._bus
        try:
            self._bus = SMBus(self._config.i2c_bus)
            return self._bus
        except Exception:
            logger.exception("Failed to open I2C bus %s", self._config.i2c_bus)
            return None

    def _keepalive_if_needed(self, bus: SMBus) -> None:
        now = time.time()
        if now - self._last_keepalive_ts < self._config.keepalive_interval_s:
            return
        try:
            bus.write_byte_data(self._config.i2c_addr, 0x01, 0x55)
            self._last_keepalive_ts = now
        except Exception:
            logger.exception("UPS keepalive write failed")

    def _read_block(self, bus: SMBus, register: int, length: int) -> list[int]:
        return bus.read_i2c_block_data(self._config.i2c_addr, register, length)

    @staticmethod
    def decode(raw: UpsRaw) -> UpsStatus:
        state = UpsHatE._decode_state(raw.status)
        vbus_mv = UpsHatE._u16(raw.vbus, 0)
        vbus_mw = UpsHatE._u16(raw.vbus, 4)

        batt_mv = UpsHatE._u16(raw.battery, 0)
        current_ma = UpsHatE._s16(raw.battery, 2)
        soc_percent = UpsHatE._u16(raw.battery, 4)
        tte_min = UpsHatE._u16(raw.battery, 8)
        ttf_min = UpsHatE._u16(raw.battery, 10)

        cell_vs = [
            UpsHatE._u16(raw.cells, 0),
            UpsHatE._u16(raw.cells, 2),
            UpsHatE._u16(raw.cells, 4),
            UpsHatE._u16(raw.cells, 6),
        ]

        time_to_empty_s = int(tte_min * 60) if current_ma < 0 else None
        time_to_full_s = int(ttf_min * 60) if current_ma >= 0 else None

        return UpsStatus(
            pack_voltage_v=UpsHatE._mv_to_v(batt_mv),
            current_a=UpsHatE._ma_to_a(current_ma),
            input_vbus_v=UpsHatE._mv_to_v(vbus_mv),
            input_power_w=UpsHatE._mw_to_w(vbus_mw),
            soc_percent=UpsHatE._clamp_percent(soc_percent),
            time_to_empty_s=time_to_empty_s,
            time_to_full_s=time_to_full_s,
            per_cell_v=[UpsHatE._mv_to_v(v) for v in cell_vs],
            state=state,
        )

    @staticmethod
    def _decode_state(status_byte: int) -> str:
        if status_byte & 0x40:
            return "FAST_CHARGING"
        if status_byte & 0x80:
            return "CHARGING"
        if status_byte & 0x20:
            return "DISCHARGING"
        return "IDLE"

    @staticmethod
    def _u16(data: list[int], offset: int) -> int:
        return data[offset] | (data[offset + 1] << 8)

    @staticmethod
    def _s16(data: list[int], offset: int) -> int:
        value = UpsHatE._u16(data, offset)
        if value & 0x8000:
            value -= 0x10000
        return value

    @staticmethod
    def _mv_to_v(value_mv: int) -> float:
        return round(value_mv / 1000.0, 3)

    @staticmethod
    def _ma_to_a(value_ma: int) -> float:
        return round(value_ma / 1000.0, 3)

    @staticmethod
    def _mw_to_w(value_mw: int) -> float:
        return round(value_mw / 1000.0, 3)

    @staticmethod
    def _clamp_percent(value: int) -> int:
        if value < 0:
            return 0
        if value > 100:
            return 100
        return value
