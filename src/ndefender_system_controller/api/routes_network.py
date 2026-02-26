from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from ..core.supervisor import Supervisor
import uuid

from ..models import BluetoothDeviceList, BluetoothState, CommandResult, NetworkStatus, WifiScanResult, WifiState
from ..util.rate_limit import RateLimiter
from ..util.time import now_ms

router = APIRouter()
_command_rate = RateLimiter(limit=10, window_s=60)


class CommandRequest(BaseModel):
    payload: dict = {}
    confirm: bool = False


def get_supervisor(request: Request) -> Supervisor:
    return request.app.state.supervisor


@router.get("/network", response_model=NetworkStatus)
async def network_status(supervisor: Supervisor = Depends(get_supervisor)) -> NetworkStatus:
    snapshot = await supervisor.snapshot()
    return snapshot.network


@router.get("/network/wifi/state", response_model=WifiState)
async def wifi_state(supervisor: Supervisor = Depends(get_supervisor)) -> WifiState:
    return supervisor.network_manager().wifi_state()


@router.get("/network/wifi/scan", response_model=WifiScanResult)
async def wifi_scan(supervisor: Supervisor = Depends(get_supervisor)) -> WifiScanResult:
    return supervisor.network_manager().wifi_scan()


@router.get("/network/bluetooth/state", response_model=BluetoothState)
async def bluetooth_state(supervisor: Supervisor = Depends(get_supervisor)) -> BluetoothState:
    return supervisor.network_manager().bluetooth_state()


@router.get("/network/bluetooth/devices", response_model=BluetoothDeviceList)
async def bluetooth_devices(supervisor: Supervisor = Depends(get_supervisor)) -> BluetoothDeviceList:
    return supervisor.network_manager().bluetooth_devices()


@router.post("/network/wifi/enable", response_model=CommandResult)
async def wifi_enable(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    enabled = bool(body.payload.get("enabled"))
    ok = supervisor.network_manager().wifi_enable(enabled)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/wifi/enable",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/wifi/disable", response_model=CommandResult)
async def wifi_disable(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok = supervisor.network_manager().wifi_enable(False)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/wifi/disable",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/wifi/connect", response_model=CommandResult)
async def wifi_connect(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ssid = body.payload.get("ssid")
    password = body.payload.get("password")
    hidden = bool(body.payload.get("hidden", False))
    if not ssid:
        raise HTTPException(status_code=400, detail="invalid_payload")
    ok = supervisor.network_manager().wifi_connect(ssid, password, hidden)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/wifi/connect",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/wifi/disconnect", response_model=CommandResult)
async def wifi_disconnect(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok = supervisor.network_manager().wifi_disconnect()
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/wifi/disconnect",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/bluetooth/enable", response_model=CommandResult)
async def bluetooth_enable(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    enabled = bool(body.payload.get("enabled"))
    ok = supervisor.network_manager().bluetooth_enable(enabled)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/bluetooth/enable",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/bluetooth/disable", response_model=CommandResult)
async def bluetooth_disable(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok = supervisor.network_manager().bluetooth_enable(False)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/bluetooth/disable",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/bluetooth/scan/start", response_model=CommandResult)
async def bluetooth_scan_start(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok = supervisor.network_manager().bluetooth_scan(True)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/bluetooth/scan/start",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/bluetooth/scan/stop", response_model=CommandResult)
async def bluetooth_scan_stop(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    ok = supervisor.network_manager().bluetooth_scan(False)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/bluetooth/scan/stop",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/bluetooth/pair", response_model=CommandResult)
async def bluetooth_pair(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    addr = body.payload.get("addr")
    pin = body.payload.get("pin")
    if not addr:
        raise HTTPException(status_code=400, detail="invalid_payload")
    ok = supervisor.network_manager().bluetooth_pair(addr, pin)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/bluetooth/pair",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )


@router.post("/network/bluetooth/unpair", response_model=CommandResult)
async def bluetooth_unpair(body: CommandRequest, supervisor: Supervisor = Depends(get_supervisor)) -> CommandResult:
    if not _command_rate.allow():
        raise HTTPException(status_code=429, detail="rate_limited")
    addr = body.payload.get("addr")
    if not addr:
        raise HTTPException(status_code=400, detail="invalid_payload")
    ok = supervisor.network_manager().bluetooth_unpair(addr)
    if not ok:
        raise HTTPException(status_code=409, detail="invalid_state")
    return CommandResult(
        command="network/bluetooth/unpair",
        command_id=str(uuid.uuid4()),
        accepted=True,
        detail=None,
        timestamp_ms=now_ms(),
    )
