from random import choice, randint, uniform
from threading import Event

from .commands import FarmCommands


class FarmWorker:
    def __init__(
        self,
        commands: FarmCommands,
        cycle_delay: float = 0,
    ):
        self.commands = commands
        self.ultimate = False
        self.stop_event = Event()

        # Randomização humana dos tempos internos
        self.possibilities = [round(uniform(1, 3), 3) for _ in range(10)]

        # Delay fixo configurado pelo usuário
        self.cycle_delay = cycle_delay

    def run(self) -> None:
        while not self.stop_event.is_set():
            self._farm_cycle()

    def _farm_cycle(self) -> None:
        self.commands.target_screen()
        self._sleep(0.1)

        for _ in range(randint(2, 4)):
            self.commands.next_target()
            self._sleep(0.01)

        self._sleep(0.3)

        self.commands.basic_attack()

        self.commands.target_screen()

        # comportamento humano aleatório
        self._sleep(choice(self.possibilities))

        if self.ultimate:
            self.commands.ultimate()

        # delay fixo entre ciclos
        if self.cycle_delay > 0:
            self._sleep(self.cycle_delay)

    def stop(self) -> None:
        self.stop_event.set()

    def _sleep(self, seconds: float) -> None:
        self.stop_event.wait(seconds)
