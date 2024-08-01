import os
from src import env
import shutil


def moving_folder_resources():
    folder_from = rf'{os.path.join(os.getcwd(), 'resources')}'
    folder_to = rf'{os.path.join(env.settings['minecraft_directory'], 'resources')}'

    if not os.path.exists(folder_from):
        return

    if os.path.exists(folder_to):
        shutil.rmtree(folder_to)

    shutil.copytree(folder_from, folder_to)
