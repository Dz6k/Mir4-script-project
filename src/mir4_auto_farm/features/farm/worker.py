from random import choice, randint, uniform
from time import sleep

from .commands import FarmCommands


class FarmWorker:
    def __init__(self, commands: FarmCommands):
        self.commands = commands
        self.ultimate = False
        self.stop = False

        self.possibilities = [
            round(uniform(1, 3), 3)
            for _ in range(10)
        ]

    def run(self) -> None:
        while not self.stop:
            self._farm_cycle()

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