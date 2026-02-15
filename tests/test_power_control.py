from ndefender_system_controller.config import AppConfig
from ndefender_system_controller.core.power_control import PowerController


def test_power_control_blocks_when_unsafe_disabled():
    controller = PowerController(AppConfig(allow_unsafe=False))
    ok, reason = controller.reboot()
    assert ok is False
    assert reason == "unsafe_disabled"
