import sys

from .base import InputController
from .keys import Key
from .linux import LinuxWindowInput

__all__ = [
    "InputController",
    "LinuxWindowInput",
    "Key",
    ]

if sys.platform == "win32":
    from .windows import WindowsWindowInput

    __all__.append("WindowsWindowInput")