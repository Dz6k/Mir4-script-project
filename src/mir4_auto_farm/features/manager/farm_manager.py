class FarmManager:
    def __init__(self):
        self.instances = {}

    def add(self, farm_instance):
        title = farm_instance.instance.title
        self.instances[title] = farm_instance

    def start(self, title):
        self.instances[title].start()

    def stop(self, title):
        self.instances[title].stop()

    def stop_all(self):
        for instance in self.instances.values():
            instance.stop()

    def remove(self, title):
        instance = self.instances.pop(title, None)

        if instance:
            instance.stop()