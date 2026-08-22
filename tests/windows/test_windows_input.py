from mir4_auto_farm.features.instance import Instance
from mir4_auto_farm.infrastructure.input import Key, WindowsWindowInput


def test_send_f_to_mir4():
    instance = Instance(
        title="Mir4G[1]",
        pid=0,
    )

    input_controller = WindowsWindowInput(instance)

    input_controller.tap(Key.F)


def test_send_all_mir4_keys():
    instance = Instance(
        title="Mir4G[1]",
        pid=0,
    )

    input_controller = WindowsWindowInput(instance)

    input_controller.tap(Key.TAB)
    input_controller.tap(Key.PAGEUP)
    input_controller.tap(Key.R)