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


class InstanceRow(QFrame):
    def __init__(self, index: int, parent=None):
        super().__init__(parent)

        self.index = index

        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(self)

        self.instance_label = QLabel(f"MIR4G[{index}]")
        self.status_label = QLabel("Stopped")

        self.ultimate_button = QPushButton("Ultimate: OFF")
        self.ultimate_button.setCheckable(True)
        self.ultimate_button.toggled.connect(self.update_ultimate)

        self.stop_button = QPushButton("Stop")

        layout.addWidget(self.instance_label)
        layout.addStretch()
        layout.addWidget(self.status_label)
        layout.addWidget(self.ultimate_button)
        layout.addWidget(self.stop_button)

    def update_ultimate(self, enabled: bool):
        text = "Ultimate: ON" if enabled else "Ultimate: OFF"
        self.ultimate_button.setText(text)


class Canvas(QWidget):
    def __init__(self):
        super().__init__()

        self.instances = {}

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Instâncias")
        title.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        layout.addWidget(title)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.NoFrame)

        self.instance_container = QWidget()

        self.instance_layout = QVBoxLayout(
            self.instance_container
        )
        self.instance_layout.setAlignment(Qt.AlignTop)

        self.empty_label = QLabel("Nenhuma instância ativa")
        self.empty_label.setAlignment(Qt.AlignCenter)

        self.instance_layout.addWidget(self.empty_label)

        self.scroll.setWidget(self.instance_container)

        layout.addWidget(self.scroll)

    def add_instance(self, index: int):
        if index in self.instances:
            return

        if not self.instances:
            self.empty_label.hide()

        row = InstanceRow(index)

        self.instances[index] = row
        self.instance_layout.addWidget(row)

    def remove_instance(self, index: int):
        row = self.instances.pop(index, None)

        if row is None:
            return

        row.deleteLater()

        if not self.instances:
            self.empty_label.show()

    def clear_instances(self):
        for index in list(self.instances):
            self.remove_instance(index)