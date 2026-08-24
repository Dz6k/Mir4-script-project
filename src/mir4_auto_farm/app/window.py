from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from mir4_auto_farm.features.canvas import Canvas
from mir4_auto_farm.features.instance import (
    FarmInstance,
    Instance,
)
from mir4_auto_farm.features.manager import FarmManager
from mir4_auto_farm.infrastructure.input import (
    WindowsWindowInput,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MIR4 Auto Farm")

        self.setMinimumSize(
            700,
            500,
        )

        self.farm_manager = FarmManager()

        self.canvas = Canvas()

        self.setup_ui()

    def setup_ui(self):

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        layout.addWidget(self.canvas)

        controls = QHBoxLayout()

        self.instances_input = QLineEdit()
        self.instances_input.setPlaceholderText("Ex: 1, 3, 7")

        self.delay_input = QLineEdit()
        self.delay_input.setPlaceholderText("Delay ciclo (seg)")

        self.start_button = QPushButton("Add Instances")

        self.start_button.clicked.connect(self.create_instances)

        self.stop_all_button = QPushButton("Stop All")

        self.stop_all_button.clicked.connect(self.stop_all)

        controls.addWidget(QLabel("Instâncias:"))

        controls.addWidget(self.instances_input)

        controls.addWidget(QLabel("Delay:"))

        controls.addWidget(self.delay_input)

        controls.addWidget(self.start_button)

        controls.addWidget(self.stop_all_button)

        layout.addLayout(controls)

    def create_instances(self):

        text = self.instances_input.text().strip()

        if not text:
            return

        cycle_delay = 0

        delay_text = self.delay_input.text().strip()

        if delay_text:
            try:
                cycle_delay = float(delay_text)
            except ValueError:
                cycle_delay = 0

        for value in text.replace(",", " ").split():
            try:
                index = int(value)

            except ValueError:
                continue

            title = f"Mir4G[{index}]"

            instance = Instance(
                title=title,
                pid=0,
            )

            input_controller = WindowsWindowInput(instance)

            farm_instance = FarmInstance(
                instance,
                input_controller,
                cycle_delay=cycle_delay,
            )

            self.farm_manager.add(farm_instance)

            self.canvas.add_instance(farm_instance)

            self.farm_manager.start(title)

        self.instances_input.clear()

    def stop_all(self):

        self.farm_manager.stop_all()
