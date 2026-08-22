import re
import subprocess
from typing import ClassVar

from .base import InputController
from .keys import Key


class LinuxWindowInput(InputController):
    KEY_MAP: ClassVar[dict[Key, str]] = {
        Key.F: "f",
        Key.TAB: "Tab",
        Key.PAGEUP: "Page_Up",
        Key.R: "r",
    }

    def tap(self, key: Key) -> None:
        try:
            xdotool_key = self.KEY_MAP[key]
        except KeyError as exc:
            raise ValueError(f"Unsupported key: {key}") from exc

        window_id = self._find_window()

        subprocess.run(
            [
                "xdotool",
                "key",
                "--window",
                window_id,
                xdotool_key,
            ],
            check=True,
        )

    def _find_window(self) -> str:
        title_pattern = f"^{re.escape(self.instance.title)}$"

        result = subprocess.run(
            [
                "xdotool",
                "search",
                "--name",
                title_pattern,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        windows = result.stdout.strip().splitlines()

        if not windows:
            raise LookupError(f"Window not found: {self.instance.title}")

        if len(windows) > 1:
            raise RuntimeError(f"Multiple windows found: {self.instance.title}")

        return windows[0]
