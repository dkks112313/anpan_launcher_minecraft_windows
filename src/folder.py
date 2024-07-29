import os
from src import env
import shutil


def removing_folder_resources():
    folder_from = rf'{os.path.join(os.getcwd(), 'resources')}'
    folder_to = rf'{os.path.join(env.settings['minecraft_directory'], 'resources')}'

    for f in os.listdir(folder_from):
        if os.path.isfile(os.path.join(folder_from, f)):
            shutil.copy(os.path.join(folder_from, f), os.path.join(folder_to, f))
        if os.path.isdir(os.path.join(folder_from, f)):
            os.system(f'rd /S /Q {folder_to}\\{f}')
            shutil.copytree(os.path.join(folder_from, f), os.path.join(folder_to, f))
