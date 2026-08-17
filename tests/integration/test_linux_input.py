from time import sleep

from mir4_auto_farm.features.farm import FarmCommands
from mir4_auto_farm.infrastructure.input import Key
from mir4_auto_farm.infrastructure.input import LinuxInputController


def test_linux_input_f():
    controller = LinuxInputController()

    try:
        sleep(1)

        controller.key_down(Key.F)
        sleep(0.1)
        controller.key_up(Key.F)

        sleep(1)
    finally:
        controller.close()

def test_linux_farm_commands():
    controller = LinuxInputController()
    commands = FarmCommands(controller)

    try:
        sleep(1)

        commands.basic_attack()

        sleep(1)
    finally:
        controller.close()