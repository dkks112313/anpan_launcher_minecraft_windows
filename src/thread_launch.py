import os
import subprocess
import minecraft_launcher_lib
from PyQt6.QtCore import QThread
import file_work
from env import *


class Launcher(QThread):
    def run(self):
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

        if file.read_version():
            file.write_version()
            minecraft_launcher_lib.install.install_minecraft_version(versionid=settings['version'],
                                                                     minecraft_directory=settings['minecraft_directory'])

        if settings['version'] == '1.16.5':
            options['jvmArguments'].append('-Dminecraft.api.env=custom')
            options['jvmArguments'].append('-Dminecraft.api.auth.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.account.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.session.host=https://invalid.invalid/')
            options['jvmArguments'].append('-Dminecraft.api.services.host=https://invalid.invalid/')

        command = minecraft_launcher_lib.command.get_minecraft_command(version=settings['version'],
                                                                       minecraft_directory=settings['minecraft_directory'],
                                                                       options=options)

        if settings['console']:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NEW_CONSOLE)
        else:
            subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)

        options['jvmArguments'] = []
