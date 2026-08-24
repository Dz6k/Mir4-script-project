import json
import subprocess

from mir4_auto_farm.features.instance import Instance

from .base import WindowDiscovery


class HyprlandWindowDiscovery(WindowDiscovery):
    def find_by_title(self, title: str) -> Instance:
        clients = self._get_clients()

        for client in clients:
            if client.get("title") != title:
                continue

            pid = client.get("pid")
            address = client.get("address")

            if pid is None or address is None:
                raise RuntimeError(
                    f"Window '{title}' was found, "
                    "but its PID or address is unavailable."
                )

            return Instance(
                title=title,
                pid=pid,
                window_id=address,
            )

        raise LookupError(f"Window not found: {title}")

    @staticmethod
    def _get_clients() -> list[dict]:
        result = subprocess.run(
            ["hyprctl", "-j", "clients"],
            capture_output=True,
            text=True,
            check=True,
        )

        try:
            return json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Hyprland returned invalid client data.") from exc
