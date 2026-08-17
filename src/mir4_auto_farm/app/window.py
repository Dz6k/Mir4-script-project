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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MIR4 Auto Farm")
        self.setMinimumSize(700, 500)

        self.canvas = Canvas()

        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        layout.addWidget(self.canvas)

        controls = QHBoxLayout()

        self.instances_input = QLineEdit()
        self.instances_input.setPlaceholderText("Ex: 0, 3, 7")

        self.start_button = QPushButton("Start Manual")
        self.start_button.clicked.connect(self.start_manual)

        self.stop_all_button = QPushButton("Stop All")
        self.stop_all_button.clicked.connect(self.stop_all)

        controls.addWidget(QLabel("Instâncias:"))
        controls.addWidget(self.instances_input)
        controls.addWidget(self.start_button)
        controls.addWidget(self.stop_all_button)

        layout.addLayout(controls)

    def start_manual(self):
        text = self.instances_input.text().strip()

        if not text:
            return

        for value in text.replace(",", " ").split():
            try:
                index = int(value)
            except ValueError:
                continue

            self.canvas.add_instance(index)

        self.instances_input.clear()

    def stop_all(self):
        self.canvas.clear_instances()