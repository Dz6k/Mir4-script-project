from threading import Thread

from mir4_auto_farm.features.instance import FarmInstance


class FarmManager:
    def __init__(self):
        self.instances: dict[str, FarmInstance] = {}
        self.threads: dict[str, Thread] = {}

    def add(
        self,
        farm_instance: FarmInstance,
    ) -> None:
        title = farm_instance.instance.title

        self.instances[title] = farm_instance

    def start(
        self,
        title: str,
    ) -> None:
        farm_instance = self.instances[title]

        current_thread = self.threads.get(title)

        if current_thread and current_thread.is_alive():
            return

        thread = Thread(
            target=farm_instance.run,
            daemon=True,
        )

        self.threads[title] = thread

        thread.start()

    def stop(
        self,
        title: str,
    ) -> None:

        farm_instance = self.instances[title]

        farm_instance.stop()

        thread = self.threads.get(title)

        if thread:
            thread.join(timeout=1)

    def stop_all(self) -> None:
        for farm_instance in self.instances.values():
            farm_instance.stop()

    def get(
        self,
        title: str,
    ) -> FarmInstance:
        return self.instances[title]
