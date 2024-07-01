import sys
import app
from PyQt6.QtWidgets import QApplication


def main():
    apps = QApplication(sys.argv)
    w = app.MainWindow()
    w.show()
    sys.exit(apps.exec())


if __name__ == "__main__":
    main()
