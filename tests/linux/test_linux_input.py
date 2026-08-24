from mir4_auto_farm.features.farm import FarmCommands
from mir4_auto_farm.features.instance import Instance
from mir4_auto_farm.infrastructure.input import Key, LinuxWindowInput


def get_instance() -> Instance:
    return Instance(
        title="Mir4G[0]",
        pid=0,
    )


def test_linux_input_f():
    instance = get_instance()

    controller = LinuxWindowInput(instance)

    controller.tap(Key.F)


def test_linux_farm_commands():
    instance = get_instance()

    controller = LinuxWindowInput(instance)
    commands = FarmCommands(controller)

    commands.basic_attack()
