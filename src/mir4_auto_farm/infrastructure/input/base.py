from abc import ABC, abstractmethod


class InputController(ABC):
    @abstractmethod
    def key_down(self, key: int) -> None:
        pass

    @abstractmethod
    def key_up(self, key: int) -> None:
        pass

    def key_press(self, key: int) -> None:
        self.key_down(key)
        self.key_up(key)