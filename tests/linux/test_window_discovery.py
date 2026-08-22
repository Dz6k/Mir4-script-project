from mir4_auto_farm.infrastructure.window import (
    HyprlandWindowDiscovery,
)


def test_find_mir4_window():
    discovery = HyprlandWindowDiscovery()

    instance = discovery.find_by_title("Mir4G[0]")

    assert instance.title == "Mir4G[0]"
    assert instance.pid > 0
    assert instance.window_id

    print(f"\nInstance found: {instance}")