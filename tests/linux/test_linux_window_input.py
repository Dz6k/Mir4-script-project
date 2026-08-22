from mir4_auto_farm.features.instance import Instance
from mir4_auto_farm.infrastructure.input import Key
from mir4_auto_farm.infrastructure.input import LinuxWindowInput


def test_send_f_to_mir4():
    instance = Instance(
        title="Mir4G[0]",
        pid=0,
    )

    input_controller = LinuxWindowInput(instance)

    input_controller.tap(Key.F)