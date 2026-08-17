from random import choice, randint, uniform
from time import sleep

from mir4_auto_farm.features.farm.commands import FarmCommands


class FarmWorker:
    def __init__(self, commands: FarmCommands):
        self.commands = commands
        self.ultimate = False
        self.stop = False

        self.possibilities = [
            round(uniform(1, 3), 3)
            for _ in range(10)
        ]

    def run(self, cycles: int | None = None) -> None:
        executed_cycles = 0

        while not self.stop:
            self._farm_cycle()

            executed_cycles += 1

            if cycles is not None and executed_cycles >= cycles:
                break

    def _farm_cycle(self) -> None:
        self.commands.target_screen()
        sleep(0.1)

        for _ in range(randint(2, 4)):
            self.commands.next_target()
            sleep(0.01)

        sleep(0.3)

        self.commands.basic_attack()

        self.commands.target_screen()
        sleep(choice(self.possibilities))

        if self.ultimate:
            self.commands.ultimate()