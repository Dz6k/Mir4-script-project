from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from mir4_auto_farm.features.instance import FarmInstance


class InstanceRow(QFrame):
    def __init__(
        self,
        farm_instance: FarmInstance,
        show_help: bool = False,
        parent=None,
    ):
        super().__init__(parent)

        self.farm_instance = farm_instance

        self.setFrameShape(QFrame.StyledPanel)

        layout = QHBoxLayout(self)

        self.instance_label = QLabel(farm_instance.instance.title)

        self.status_label = QLabel("Stopped")

        self.delay_input = QLineEdit(
            str(farm_instance.cycle_delay)
        )
        self.delay_input.setFixedWidth(70)
        self.delay_input.returnPressed.connect(
            self.update_cycle_delay
        )

        self.help_label = QLabel("?")
        self.help_label.setStyleSheet("""
            QLabel {
                border: 1px solid gray;
                border-radius: 10px;
                padding: 0px 5px;
                font-weight: bold
            }
        """)

        self.help_label.setToolTip(
            "Delay do ciclo:\n"
            "Define o tempo de espera entre os ciclos de agro.\n"
            "Pressione Enter para aplicar."
        )

        self.help_label

        self.help_label.setVisible(show_help)

        self.ultimate_button = QPushButton("Ultimate: OFF")

        self.ultimate_button.setCheckable(True)
        self.ultimate_button.toggled.connect(self.toggle_ultimate)

        self.farm_button = QPushButton("Agro: OFF")
        self.farm_button.setCheckable(True)
        self.farm_button.toggled.connect(self.toggle_running)

        self.remove_button = QPushButton("×")
        self.remove_button.setFixedWidth(30)

        layout.addWidget(self.instance_label)

        layout.addStretch()

        layout.addWidget(self.status_label)

        layout.addWidget(self.delay_input)

        layout.addWidget(self.help_label)

        layout.addWidget(self.ultimate_button)

        layout.addWidget(self.farm_button)

        layout.addWidget(self.remove_button)

    def toggle_ultimate(self, enabled: bool,):
        self.farm_instance.ultimate = enabled
        self.ultimate_button.setText("Ultimate: ON" if enabled else "Ultimate: OFF")

    def update_cycle_delay(self):
        try:
            value = float(self.delay_input.text())
        except ValueError:
            self.delay_input.setText(
                str(self.farm_instance.cycle_delay)
            )
            return

        if value < 0:
            self.delay_input.setText(
                str(self.farm_instance.cycle_delay)
            )
            return

        self.farm_instance.cycle_delay = value
        self.delay_input.setText(
            str(self.farm_instance.cycle_delay)
        )
    
    def toggle_running(self, enabled: bool):
        if enabled:
            self.farm_instance.start()
        else:
            self.farm_instance.stop()

        self.update_status()

    def update_status(self):
        if self.farm_instance.running:
            self.status_label.setText("Running")
            self.farm_button.setText("Agro: ON")
        else:
            self.status_label.setText("Stopped")
            self.farm_button.setText("Agro: OFF")


class Canvas(QWidget):
    
    def __init__(self):
        super().__init__()
        
        from mir4_auto_farm.features.manager.farm_manager import FarmManager

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

        row = InstanceRow(farm_instance, show_help=not self.instances,)

        row.remove_button.clicked.connect(
            lambda: self.remove_instance(title)
        )

        self.instances[title] = row

        self.farm_manager.add(farm_instance)

        self.instance_layout.addWidget(row)

    def remove_instance(self, title: str):
        self.farm_manager.remove(title)

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
