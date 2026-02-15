from ndefender_system_controller.core.ups_hat_e import UpsHatE, UpsRaw


def test_ups_decode_sample():
    raw = UpsRaw(
        status=0x20,
        vbus=[0x88, 0x13, 0xD0, 0x07, 0x10, 0x27],
        battery=[0xD0, 0x39, 0x24, 0xFA, 0x50, 0x00, 0xA0, 0x0F, 0x0C, 0x00, 0x00, 0x00],
        cells=[0x74, 0x0E, 0x7E, 0x0E, 0x6A, 0x0E, 0x88, 0x0E],
    )
    status = UpsHatE.decode(raw)
    assert status.state == "DISCHARGING"
    assert status.pack_voltage_v == 14.8
    assert status.current_a == -1.5
    assert status.input_vbus_v == 5.0
    assert status.input_power_w == 10.0
    assert status.soc_percent == 80
    assert status.time_to_empty_s == 720
    assert status.time_to_full_s is None
    assert status.per_cell_v == [3.7, 3.71, 3.69, 3.72]
