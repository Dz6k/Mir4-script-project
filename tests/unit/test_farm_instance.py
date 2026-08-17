from mir4_auto_farm.features.instance import Instance
from mir4_auto_farm.features.instance import FarmInstance
from mir4_auto_farm.infrastructure.input import InputController


class FakeInputController(InputController):
    def tap(self, key):
        pass


def test_farm_instance_creation():
    instance = Instance(
        title="Mir4G[0]",
        pid=0,
    )

    input_controller = FakeInputController(instance)

    farm = FarmInstance(
        instance=instance,
        input_controller=input_controller,
    )

    assert farm.instance == instance
    assert farm.ultimate is False
    assert farm.stopped is False

def test_farm_instance_ultimate():
    instance = Instance(
        title="Mir4G[0]",
        pid=0,
    )

    input_controller = FakeInputController(instance)

    farm = FarmInstance(instance, input_controller)

    farm.ultimate = True

    assert farm.ultimate is True

def test_farm_instance_stop():
    instance = Instance(
        title="Mir4G[0]",
        pid=0,
    )

    input_controller = FakeInputController(instance)

    farm = FarmInstance(instance, input_controller)

    farm.stop()

    assert farm.stopped is True