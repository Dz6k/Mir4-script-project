import sys

from PySide6.QtWidgets import QApplication

from mir4_auto_farm.app import MainWindow


def main():
    app = QApplication(sys.argv)

    app.setStyleSheet("""
        QToolTip {
            background-color: #fffde7;
            border: 1px solid #000000;
        }
    """)


    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
