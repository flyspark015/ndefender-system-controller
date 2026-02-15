import time

from ndefender_system_controller.util.rate_limit import Cooldown


def test_cooldown_allows_then_blocks():
    cd = Cooldown(interval_s=10)
    assert cd.allow() is True
    assert cd.allow() is False


def test_cooldown_allows_after_interval():
    cd = Cooldown(interval_s=0.01)
    assert cd.allow() is True
    assert cd.allow() is False
    time.sleep(0.02)
    assert cd.allow() is True
