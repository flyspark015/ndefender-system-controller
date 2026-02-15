#!/usr/bin/env python3
import json

from ndefender_system_controller.config import UpsConfig
from ndefender_system_controller.core.ups_hat_e import UpsHatE


def main() -> None:
    ups = UpsHatE(UpsConfig.from_env())
    status = ups.read_status()
    print(json.dumps(status.model_dump(), indent=2))


if __name__ == "__main__":
    main()
