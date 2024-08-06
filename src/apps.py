import configparser
import os
import subprocess
import sys
import time
import minecraft_launcher_lib
import json

import requests
from packaging import version
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QIntValidator, QPixmap, QIcon
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QHBoxLayout, QVBoxLayout, \
    QCheckBox, QFileDialog, QProgressBar, QMessageBox, QSlider

from src import request, regex, git_work, file_work, status, configer
from src.env import *
from src.random_image import random_image2
from src.thread_launch import Launcher


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        configer.checker_config_params_to_exist()
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.language_select = QComboBox()
        self.language_select.addItems(["English", "Ukraine"])
        self.settings_button = None
        self.launch_button = None
        self.progress_bar = None
        self.img_label = None
        self.img_pixmap = None
        self.image_layout = None
        self.save_count = None

        self.ram_slider = QSlider(Qt.Orientation.Horizontal)
        self.ram_slider.setMinimum(2)
        #self.ram_slider.setMaximum(ram_user.ram_size() * 10)
        self.ram_slider.setMaximum(16 * 10)
        self.ram_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.ram_slider.setTickInterval(1)

        self.main_interface_layout = None
        self.jvm_box = QLineEdit()
        self.git_checkbox = QCheckBox()
        self.warning_checkbox = QCheckBox()
        self.console_checkbox = QCheckBox()
        self.data_checkbox = QCheckBox()
        self.alpha_checkbox = QCheckBox()
        self.snapshot_checkbox = QCheckBox()
        self.path_box = QLineEdit()
        self.path_box.setReadOnly(True)
        self.java_box = QLineEdit()
        self.java_box.setReadOnly(True)
        self.version_select = QComboBox()
        self.choice_mod = QComboBox()
        self.choice_mod.addItems(["Vanilla", "Forge", "Fabric", "Qulit"])
        self.username_edit = QLineEdit()
        self.exit_checkbox = QCheckBox()
        self.launcher = Launcher()
        self.ram_box = QLineEdit()
        validator = QIntValidator()
        self.ram_box.setValidator(validator)

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

        if status.check_internet_connection():
            settings['status'] = True
        else:
            settings['status'] = False

        self.launch_button = QPushButton("Launch")
        self.settings_button = QPushButton("Settings")

        self.progress_bar = QProgressBar()
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setVisible(False)

        self.launch_button.clicked.connect(self.launch_minecraft)
        self.settings_button.clicked.connect(self.show_settings)

        self.launcher.state_signal.connect(self.state_progress)
        self.launcher.progress_signal.connect(self.update_progress)

        self.snapshot_checkbox.stateChanged.connect(self.update_version_list)
        self.alpha_checkbox.stateChanged.connect(self.update_version_list)
        self.choice_mod.currentTextChanged.connect(self.update_version_list)

        self.load_settings()

        self.update_version_list()

        self.image_layout = QHBoxLayout()

        if os.path.isdir('content'):
            self.img_pixmap = QPixmap(random_image2())

            self.img_label = QLabel()
            self.img_label.setPixmap(self.img_pixmap)
            self.image_layout.addWidget(self.img_label, alignment=Qt.AlignmentFlag.AlignCenter)
            self.main_interface_layout.addLayout(self.image_layout)
        else:
            os.mkdir('content')

        self.progress_bar.setStyleSheet("""
            QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}
            QProgressBar::chunk {background-color: #ffa500;width: 1px;margin: 0.5px;}
        """)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Version:"))
        bottom_layout.addWidget(self.version_select)
        bottom_layout.addWidget(self.choice_mod)
        bottom_layout.addWidget(self.launch_button)
        bottom_layout.addWidget(self.settings_button)

        user_layout = QHBoxLayout()
        user_layout.addWidget(QLabel("Username:"))
        user_layout.addWidget(self.username_edit)

        self.main_interface_layout.addStretch(1)
        self.main_interface_layout.addWidget(self.progress_bar)
        self.main_interface_layout.addLayout(user_layout)
        self.main_interface_layout.addLayout(bottom_layout)

        self.load_settings()

        self.username_edit.textChanged.connect(self.save_settings)
        self.version_select.currentTextChanged.connect(self.save_settings)
        self.choice_mod.currentTextChanged.connect(self.save_settings)

        self.main_interface.setVisible(True)
        self.settings_interface.setVisible(False)

        self.init_settings_interface()

        config = configparser.ConfigParser()
        config.read("config.ini")

        try:
            check = git_work.get_latest_version()

            if self.git_checkbox.isChecked() and config["CONFIG"]["version_id"] != check:
                self.save_count = config["CONFIG"]["version_id"]
                config["CONFIG"]["version_id"] = check

                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

                self.update_message()
        except Exception:
            pass

    def update_version_list(self):
        self.version_select.clear()
        alpha = self.alpha_checkbox.isChecked()
        snapshot = self.snapshot_checkbox.isChecked()

        file_work.check_version_list()

        if status.check_internet_connection():
            if self.choice_mod.currentText() == "Vanilla":
                with open('version_vanilla.json', 'r', encoding='utf-8') as file_vanilla:
                    vanilla = json.load(file_vanilla)h

                if alpha and snapshot:
                    for version_info in vanilla:
                        self.version_select.addItem(version_info["id"])
                elif alpha:
                    for version_info in vanilla:
                        if version_info['type'] in ['old_alpha', 'old_beta', 'release']:
                            self.version_select.addItem(version_info['id'])
                elif snapshot:
                    for version_info in vanilla:
                        if version_info['type'] in ['snapshot', 'release']:
                            self.version_select.addItem(version_info['id'])
                else:
                    for version_info in vanilla:
                        if version_info['type'] in ['release']:
                            self.version_select.addItem(version_info["id"])
            elif self.choice_mod.currentText() == "Forge":
                with open('version_forge.json', 'r', encoding='utf-8') as file_forge:
                    forges = json.load(file_forge)

                for version_info in forges:
                    self.version_select.addItem(version_info)
            elif self.choice_mod.currentText() == "Fabric":
                with open('version_fabric.json', 'r', encoding='utf-8') as file_fabric:
                    fabrics = json.load(file_fabric)

                if snapshot:
                    for version_info in fabrics:
                        if minecraft_launcher_lib.fabric.is_minecraft_version_supported(version_info['version']):
                            self.version_select.addItem(version_info['version'])
                else:
                    for version_info in fabrics:
                        if minecraft_launcher_lib.fabric.is_minecraft_version_supported(version_info['version']) and version_info['stable']:
                            self.version_select.addItem(version_info['version'])
            elif self.choice_mod.currentText() == "Qulit":
                with open('version_qulit.json', 'r', encoding='utf-8') as file_qulit:
                    qulits = json.load(file_qulit)

                if snapshot:
                    for version_info in qulits:
                        if minecraft_launcher_lib.quilt.is_minecraft_version_supported(version_info['version']):
                            self.version_select.addItem(version_info['version'])
                else:
                    for version_info in qulits:
                        if minecraft_launcher_lib.quilt.is_minecraft_version_supported(version_info['version']) and version_info['stable']:
                            self.version_select.addItem(version_info['version'])
        else:
            for version_item in file_work.get_version_list():
                self.version_select.addItem(version_item)

    def init_settings_interface(self):
        settings_layout = QVBoxLayout()

        path = QHBoxLayout()
        path_label = QLabel("Path")
        path_choice = QPushButton("Choice")
        path_choice.clicked.connect(self.select_directory)
        default_button = QPushButton("Default")
        default_button.clicked.connect(self.default_directory)
        open_version_path = QPushButton("Open")
        open_version_path.clicked.connect(self.open_directory)
        path.addWidget(path_label)
        path.addWidget(self.path_box)
        path.addWidget(path_choice)
        path.addWidget(default_button)
        path.addWidget(open_version_path)

        java = QHBoxLayout()
        java_label = QLabel("Java")
        java_choice = QPushButton("Choice")
        java_choice.clicked.connect(self.select_java)
        java_default = QPushButton("Default")
        java_default.clicked.connect(self.default_java)
        java.addWidget(java_label)
        java.addWidget(self.java_box)
        java.addWidget(java_choice)
        java.addWidget(java_default)

        ram = QHBoxLayout()
        ram_slider_label = QLabel(f"RAM(mb): ")
        ram.addWidget(ram_slider_label)
        ram.addWidget(self.ram_slider)
        ram.addWidget(self.ram_box)

        '''labels_ram_layout = QHBoxLayout()

        for i in range(2, ram_user.ram_size() + 1):
            label = QLabel(str(i))
            labels_ram_layout.addWidget(label)
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)'''

        self.ram_slider.valueChanged.connect(self.update_line_edit)
        self.ram_box.textChanged.connect(self.update_slider)

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

        exit_launcher = QHBoxLayout()
        exit_label = QLabel("Exit")
        exit_launcher.addWidget(exit_label)
        exit_launcher.addWidget(self.exit_checkbox)

        language = QHBoxLayout()
        language_label = QLabel("Language")
        language.addWidget(language_label)
        language.addWidget(self.language_select)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main)

        settings_layout.addStretch(1)
        settings_layout.addLayout(path)
        settings_layout.addLayout(java)
        settings_layout.addLayout(ram)
        settings_layout.addLayout(jvm)
        settings_layout.addLayout(language)
        settings_layout.addLayout(git)
        settings_layout.addLayout(warning)
        settings_layout.addLayout(console)
        settings_layout.addLayout(snapshot)
        settings_layout.addLayout(alpha)
        settings_layout.addLayout(data)
        settings_layout.addLayout(exit_launcher)
        settings_layout.addWidget(back_button)

        self.settings_interface.setLayout(settings_layout)

    def update_line_edit(self, value):
        self.ram_box.blockSignals(True)
        self.ram_box.setText(str(value * 100))
        self.ram_box.blockSignals(False)

    def update_slider(self, text):
        if text.isdigit():
            value = int(text) // 100
            self.ram_slider.blockSignals(True)
            self.ram_slider.setValue(value)
            self.ram_slider.blockSignals(False)

    def run_update(self):
        process = QProcess(self)
        process.startDetached("update.exe")
        sys.exit()

    def update_message(self):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setText("You want to update?")
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
        self.msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)

        res = self.msgBox.exec()
        if res == QMessageBox.StandardButton.Cancel:
            config = configparser.ConfigParser()
            config.read('config.ini')
            config["CONFIG"]["version_id"] = self.save_count

            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        elif res == QMessageBox.StandardButton.Ok:
            self.run_update()

    def warning_message(self, user_message):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setText(user_message)
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        button_adapt = self.msgBox.button(QMessageBox.StandardButton.Ok)
        button_adapt.setText("Change username")
        self.msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.msgBox.exec()

    def show_message(self, user_message):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setText(user_message)
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.msgBox.exec()

    def show_launch_message(self, user_message):
        self.msgBox = QMessageBox(self)
        self.msgBox.setIcon(QMessageBox.Icon.Information)
        self.msgBox.setText(user_message)
        self.msgBox.setWindowTitle("Message")
        self.msgBox.setStandardButtons(QMessageBox.StandardButton.Ok)
        self.msgBox.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.msgBox.buttonClicked.connect(self.on_message_box_close)
        self.msgBox.exec()

    def on_message_box_close(self):
        self.launcher.release_wait()

    def show_settings(self):
        self.load_settings()
        self.save_settings()
        self.main_interface.setVisible(False)
        self.settings_interface.setVisible(True)

    def show_main(self):
        self.save_settings()
        self.load_settings()
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

    def select_java(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.java_box.setText(directory)

    def default_java(self):
        self.java_box.setText("")

    def open_directory(self):
        if os.path.isdir(self.path_box.text() + '\\' + self.version_select.currentText()):
            subprocess.Popen("explorer " + self.path_box.text() + '\\' + self.version_select.currentText(), creationflags=subprocess.CREATE_NO_WINDOW)
        else:
            self.show_message("Directory not exist")

    def load_settings(self):
        configer.create_or_no_new_config()
        config = configparser.ConfigParser()
        config.read('config.ini')
        configer.checker_config_params_to_exist()

        self.username_edit.setText(config["CONFIG"]["username"])
        self.version_select.setCurrentText(config["CONFIG"]["version"])
        self.ram_box.setText(config["CONFIG"]["ram"])
        self.snapshot_checkbox.setChecked(config["CONFIG"]["snapshot"] == "True")
        self.alpha_checkbox.setChecked(config["CONFIG"]["alpha"] == "True")
        self.choice_mod.setCurrentText(config["CONFIG"]["mode"])
        if config['CONFIG']['directory'] == "":
            self.path_box.setText(os.path.join(os.getenv('APPDATA'), '.launch'))
        else:
            self.path_box.setText(config['CONFIG']['directory'])
        self.java_box.setText(config['CONFIG']['java'])
        self.console_checkbox.setChecked(config["CONFIG"]["console"] == "True")
        self.git_checkbox.setChecked(config["CONFIG"]["git"] == "True")
        self.warning_checkbox.setChecked(config["CONFIG"]["warning"] == "True")
        self.data_checkbox.setChecked(config["CONFIG"]["data"] == "True")
        self.jvm_box.setText(config["CONFIG"]["jvm"])
        self.exit_checkbox.setChecked(config["CONFIG"]["exit"] == "True")
        self.language_select.setCurrentText(config["CONFIG"]["lang"])

    def save_settings(self):
        configer.create_or_no_new_config()

        config = configparser.ConfigParser()
        config.read('config.ini')
        configer.checker_config_params_to_exist()

        config["CONFIG"]["username"] = self.username_edit.text()
        config["CONFIG"]["version"] = self.version_select.currentText()
        config["CONFIG"]["ram"] = self.ram_box.text()
        config["CONFIG"]["snapshot"] = "True" if self.snapshot_checkbox.isChecked() else "False"
        config["CONFIG"]["alpha"] = "True" if self.alpha_checkbox.isChecked() else "False"
        config["CONFIG"]["mode"] = self.choice_mod.currentText()
        config['CONFIG']['directory'] = self.path_box.text()
        config['CONFIG']['java'] = self.java_box.text()
        config["CONFIG"]["console"] = "True" if self.console_checkbox.isChecked() else "False"
        config["CONFIG"]["git"] = "True" if self.git_checkbox.isChecked() else "False"
        config["CONFIG"]["data"] = "True" if self.data_checkbox.isChecked() else "False"
        config["CONFIG"]["warning"] = "True" if self.warning_checkbox.isChecked() else "False"
        config["CONFIG"]["jvm"] = self.jvm_box.text()
        config['CONFIG']["exit"] = "True" if self.exit_checkbox.isChecked() else "False"
        config["CONFIG"]["lang"] = self.language_select.currentText()

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def save_config(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        config["CONFIG"]["username"] = self.username_edit.text()
        config["CONFIG"]["version"] = self.version_select.currentText()
        config["CONFIG"]["ram"] = self.ram_box.text()
        config["CONFIG"]["snapshot"] = str(self.snapshot_checkbox.isChecked())
        config["CONFIG"]["alpha"] = str(self.alpha_checkbox.isChecked())
        config["CONFIG"]["mode"] = self.choice_mod.currentText()
        config["CONFIG"]["directory"] = self.path_box.text()
        config['CONFIG']['java'] = self.java_box.text()
        config["CONFIG"]["console"] = str(self.console_checkbox.isChecked())
        config["CONFIG"]["git"] = str(self.git_checkbox.isChecked())
        config["CONFIG"]["data"] = str(self.data_checkbox.isChecked())
        config["CONFIG"]["jvm"] = self.jvm_box.text()
        config['CONFIG']["exit"] = str(self.exit_checkbox.isChecked())
        config["CONFIG"]["lang"] = self.language_select.currentText()

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

    def closeEvent(self, event):
        self.save_config()
        request.on_close()
        event.accept()

    def state_progress(self, value):
        self.launch_button.setDisabled(value)

        if self.launcher.status:
            self.show_launch_message("Minecraft is installed and starts")
            self.progress_bar.setVisible(False)
            time.sleep(5)
            self.launcher.status = False
            if self.exit_checkbox.isChecked():
                self.close()

    def update_progress(self, progress, max_progress):
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(progress)
        self.progress_bar.setMaximum(max_progress)

    def launch_minecraft(self):
        configer.create_or_no_new_config()
        configer.checker_config_params_to_exist()

        settings['version'] = self.version_select.currentText()
        options["username"] = self.username_edit.text()

        if not regex.check_to_latin_alphabet(options["username"]) and self.warning_checkbox.isChecked():
            self.warning_message("Your name contains symbols that may interfere with your future game")
            return

        if status.check_internet_connection():
            if self.path_box.text() != os.path.join(os.getenv('APPDATA'), '.launch'):
                settings['minecraft_directory'] = self.path_box.text()
            else:
                settings['minecraft_directory'] = os.path.join(os.getenv('APPDATA'), '.launch')
        else:
            settings['minecraft_directory'] = file_work.directory_path_version()[settings['version']]

        if self.jvm_box.text():
            for arg in self.jvm_box.text().split(" "):
                options['jvmArguments'].append(arg)

        ram = int(self.ram_box.text())
        options['jvmArguments'].append(f'-Xmx{ram}M')

        if self.java_box.text() != "":
            options['executablePath'] = os.path.join(self.java_box.text(), 'java.exe')

        settings['console'] = self.console_checkbox.isChecked()
        settings['alpha'] = self.alpha_checkbox.isChecked()
        settings['snapshot'] = self.snapshot_checkbox.isChecked()
        settings['data'] = self.data_checkbox.isChecked()
        settings['git'] = self.git_checkbox.isChecked()
        settings['mods'] = self.choice_mod.currentText()

        if status.check_internet_connection():
            if settings['mods'] == 'Forge':
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + f'Forge {settings['version']}'):
                    if os.path.isdir(settings['minecraft_directory'] + '\\' + f'Forge {settings['version']}'):
                        self.show_message("Minecraft is starting")
            elif settings['mods'] == 'Fabric':
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + f'Fabric {settings['version']}'):
                    if os.path.isdir(settings['minecraft_directory'] + '\\' + f'Fabric {settings['version']}'):
                        self.show_message("Minecraft is starting")
            elif settings['mods'] == 'Qulit':
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + f'Qulit {settings['version']}'):
                    if os.path.isdir(settings['minecraft_directory'] + '\\' + f'Qulit {settings['version']}'):
                        self.show_message("Minecraft is starting")
            else:
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + settings['version']):
                    if os.path.isdir(settings['minecraft_directory'] + '\\' + settings['version']):
                        self.show_message("Minecraft is starting")
        else:
            if settings['mods'] == 'Forge':
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + f'Forge {settings['version']}'):
                    self.show_message("Minecraft is starting")
            elif settings['mods'] == 'Fabric':
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + f'Fabric {settings['version']}'):
                    self.show_message("Minecraft is starting")
            elif settings['mods'] == 'Qulit':
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + f'Qulit {settings['version']}'):
                    self.show_message("Minecraft is starting")
            else:
                if file_work.read_version_and_check(settings['minecraft_directory'] + '\\' + settings['version']):
                    self.show_message("Minecraft is starting")

        self.launcher.start()

        if self.exit_checkbox.isChecked() and file_work.read_version_and_check(
                settings['minecraft_directory'] + '\\' + settings['version']):
            self.close()
