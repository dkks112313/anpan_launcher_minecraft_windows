import sys
from PyQt6.QtGui import QIcon
from src import app
from PyQt6.QtWidgets import QApplication


def main():
    apps = QApplication(sys.argv)
    window = app.MainWindow()
    window.setWindowIcon(QIcon("icon.ico"))
    window.setFixedSize(700, 700)
    window.show()
    sys.exit(apps.exec())


if __name__ == "__main__":
    main()
