from mir4_auto_farm.features.farm import FarmCommands, FarmWorker
from .models import Instance
from mir4_auto_farm.infrastructure.input import InputController


class FarmInstance:
    def __init__(
        self,
        instance: Instance,
        input_controller: InputController,
    ):
        self.instance = instance
        self.commands = FarmCommands(input_controller)
        self.worker = FarmWorker(self.commands)

    @property
    def ultimate(self) -> bool:
        return self.worker.ultimate

    @ultimate.setter
    def ultimate(self, enabled: bool) -> None:
        self.worker.ultimate = enabled

    @property
    def stopped(self) -> bool:
        return self.worker.stop

    def run(self) -> None:
        self.worker.run()

    def stop(self) -> None:
        self.worker.stop = True