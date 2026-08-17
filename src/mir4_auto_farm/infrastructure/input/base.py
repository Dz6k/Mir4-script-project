from abc import ABC, abstractmethod

from mir4_auto_farm.features.instance import Instance
from .keys import Key


class InputController(ABC):
    def __init__(self, instance: Instance):
        self.instance = instance

    @abstractmethod
    def tap(self, key: Key) -> None:
        """Send a key event to the instance."""
        raise NotImplementedError