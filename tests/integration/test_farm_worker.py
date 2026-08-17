from mir4_auto_farm.features.farm.commands import FarmCommands
from mir4_auto_farm.features.farm.worker import FarmWorker
from mir4_auto_farm.infrastructure.input.linux import LinuxInputController


WINDOW_INDEX = 0
CYCLES = 3


def test_farm_worker():
    input_controller = LinuxInputController()
    commands = FarmCommands(input_controller)
    worker = FarmWorker(commands)

    try:
        worker.run(cycles=CYCLES)
    finally:
        input_controller.close()