from mir4_auto_farm.features.farm import FarmCommands, FarmWorker
from mir4_auto_farm.features.instance import Instance
from mir4_auto_farm.infrastructure.input import WindowsWindowInput


def test_windows_farm_worker_cycle():
    instance = Instance(
        title="Mir4G[1]",
        pid=0,
    )

    input_controller = WindowsWindowInput(instance)

    commands = FarmCommands(input_controller)

    worker = FarmWorker(commands)

    worker._farm_cycle()
