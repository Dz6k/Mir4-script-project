from mir4_auto_farm.features.farm import FarmCommands, FarmWorker


class FakeFarmCommands(FarmCommands):
    def __init__(self):
        self.calls = []

    def target_screen(self):
        self.calls.append("target_screen")

    def next_target(self):
        self.calls.append("next_target")

    def basic_attack(self):
        self.calls.append("basic_attack")

    def ultimate(self):
        self.calls.append("ultimate")


def test_farm_worker_cycle(monkeypatch):
    commands = FakeFarmCommands()
    worker = FarmWorker(commands)

    monkeypatch.setattr(
        "mir4_auto_farm.features.farm.worker.sleep",
        lambda _: None,
    )

    worker._farm_cycle()

    assert commands.calls[0] == "target_screen"
    assert commands.calls[-2] == "basic_attack"
    assert commands.calls[-1] == "target_screen"

    next_target_calls = commands.calls.count("next_target")

    assert 2 <= next_target_calls <= 4


def test_farm_worker_cycle_with_ultimate(monkeypatch):
    commands = FakeFarmCommands()
    worker = FarmWorker(commands)

    worker.ultimate = True

    monkeypatch.setattr(
        "mir4_auto_farm.features.farm.worker.sleep",
        lambda _: None,
    )

    worker._farm_cycle()

    assert commands.calls[-1] == "ultimate"