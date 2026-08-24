from mir4_auto_farm.features.farm import FarmCommands, FarmWorker
from mir4_auto_farm.features.instance import Instance
from mir4_auto_farm.infrastructure.input import LinuxWindowInput


def test_farm_worker():
    instance = Instance(
        title="Mir4G[0]",
        pid=0,
    )

    input_controller = LinuxWindowInput(instance)
    commands = FarmCommands(input_controller)
    worker = FarmWorker(commands)

    worker.stop = True

    worker._farm_cycle()
