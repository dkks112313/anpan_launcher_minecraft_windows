import sys
from src import apps, check_hours_to_update
from PyQt6.QtWidgets import QApplication


def main():
    app = QApplication(sys.argv)
    window = apps.MainWindow()
    window.setFixedSize(700, 700)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
