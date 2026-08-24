from typing import ClassVar

import win32con
import win32gui

from .base import InputController
from .keys import Key


class WindowsWindowInput(InputController):
    KEY_MAP: ClassVar[dict[Key, str]] = {
        Key.F: ord("F"),
        Key.TAB: win32con.VK_TAB,
        Key.PAGEUP: win32con.VK_PRIOR,
        Key.R: ord("R"),
    }

    def tap(self, key: Key) -> None:
        window = self._find_window()

        key_code = self.KEY_MAP[key]

        win32gui.PostMessage(
            window,
            win32con.WM_KEYDOWN,
            key_code,
            0,
        )

        win32gui.PostMessage(
            window,
            win32con.WM_KEYUP,
            key_code,
            0,
        )

    def _find_window(self) -> int:
        window = win32gui.FindWindow(
            None,
            self.instance.title,
        )

        if not window:
            raise RuntimeError(f"Window not found: {self.instance.title}")

        return window
