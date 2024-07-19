import sys
import requests
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QProgressBar, QWidget


class DownloadThread(QThread):
    progress_changed = pyqtSignal(int)

    def __init__(self, url, filename):
        super().__init__()
        self.url = url
        self.filename = filename

    def run(self):
        response = requests.get(self.url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:
            with open(self.filename, 'wb') as f:
                f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            with open(self.filename, 'wb') as f:
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    self.progress_changed.emit(int(100 * dl / total_length))


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.download_thread = None
        self.setWindowTitle("Update")
        self.setFixedSize(400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        self.label = QLabel("Updating...")
        self.progress = QProgressBar()
        self.progress.setStyleSheet("""
                                QProgressBar {
                                    border: 2px solid grey;
                                    border-radius: 5px;
                                    text-align: center;
                                }
                                QProgressBar::chunk {
                                    background-color: #ffa500;
                                    width: 1px;
                                    margin: 0.5px;
                                }
                            """)
        self.progress.setValue(0)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        self.start_download()

    def start_download(self):
        REPO = "dkks112313/An-Pan-Launcher"
        ASSET_NAME = "An-Pan.Launcher.exe"

        response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
        release_data = response.json()

        asset_url = None
        for asset in release_data.get("assets", []):
            if asset["name"] == ASSET_NAME:
                asset_url = asset["browser_download_url"]
                break

        self.download_thread = DownloadThread(asset_url, ASSET_NAME)
        self.download_thread.progress_changed.connect(self.update_progress)
        self.download_thread.start()

    def update_progress(self, value):
        self.progress.setValue(value)
        if value == 100:
            self.label.setText("Update complete!")


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.setFixedSize(400, 100)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()