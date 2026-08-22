from threading import Event

from mir4_auto_farm.features.manager import FarmManager


class FakeFarmInstance:
    def __init__(self, title: str):
        self.instance = type(
            "Instance",
            (),
            {"title": title},
        )()

        self.running = False
        self.started = 0
        self.stopped = False
        self.running_event = Event()

    def run(self):
        self.running = True
        self.started += 1

        self.running_event.wait()

    def stop(self):
        self.stopped = True
        self.running_event.set()


def test_add_farm_instance():
    manager = FarmManager()

    farm = FakeFarmInstance("Mir4G[1]")

    manager.add(farm)

    assert manager.get("Mir4G[1]") == farm


def test_start_farm_instance():
    manager = FarmManager()

    farm = FakeFarmInstance("Mir4G[1]")

    manager.add(farm)

    manager.start("Mir4G[1]")

    assert farm.running is True


def test_stop_farm_instance():
    manager = FarmManager()

    farm = FakeFarmInstance("Mir4G[1]")

    manager.add(farm)

    manager.stop("Mir4G[1]")

    assert farm.stopped is True


def test_stop_all_farm_instances():
    manager = FarmManager()

    farm_one = FakeFarmInstance("Mir4G[1]")
    farm_two = FakeFarmInstance("Mir4G[2]")

    manager.add(farm_one)
    manager.add(farm_two)

    manager.stop_all()

    assert farm_one.stopped is True
    assert farm_two.stopped is True


def test_farm_manager_restart():
    manager = FarmManager()

    farm = FakeFarmInstance("Mir4G[0]")

    manager.add(farm)

    manager.start("Mir4G[0]")

    assert farm.started == 1

    manager.stop("Mir4G[0]")

    manager.threads["Mir4G[0]"].join(timeout=1)

    manager.start("Mir4G[0]")

    assert farm.started == 2

    manager.stop("Mir4G[0]")