from mir4_auto_farm.features.farm import (
    FarmCommands,
    FarmWorker,
)
from mir4_auto_farm.infrastructure.input import (
    InputController,
)

from .models import Instance

from threading import Thread


class FarmInstance:
    def __init__(
        self,
        instance: Instance,
        input_controller: InputController,
        cycle_delay: float = 0,
    ):
        self.instance = instance
        self.commands = FarmCommands(input_controller)
        self._cycle_delay = cycle_delay

        self.worker = FarmWorker(
            self.commands,
            self._cycle_delay,
        )

        self.thread: Thread | None = None

    @property
    def cycle_delay(self) -> float:
        return self._cycle_delay

    @cycle_delay.setter
    def cycle_delay(self, value: float) -> None:
        self._cycle_delay = value
        self.worker.cycle_delay = value

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
    def running(self) -> bool:
        return bool( self.thread and self.thread.is_alive())

    @property
    def stopped(self) -> bool:
        return self.worker.stop_event.is_set()

    def run(self) -> None:
        self.worker.run()

    def start(self):
        if self.running:
            return

        self.worker = FarmWorker(
            self.commands,
            self.cycle_delay,
        )

        self.thread = Thread(
            target=self.worker.run,
            daemon=True,
        )

        self.thread.start()

    def stop(self):
        self.worker.stop()

        if self.thread:
            self.thread.join(timeout=1)
            self.thread = None
