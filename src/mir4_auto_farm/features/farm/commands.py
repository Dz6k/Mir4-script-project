from mir4_auto_farm.infrastructure.input import InputController
from mir4_auto_farm.infrastructure.input import Key


class FarmCommands:
    def __init__(self, input_controller: InputController):
        self.input = input_controller

    def basic_attack(self) -> None:
        self.input.key_press(Key.F)

    def target_screen(self) -> None:
        self.input.key_press(Key.TAB)

    def next_target(self) -> None:
        self.input.key_press(Key.PAGEUP)

    def ultimate(self) -> None:
        self.input.key_press(Key.R)