from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from mir4_auto_farm.features.instance import FarmInstance
from mir4_auto_farm.features.manager import FarmManager


class InstanceRow(QFrame):
    def __init__(
        self,
        farm_instance: FarmInstance,
        parent=None,
    ):
        super().__init__(parent)

        self.farm_instance = farm_instance

        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(self)

        self.instance_label = QLabel(farm_instance.instance.title)

        self.status_label = QLabel("Stopped")

        self.ultimate_button = QPushButton("Ultimate: OFF")

        self.ultimate_button.setCheckable(True)
        self.ultimate_button.toggled.connect(self.toggle_ultimate)

        self.start_button = QPushButton("Start")

        self.stop_button = QPushButton("Stop")

        layout.addWidget(self.instance_label)

        layout.addStretch()

        layout.addWidget(self.status_label)

        layout.addWidget(self.ultimate_button)

        layout.addWidget(self.start_button)

        layout.addWidget(self.stop_button)

    def toggle_ultimate(
        self,
        enabled: bool,
    ):
        self.farm_instance.ultimate = enabled

        self.ultimate_button.setText("Ultimate: ON" if enabled else "Ultimate: OFF")


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.farm_manager = FarmManager()

        self.instances: dict[str, InstanceRow] = {}

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout(self)

        title = QLabel("Instâncias")

        title.setStyleSheet("font-size: 18px; font-weight: bold;")

        layout.addWidget(title)

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(True)

        self.scroll.setFrameShape(QFrame.NoFrame)

        self.instance_container = QWidget()

        self.instance_layout = QVBoxLayout(self.instance_container)

        self.instance_layout.setAlignment(Qt.AlignTop)

        self.empty_label = QLabel("Nenhuma instância ativa")

        self.empty_label.setAlignment(Qt.AlignCenter)

        self.instance_layout.addWidget(self.empty_label)

        self.scroll.setWidget(self.instance_container)

        layout.addWidget(self.scroll)

    def add_instance(
        self,
        farm_instance: FarmInstance,
    ):

        title = farm_instance.instance.title

        if title in self.instances:
            return

        if not self.instances:
            self.empty_label.hide()

        row = InstanceRow(farm_instance)

        row.start_button.clicked.connect(lambda: self.start_instance(title))

        row.stop_button.clicked.connect(lambda: self.stop_instance(title))

        self.instances[title] = row

        self.farm_manager.add(farm_instance)

        self.instance_layout.addWidget(row)

    def start_instance(
        self,
        title: str,
    ):

        self.farm_manager.start(title)

        row = self.instances[title]

        row.status_label.setText("Running")

    def stop_instance(
        self,
        title: str,
    ):

        self.farm_manager.stop(title)

        row = self.instances[title]

        row.status_label.setText("Stopped")

    def remove_instance(
        self,
        title: str,
    ):

        row = self.instances.pop(
            title,
            None,
        )

        if row is None:
            return

        row.deleteLater()

        if not self.instances:
            self.empty_label.show()

    def clear_instances(self):

        self.farm_manager.stop_all()

        for title in list(self.instances):
            self.remove_instance(title)
