from ndefender_system_controller.util.rate_limit import Cooldown


def test_cooldown_allows_then_blocks():
    cd = Cooldown(interval_s=10)
    assert cd.allow() is True
    assert cd.allow() is False
