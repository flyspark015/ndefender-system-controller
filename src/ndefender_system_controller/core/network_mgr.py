import socket
import subprocess
import shutil

from ..models import BluetoothDeviceList, BluetoothState, NetworkStatus, WifiScanResult, WifiState
from ..util.time import now_ms


class NetworkManager:
    def status(self) -> NetworkStatus:
        ssid = self._read_ssid()
        ip_v4, ip_v6 = self._read_ips()
        return NetworkStatus(
            connected=bool(ssid) or bool(ip_v4) or bool(ip_v6),
            ssid=ssid,
            ip_v4=ip_v4,
            ip_v6=ip_v6,
            wifi=self.wifi_state(),
            bluetooth=self.bluetooth_state(),
        )

    def wifi_state(self) -> WifiState:
        timestamp_ms = now_ms()
        if not shutil.which("nmcli"):
            return WifiState(
                timestamp_ms=timestamp_ms,
                enabled=None,
                connected=False,
                last_update_ms=timestamp_ms,
                last_error="nmcli_not_found",
            )
        enabled = None
        connected = False
        ssid = None
        bssid = None
        rssi_dbm = None
        ip = None
        try:
            output = subprocess.run(
                ["nmcli", "-t", "-f", "WIFI", "g"],
                capture_output=True,
                text=True,
                check=False,
                timeout=2,
            ).stdout.strip()
            if output:
                enabled = output.strip().lower() == "enabled"
        except Exception:
            pass
        try:
            lines = subprocess.run(
                ["nmcli", "-t", "-f", "ACTIVE,SSID,BSSID,SIGNAL", "dev", "wifi"],
                capture_output=True,
                text=True,
                check=False,
                timeout=2,
            ).stdout.strip().splitlines()
            for line in lines:
                parts = line.split(":")
                if len(parts) < 4:
                    continue
                active = parts[0] == "yes"
                if active:
                    connected = True
                    ssid = parts[1] or None
                    bssid = parts[2] or None
                    try:
                        rssi_dbm = int(parts[3]) - 100
                    except Exception:
                        rssi_dbm = None
                    break
        except Exception:
            pass
        ip_v4, _ = self._read_ips()
        ip = ip_v4
        return WifiState(
            timestamp_ms=timestamp_ms,
            enabled=enabled,
            connected=connected,
            ssid=ssid,
            bssid=bssid,
            ip=ip,
            rssi_dbm=rssi_dbm,
            last_update_ms=timestamp_ms,
        )

    def wifi_scan(self) -> WifiScanResult:
        timestamp_ms = now_ms()
        networks: list[dict] = []
        if not shutil.which("nmcli"):
            return WifiScanResult(timestamp_ms=timestamp_ms, networks=[], last_error="nmcli_not_found")
        try:
            output = subprocess.run(
                ["nmcli", "-t", "-f", "SSID,BSSID,SECURITY,SIGNAL,CHAN,FREQ", "dev", "wifi", "list"],
                capture_output=True,
                text=True,
                check=False,
                timeout=4,
            ).stdout.strip()
            for line in output.splitlines():
                ssid, bssid, security, signal, chan, freq = (line.split(":") + [None] * 6)[:6]
                entry = {
                    "ssid": ssid or None,
                    "bssid": bssid or None,
                    "security": security or None,
                }
                if signal and signal.isdigit():
                    entry["signal_dbm"] = int(signal) - 100
                if chan and chan.isdigit():
                    entry["channel"] = int(chan)
                if freq and freq.isdigit():
                    entry["frequency_mhz"] = int(freq)
                networks.append(entry)
        except Exception:
            return WifiScanResult(timestamp_ms=timestamp_ms, networks=[], last_error="wifi_scan_failed")
        return WifiScanResult(timestamp_ms=timestamp_ms, networks=networks)

    def bluetooth_state(self) -> BluetoothState:
        timestamp_ms = now_ms()
        if not shutil.which("bluetoothctl"):
            return BluetoothState(
                timestamp_ms=timestamp_ms,
                enabled=None,
                scanning=None,
                paired_count=0,
                connected_devices=[],
                last_update_ms=timestamp_ms,
                last_error="bluetoothctl_not_found",
            )
        enabled = None
        scanning = None
        try:
            output = subprocess.run(
                ["bluetoothctl", "show"],
                capture_output=True,
                text=True,
                check=False,
                timeout=3,
            ).stdout
            for line in output.splitlines():
                if "Powered:" in line:
                    enabled = line.split(":", 1)[1].strip().lower() == "yes"
                if "Discovering:" in line:
                    scanning = line.split(":", 1)[1].strip().lower() == "yes"
        except Exception:
            pass
        paired = self._bluetooth_paired()
        connected = self._bluetooth_connected()
        return BluetoothState(
            timestamp_ms=timestamp_ms,
            enabled=enabled,
            scanning=scanning,
            paired_count=len(paired),
            connected_devices=connected,
            last_update_ms=timestamp_ms,
        )

    def bluetooth_devices(self) -> BluetoothDeviceList:
        timestamp_ms = now_ms()
        devices = []
        if not shutil.which("bluetoothctl"):
            return BluetoothDeviceList(timestamp_ms=timestamp_ms, devices=[])
        paired = {d["addr"]: d for d in self._bluetooth_paired()}
        connected_addrs = {d["addr"] for d in self._bluetooth_connected()}
        for addr, entry in paired.items():
            devices.append(
                {
                    "addr": addr,
                    "name": entry.get("name"),
                    "paired": True,
                    "connected": addr in connected_addrs,
                }
            )
        return BluetoothDeviceList(timestamp_ms=timestamp_ms, devices=devices)

    def wifi_enable(self, enabled: bool) -> bool:
        if not shutil.which("nmcli"):
            return False
        subprocess.run(["nmcli", "radio", "wifi", "on" if enabled else "off"], check=False)
        return True

    def wifi_connect(self, ssid: str, password: str | None, hidden: bool = False) -> bool:
        if not shutil.which("nmcli"):
            return False
        cmd = ["nmcli", "dev", "wifi", "connect", ssid]
        if password:
            cmd += ["password", password]
        if hidden:
            cmd += ["hidden", "yes"]
        subprocess.run(cmd, check=False)
        return True

    def wifi_disconnect(self) -> bool:
        if not shutil.which("nmcli"):
            return False
        subprocess.run(["nmcli", "dev", "disconnect", "wlan0"], check=False)
        return True

    def bluetooth_enable(self, enabled: bool) -> bool:
        if not shutil.which("bluetoothctl"):
            return False
        subprocess.run(["bluetoothctl", "power", "on" if enabled else "off"], check=False)
        return True

    def bluetooth_scan(self, enabled: bool) -> bool:
        if not shutil.which("bluetoothctl"):
            return False
        subprocess.run(["bluetoothctl", "scan", "on" if enabled else "off"], check=False)
        return True

    def bluetooth_pair(self, addr: str, pin: str | None = None) -> bool:
        if not shutil.which("bluetoothctl"):
            return False
        subprocess.run(["bluetoothctl", "pair", addr], check=False)
        return True

    def bluetooth_unpair(self, addr: str) -> bool:
        if not shutil.which("bluetoothctl"):
            return False
        subprocess.run(["bluetoothctl", "remove", addr], check=False)
        return True

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

    @staticmethod
    def _bluetooth_paired() -> list[dict]:
        devices: list[dict] = []
        try:
            output = subprocess.run(
                ["bluetoothctl", "paired-devices"],
                capture_output=True,
                text=True,
                check=False,
                timeout=3,
            ).stdout
            for line in output.splitlines():
                if line.startswith("Device"):
                    _, addr, *name = line.split()
                    devices.append({"addr": addr, "name": " ".join(name)})
        except Exception:
            pass
        return devices

    @staticmethod
    def _bluetooth_connected() -> list[dict]:
        devices: list[dict] = []
        try:
            output = subprocess.run(
                ["bluetoothctl", "devices", "Connected"],
                capture_output=True,
                text=True,
                check=False,
                timeout=3,
            ).stdout
            for line in output.splitlines():
                if line.startswith("Device"):
                    _, addr, *name = line.split()
                    devices.append({"addr": addr, "name": " ".join(name)})
        except Exception:
            pass
        return devices
