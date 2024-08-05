import os
import subprocess
import minecraft_launcher_lib

from PyQt6.QtCore import QThread, QWaitCondition, QMutex, pyqtSignal
from src import file_work, folder
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

    @staticmethod
    def split_forge_version(text):
        lists = text.split('-')
        lists[0] += '-forge-'
        lists[0] += lists[1]
        return lists[0]

    @staticmethod
    def split_fabric_version(text):
        fabric = 'fabric-loader-' + minecraft_launcher_lib.fabric.get_latest_loader_version() + '-' + text
        return fabric

    @staticmethod
    def split_qulit_version(text):
        qulit = 'quilt-loader-' + minecraft_launcher_lib.quilt.get_latest_loader_version() + '-' + text
        return qulit

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

        file = file_work.FileLog()

        minecraft_directory = settings['minecraft_directory']
        if file.read_version(minecraft_directory):
            file.write_version(minecraft_directory)
            self.status = True
            if settings['mods'] == "Vanilla":
                minecraft_launcher_lib.install.install_minecraft_version(versionid=settings['version'],
                                                                         minecraft_directory=
                                                                         settings['minecraft_directory'],
                                                                         callback={
                                                                         'setStatus': self.update_progress_label,
                                                                         'setProgress': self.update_progress,
                                                                         'setMax': self.update_progress_max})
                folder.moving_folder_resources()
            elif settings['mods'] == "Forge":
                minecraft_launcher_lib.forge.install_forge_version(settings['version'],
                                                                   settings['minecraft_directory'],
                                                                   callback={
                                                                   'setStatus': self.update_progress_label,
                                                                   'setProgress': self.update_progress,
                                                                   'setMax': self.update_progress_max},
                                                                   java=f'{minecraft_directory}\\runtime\\jre-legacy\\windows-x64\\jre-legacy\\bin\\java.exe')
            elif settings['mods'] == "Fabric":
                minecraft_launcher_lib.fabric.install_fabric(settings['version'],
                                                             settings['minecraft_directory'],
                                                             callback={
                                                             'setStatus': self.update_progress_label,
                                                             'setProgress': self.update_progress,
                                                             'setMax': self.update_progress_max},
                                                             java=f'{minecraft_directory}\\runtime\\jre-legacy\\windows-x64\\jre-legacy\\bin\\java.exe')
            elif settings['mods'] == "Qulit":
                minecraft_launcher_lib.quilt.install_quilt(settings['version'],
                                                           settings['minecraft_directory'],
                                                           callback={
                                                           'setStatus': self.update_progress_label,
                                                           'setProgress': self.update_progress,
                                                           'setMax': self.update_progress_max},
                                                           java=f'{minecraft_directory}\\runtime\\jre-legacy\\windows-x64\\jre-legacy\\bin\\java.exe')

            self.state_signal.emit(False)

            self.mutex.lock()
            self.wait_condition.wait(self.mutex)
            self.mutex.unlock()

        if len(settings['version']) >= 6:
            if settings['version'][:6] == '1.16.5':
                options['jvmArguments'].append('-Dminecraft.api.env=custom')
                options['jvmArguments'].append('-Dminecraft.api.auth.host=https://invalid.invalid/')
                options['jvmArguments'].append('-Dminecraft.api.account.host=https://invalid.invalid/')
                options['jvmArguments'].append('-Dminecraft.api.session.host=https://invalid.invalid/')
                options['jvmArguments'].append('-Dminecraft.api.services.host=https://invalid.invalid/')

        version = ''
        if settings['mods'] == 'Vanilla':
            version = settings['version']
        elif settings['mods'] == "Forge":
            version = self.split_forge_version(settings['version'])
        elif settings['mods'] == 'Fabric':
            version = self.split_fabric_version(settings['version'])
        elif settings['mods'] == 'Qulit':
            version = self.split_qulit_version(settings['version'])

        command = minecraft_launcher_lib.command.get_minecraft_command(version=version,
                                                                       minecraft_directory=
                                                                       minecraft_directory,
                                                                       options=options)

        if settings['console']:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

        options['jvmArguments'] = []
        self.state_signal.emit(False)
