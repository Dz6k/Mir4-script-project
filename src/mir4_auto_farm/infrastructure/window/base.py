from abc import ABC, abstractmethod

from mir4_auto_farm.features.instance import Instance


class WindowDiscovery(ABC):
    @abstractmethod
    def find_by_title(self, title: str) -> Instance:
        """Find a window by its title."""
        raise NotImplementedError
