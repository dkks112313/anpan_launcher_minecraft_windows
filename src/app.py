import configparser
import os
import subprocess

import minecraft_launcher_lib
from PyQt6.QtCore import QSettings, Qt
from PyQt6.QtGui import QIntValidator, QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, \
    QCheckBox, QFileDialog, QProgressBar, QMessageBox

from src import request, regex
from src.env import *
from src.random_tablet import random_image
from src.thread_launch import Launcher


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.progress_bar = None
        self.img_label = None
        self.img_pixmap = None
        self.image_layout = None
        self.jvm_box = QLineEdit()
        self.git_checkbox = QCheckBox()
        self.warning_checkbox = QCheckBox()
        self.console_checkbox = QCheckBox()
        self.main_interface_layout = None
        self.data_checkbox = QCheckBox()
        self.alpha_checkbox = QCheckBox()
        self.snapshot_checkbox = QCheckBox()
        self.path_box = QLineEdit()
        self.path_box.setReadOnly(True)
        self.settings_button = QPushButton("Settings")
        self.launch_button = QPushButton("Launch")
        self.version_select = QComboBox()
        self.username_edit = QLineEdit()
        self.launcher = Launcher()
        self.ram_box = QLineEdit()
        validator = QIntValidator()
        self.ram_box.setValidator(validator)

        self.settings = QSettings("MyApp", "App")

        self.setWindowTitle("An-Pan Launcher")
        self.setWindowIcon(QIcon("icon.ico"))

        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        self.main_interface = QWidget()
        self.settings_interface = QWidget()

        self.main_layout.addWidget(self.main_interface)
        self.main_layout.addWidget(self.settings_interface)

        self.ui_init()

    def ui_init(self):
        self.main_interface_layout = QVBoxLayout()
        self.main_interface.setLayout(self.main_interface_layout)

        self.username_edit = QLineEdit()
        self.version_select = QComboBox()
        self.launch_button = QPushButton("Launch")
        self.settings_button = QPushButton("Settings")

        self.launch_button.clicked.connect(self.launch_minecraft)
        self.settings_button.clicked.connect(self.show_settings)

        self.launcher.state_signal.connect(self.state_progress)
        self.launcher.progress_signal.connect(self.update_progress)

        self.snapshot_checkbox.stateChanged.connect(self.update_version_list)
        self.alpha_checkbox.stateChanged.connect(self.update_version_list)

        self.load_settings()

        self.update_version_list()

        self.image_layout = QHBoxLayout()

        self.img_pixmap = QPixmap(random_image())

        self.img_label = QLabel()
        self.img_label.setPixmap(self.img_pixmap)
        self.image_layout.addWidget(self.img_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setProperty("value", 0)

        self.progress_bar.setStyleSheet("""
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

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Version:"))
        bottom_layout.addWidget(self.version_select)
        bottom_layout.addWidget(self.launch_button)
        bottom_layout.addWidget(self.settings_button)

        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Username:"))
        user_layout.addWidget(self.username_edit)

        self.main_interface_layout.addStretch(1)
        self.main_interface_layout.addLayout(self.image_layout)
        self.main_interface_layout.addWidget(self.progress_bar)
        self.main_interface_layout.addLayout(user_layout)
        self.main_interface_layout.addLayout(bottom_layout)

        self.load_settings()

        self.username_edit.textChanged.connect(self.save_settings)
        self.version_select.currentTextChanged.connect(self.save_settings)

        self.main_interface.setVisible(True)
        self.settings_interface.setVisible(False)

        self.init_settings_interface()

        if self.git_checkbox.isChecked():
            self.update_message()

    def update_version_list(self):
        self.version_select.clear()
        alpha = self.alpha_checkbox.isChecked()
        snapshot = self.snapshot_checkbox.isChecked()

        if alpha and snapshot:
            for version_info in minecraft_launcher_lib.utils.get_version_list():
                self.version_select.addItem(version_info["id"])
        elif alpha:
            for version_info in minecraft_launcher_lib.utils.get_version_list():
                if version_info['type'] in ['old_alpha', 'old_beta', 'release']:
                    self.version_select.addItem(version_info['id'])
        elif snapshot:
            for version_info in minecraft_launcher_lib.utils.get_version_list():
                if version_info['type'] in ['snapshot', 'release']:
                    self.version_select.addItem(version_info['id'])
        else:
            for version_info in minecraft_launcher_lib.utils.get_version_list():
                if version_info['type'] in ['release']:
                    self.version_select.addItem(version_info["id"])

    def init_settings_interface(self):
        settings_layout = QVBoxLayout()

        path = QHBoxLayout()
        path_label = QLabel("Path")
        path_choice = QPushButton("Choice")
        path_choice.clicked.connect(self.select_directory)
        default_button = QPushButton("Default")
        default_button.clicked.connect(self.default_directory)
        path.addWidget(path_label)
        path.addWidget(self.path_box)
        path.addWidget(path_choice)
        path.addWidget(default_button)

        ram = QHBoxLayout()
        ram_slider_label = QLabel(f"RAM(mb): ")
        ram.addWidget(ram_slider_label)
        ram.addWidget(self.ram_box)

        jvm = QHBoxLayout()
        jvm_label = QLabel("JVM")
        jvm.addWidget(jvm_label)
        jvm.addWidget(self.jvm_box)

        git = QHBoxLayout()
        git_lable = QLabel("Auto Update")
        git.addWidget(git_lable)
        git.addWidget(self.git_checkbox)

        warning = QHBoxLayout()
        warning_label = QLabel("Warning")
        warning.addWidget(warning_label)
        warning.addWidget(self.warning_checkbox)

        console = QHBoxLayout()
        console_label = QLabel("Console")
        console.addWidget(console_label)
        console.addWidget(self.console_checkbox)

        snapshot = QHBoxLayout()
        snapshot_label = QLabel("Snapshot")
        snapshot.addWidget(snapshot_label)
        snapshot.addWidget(self.snapshot_checkbox)

        alpha = QHBoxLayout()
        alpha_label = QLabel("Alpha")
        alpha.addWidget(alpha_label)
        alpha.addWidget(self.alpha_checkbox)

        data = QHBoxLayout()
        data_label = QLabel("Data")
        data.addWidget(data_label)
        data.addWidget(self.data_checkbox)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main)

        settings_layout.addStretch(1)
        settings_layout.addLayout(path)
        settings_layout.addLayout(ram)
        settings_layout.addLayout(jvm)
        settings_layout.addLayout(git)
        settings_layout.addLayout(warning)
        settings_layout.addLayout(console)
        settings_layout.addLayout(snapshot)
        settings_layout.addLayout(alpha)
        settings_layout.addLayout(data)
        settings_layout.addWidget(back_button)

        self.settings_interface.setLayout(settings_layout)

        self.path_box.textChanged.connect(self.save_settings)
        self.ram_box.textChanged.connect(self.save_settings)
        self.snapshot_checkbox.stateChanged.connect(self.save_settings)
        self.alpha_checkbox.stateChanged.connect(self.save_settings)
        self.data_checkbox.stateChanged.connect(self.save_settings)
        self.console_checkbox.stateChanged.connect(self.save_settings)
        self.git_checkbox.stateChanged.connect(self.save_settings)
        self.warning_checkbox.stateChanged.connect(self.save_settings)
        self.jvm_box.textChanged.connect(self.save_settings)

    def update_message(self):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setText("You want to update?")
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        res = self.msgBox.exec()
        if res == QMessageBox.StandardButton.Ok:
            subprocess.call('update.exe')
            self.close()
        self.msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.msgBox.show()

    def show_message(self, user_message):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setText(user_message)
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.msgBox.show()

    def show_settings(self):
        self.load_settings()
        self.main_interface.setVisible(False)
        self.settings_interface.setVisible(True)

    def show_main(self):
        self.save_settings()
        self.main_interface.setVisible(True)
        self.settings_interface.setVisible(False)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.path_box.setText(directory)

    def default_directory(self):
        os.makedirs(os.path.join(os.getenv('APPDATA'), '.launch'), exist_ok=True)
        settings['minecraft_directory'] = os.path.join(os.getenv('APPDATA'), '.launch')
        self.path_box.setText(settings['minecraft_directory'])

    def load_settings(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.username_edit.setText(self.settings.value("username", config["CONFIG"]["username"]))
        self.version_select.setCurrentText(self.settings.value("version", config["CONFIG"]["version"]))
        self.ram_box.setText(self.settings.value("ram", config["CONFIG"]["ram"]))
        self.snapshot_checkbox.setChecked(self.settings.value("snapshot_checkbox", config["CONFIG"]["snapshot"]) == "True")
        self.alpha_checkbox.setChecked(self.settings.value("alpha_checkbox", config["CONFIG"]["alpha"]) == "True")
        if config['CONFIG']['directory'] == "":
            self.path_box.setText(self.settings.value("directory", os.path.join(os.getenv('APPDATA'), '.launch')))
        else:
            self.path_box.setText(self.settings.value("directory", config['CONFIG']['directory']))
        self.console_checkbox.setChecked(self.settings.value("console_checkbox", config["CONFIG"]["console"]) == "True")
        self.git_checkbox.setChecked(self.settings.value("update_git", config["CONFIG"]["git"]) == "True")
        self.warning_checkbox.setChecked(self.settings.value("warning_checkbox", "False") == "True")
        self.data_checkbox.setChecked(self.settings.value("data_checkbox", config["CONFIG"]["data"]) == "True")
        self.jvm_box.setText(self.settings.value("jvm_box", config["CONFIG"]["jvm"]))

    def save_settings(self):
        self.settings.setValue("username", self.username_edit.text())
        self.settings.setValue("version", self.version_select.currentText())
        self.settings.setValue("ram", self.ram_box.text())
        self.settings.setValue("snapshot_checkbox", "True" if self.snapshot_checkbox.isChecked() else "False")
        self.settings.setValue("alpha_checkbox", "True" if self.alpha_checkbox.isChecked() else "False")
        self.settings.setValue("directory", self.path_box.text())
        self.settings.setValue("console_checkbox", "True" if self.console_checkbox.isChecked() else "False")
        self.settings.setValue("update_git", "True" if self.git_checkbox.isChecked() else "False")
        self.settings.setValue("warning_checkbox", "True" if self.warning_checkbox.isChecked() else "False")
        self.settings.setValue("data_checkbox", "True" if self.data_checkbox.isChecked() else "False")
        self.settings.setValue("jvm_box", self.jvm_box.text())

    def save_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config["CONFIG"]["username"] = self.username_edit.text()
        config["CONFIG"]["version"] = self.version_select.currentText()
        config["CONFIG"]["ram"] = self.ram_box.text()
        config["CONFIG"]["snapshot"] = str(self.snapshot_checkbox.isChecked())
        config["CONFIG"]["alpha"] = str(self.alpha_checkbox.isChecked())
        config["CONFIG"]["directory"] = self.path_box.text()
        config["CONFIG"]["console"] = str(self.console_checkbox.isChecked())
        config["CONFIG"]["git"] = str(self.git_checkbox.isChecked())
        config["CONFIG"]["data"] = str(self.data_checkbox.isChecked())
        config["CONFIG"]["jvm"] = self.jvm_box.text()

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def closeEvent(self, event):
        self.save_config()
        request.on_close()
        event.accept()

    def state_progress(self, value):
        if self.launcher.status:
            self.show_message("Minecraft is installed and ready to launch")
            self.launcher.status = False
        self.launch_button.setDisabled(value)
        self.progress_bar.setVisible(not value)

    def update_progress(self, progress, max_progress):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(progress)
        self.progress_bar.setMaximum(max_progress)

    def launch_minecraft(self):
        settings['version'] = self.version_select.currentText()
        options["username"] = self.username_edit.text()

        if not regex.check_to_latin_alphabet(options["username"]) and self.warning_checkbox.isChecked():
            self.show_message("Your name contains symbols that may interfere with your future game")
            self.settings.setValue("warning_checkbox", "False")

        if self.path_box.text() != os.path.join(os.getenv('APPDATA'), '.launch'):
            settings['minecraft_directory'] = self.path_box.text()
        else:
            settings['minecraft_directory'] = os.path.join(os.getenv('APPDATA'), '.launch')

        if self.jvm_box.text():
            for arg in self.jvm_box.text().split(" "):
                options['jvmArguments'].append(arg)

        ram = int(self.ram_box.text())
        options['jvmArguments'].append(f'-Xmx{ram}M')

        settings['console'] = self.console_checkbox.isChecked()
        settings['alpha'] = self.alpha_checkbox.isChecked()
        settings['snapshot'] = self.snapshot_checkbox.isChecked()
        settings['data'] = self.data_checkbox.isChecked()
        settings['git'] = self.git_checkbox.isChecked()

        self.launcher.start()
