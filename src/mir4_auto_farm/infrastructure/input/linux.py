from evdev import UInput, ecodes

from mir4_auto_farm.infrastructure.input.base import InputController
from mir4_auto_farm.infrastructure.input.keys import Key


class LinuxInputController(InputController):
    KEY_MAP = {
        Key.F: ecodes.KEY_F,
        Key.TAB: ecodes.KEY_TAB,
        Key.PAGEUP: ecodes.KEY_PAGEUP,
        Key.R: ecodes.KEY_R,
    }

    def __init__(self):
        capabilities = {
            ecodes.EV_KEY: list(self.KEY_MAP.values()),
        }

        self.device = UInput(
            capabilities,
            name="MIR4 Auto Farm",
        )

    def key_down(self, key: Key) -> None:
        self.device.write(
            ecodes.EV_KEY,
            self.KEY_MAP[key],
            1,
        )
        self.device.syn()

    def key_up(self, key: Key) -> None:
        self.device.write(
            ecodes.EV_KEY,
            self.KEY_MAP[key],
            0,
        )
        self.device.syn()

    def close(self) -> None:
        self.device.close()