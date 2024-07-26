import os
import subprocess
import minecraft_launcher_lib
from PyQt6.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal
from PyQt6.QtWidgets import QMessageBox
from src import file_work
from src.env import *


class Launcher(QThread):
    progress_signal = pyqtSignal(int, int, str)
    state_signal = pyqtSignal(bool)
    progress = 0
    progress_max = 0
    progress_label = ''
    status = False
    mutex = QMutex()
    wait_condition = QWaitCondition()

    def release_wait(self):
        self.mutex.lock()
        self.wait_condition.wakeAll()
        self.mutex.unlock()

    def update_progress_label(self, value):
        self.progress_label = value
        self.progress_signal.emit(self.progress, self.progress_max, self.progress_label)

    def update_progress(self, value):
        self.progress = value
        self.progress_signal.emit(self.progress, self.progress_max, self.progress_label)

    def update_progress_max(self, value):
        self.progress_max = value
        self.progress_signal.emit(self.progress, self.progress_max, self.progress_label)

    def run(self):
        self.state_signal.emit(True)

        if options['username'] == '':
            return

        appdata = os.getenv('APPDATA')
        os.makedirs(os.path.join(appdata, '.launch'), exist_ok=True)

        if settings['minecraft_directory'] == '':
            os.makedirs(os.path.join(appdata, '.launch\\', settings['version']), exist_ok=True)
            settings['minecraft_directory'] = os.path.join(appdata, '.launch\\', settings['version'])
        else:
            settings['minecraft_directory'] += f'\\{settings['version']}'

        file = file_work.FileLog(minecraft_directory=settings['minecraft_directory'])

        minecraft_directory = settings['minecraft_directory']
        if file.read_version():
            file.write_version()
            self.status = True
            minecraft_launcher_lib.install.install_minecraft_version(versionid=settings['version'],
                                                                     minecraft_directory=
                                                                     settings['minecraft_directory'],
                                                                     callback={'setStatus': self.update_progress_label,
                                                                               'setProgress': self.update_progress,
                                                                               'setMax': self.update_progress_max})

            self.state_signal.emit(False)

            self.mutex.lock()
            self.wait_condition.wait(self.mutex)
            self.mutex.unlock()

        if settings['version'] == '1.16.5':
            options['jvmArguments'].append('-Dminecraft.api.env=custom')
            options['jvmArguments'].append('-Dminecraft.api.auth.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.account.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.session.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.services.host=https://invalid.invalid/')

        command = minecraft_launcher_lib.command.get_minecraft_command(version=settings['version'],
                                                                       minecraft_directory=
                                                                       minecraft_directory,
                                                                       options=options)

        if settings['console']:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

        options['jvmArguments'] = []

        #self.state_signal.emit(False)
