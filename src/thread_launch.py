import os
import subprocess
import minecraft_launcher_lib
import platform
import json
from packaging import version

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
    def find_longest_filename(dir):
        longest_filename = ""
        max_length = 0

        for filename in os.listdir(dir):
            if len(filename) > max_length:
                longest_filename = filename
                max_length = len(filename)

        return longest_filename

    def run(self):
        self.state_signal.emit(True)

        if options['username'] == '':
            return

        appdata = os.getenv('APPDATA')
        os.makedirs(os.path.join(appdata, '.launch'), exist_ok=True)

        if settings['mods'] == 'Forge':
            if settings['minecraft_directory'] == '':
                os.makedirs(os.path.join(appdata, '.launch\\', f'Forge {settings['version']}'), exist_ok=True)
                settings['minecraft_directory'] = os.path.join(appdata, '.launch\\', f'Forge {settings['version']}')
            else:
                settings['minecraft_directory'] += f'\\Forge {settings['version']}'
        elif settings['mods'] == 'Fabric':
            if settings['minecraft_directory'] == '':
                os.makedirs(os.path.join(appdata, '.launch\\', f'Fabric {settings['version']}'), exist_ok=True)
                settings['minecraft_directory'] = os.path.join(appdata, '.launch\\', f'Fabric {settings['version']}')
            else:
                settings['minecraft_directory'] += f'\\Fabric {settings['version']}'
        elif settings['mods'] == 'Qulit':
            if settings['minecraft_directory'] == '':
                os.makedirs(os.path.join(appdata, '.launch\\', f'Qulit {settings['version']}'), exist_ok=True)
                settings['minecraft_directory'] = os.path.join(appdata, '.launch\\', f'Qulit {settings['version']}')
            else:
                settings['minecraft_directory'] += f'\\Qulit {settings['version']}'
        else:
            if settings['minecraft_directory'] == '':
                os.makedirs(os.path.join(appdata, '.launch\\', settings['version']), exist_ok=True)
                settings['minecraft_directory'] = os.path.join(appdata, '.launch\\', settings['version'])
            else:
                settings['minecraft_directory'] += f'\\{settings['version']}'

        file = file_work.FileLog()

        core = ''
        if platform.system() == "Windows":
            if platform.architecture()[0] == "32bit":
                core = "windows-x86"
            else:
                core = "windows-x64"
        elif platform.system() == "Linux":
            if platform.architecture()[0] == "32bit":
                core = "linux-i386"
            else:
                core = "linux"
        elif platform.system() == "Darwin":
            if platform.machine() == "arm64":
                core = "mac-os-arm64"
            else:
                core = "mac-os"

        runtime = ''
        if version.parse('1.20.6') <= version.parse(settings['version']) <= version.parse('1.21'):
            runtime = 'java-runtime-delta'
        elif version.parse('1.19') <= version.parse(settings['version']) <= version.parse('1.20.4'):
            runtime = 'java-runtime-gamma'
        elif version.parse('1.18') <= version.parse(settings['version']) <= version.parse('1.18.2'):
            runtime = 'java-runtime-beta'
        elif version.parse('1.17.1') == version.parse(settings['version']):
            runtime = 'java-runtime-alpha'
        elif version.parse('1.1') <= version.parse(settings['version']) <= version.parse('1.16.5'):
            runtime = 'jre-legacy'

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
                vers = minecraft_launcher_lib.forge.find_forge_version(settings['version'])
                if version.parse('1.1') <= version.parse(settings['version']) <= version.parse('1.12.1'):
                    os.makedirs(minecraft_directory, exist_ok=True)
                    data = {
                        "clientToken": "f31f3299-7ead-4649-802d-14e7608bfc59",
                        "profiles": {}
                    }

                    if not os.path.isfile(f'{minecraft_directory}\\launcher_profiles.json'):
                        with open(f'{minecraft_directory}\\launcher_profiles.json', 'a') as file:
                            json.dump(data, file, indent=4)

                    try:
                        minecraft_launcher_lib.forge.run_forge_installer(vers)
                    except Exception as e:
                        pass

                minecraft_launcher_lib.forge.install_forge_version(vers,
                                                                   settings['minecraft_directory'],
                                                                   callback={
                                                                       'setStatus': self.update_progress_label,
                                                                       'setProgress': self.update_progress,
                                                                       'setMax': self.update_progress_max},
                                                                   java=f'{minecraft_directory}\\runtime\\{runtime}\\{core}\\{runtime}\\bin\\java.exe')

                self.progress = self.progress_max
                self.progress_signal.emit(self.progress, self.progress_max, self.progress_label)
            elif settings['mods'] == "Fabric":
                minecraft_launcher_lib.fabric.install_fabric(settings['version'],
                                                             settings['minecraft_directory'],
                                                             callback={
                                                                 'setStatus': self.update_progress_label,
                                                                 'setProgress': self.update_progress,
                                                                 'setMax': self.update_progress_max},
                                                             java=f'{minecraft_directory}\\runtime\\{runtime}\\{core}\\{runtime}\\bin\\java.exe')
            elif settings['mods'] == "Qulit":
                minecraft_launcher_lib.quilt.install_quilt(settings['version'],
                                                           settings['minecraft_directory'],
                                                           callback={
                                                               'setStatus': self.update_progress_label,
                                                               'setProgress': self.update_progress,
                                                               'setMax': self.update_progress_max},
                                                           java=f'{minecraft_directory}\\runtime\\{runtime}\\{core}\\{runtime}\\bin\\java.exe')

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

        versions = ''
        if settings['mods'] == 'Vanilla':
            versions = settings['version']
        elif settings['mods'] == "Forge" or settings['mods'] == 'Fabric' or settings['mods'] == 'Qulit':
            versions = self.find_longest_filename(os.path.join(minecraft_directory, 'versions'))

        command = minecraft_launcher_lib.command.get_minecraft_command(version=versions,
                                                                       minecraft_directory=
                                                                       minecraft_directory,
                                                                       options=options)

        if settings['console']:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

        options['jvmArguments'] = []
        self.state_signal.emit(False)
