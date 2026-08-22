from mir4_auto_farm.features.farm import (
    FarmCommands,
    FarmWorker,
)
from mir4_auto_farm.infrastructure.input import (
    InputController,
)

from .models import Instance


class FarmInstance:
    def __init__(
        self,
        instance: Instance,
        input_controller: InputController,
        cycle_delay: float = 0,
    ):
        self.instance = instance
        self.commands = FarmCommands(input_controller)

        self.cycle_delay = cycle_delay

        self.worker = FarmWorker(
            self.commands,
            self.cycle_delay,
        )

    @property
    def ultimate(self) -> bool:
        return self.worker.ultimate

    @ultimate.setter
    def ultimate(
        self,
        enabled: bool,
    ) -> None:
        self.worker.ultimate = enabled

    @property
    def stopped(self) -> bool:
        return self.worker.stop_event.is_set()

    def start(self) -> None:
        if not self.worker.stop_event.is_set():
            return

        self.worker = FarmWorker(
            self.commands,
            self.cycle_delay,
        )

        self.worker.run()

    def run(self) -> None:
        self.worker.stop_event.clear()
        self.worker.run()

    def stop(self) -> None:
        self.worker.stop()
