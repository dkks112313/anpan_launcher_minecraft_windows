import os
import shutil
import zipfile


def update_and_cleaning():
    with zipfile.ZipFile('game-launcher.zip', 'r') as zip_ref:
        zip_ref.extractall()

    list_files = ['An-Pan-Launcher.exe', 'icon.ico', 'content', 'resources']

    if os.path.isdir(f'{os.getcwd()}/content'):
        shutil.rmtree(f'{os.getcwd()}/content')

    if os.path.isdir(f'{os.getcwd()}/resources'):
        shutil.rmtree(f'{os.getcwd()}/resources')

    for i in list_files:
        shutil.move(f'{os.getcwd()}/An-Pan-Launcher/{i}', f'{os.getcwd()}/{i}')

    shutil.rmtree(f'{os.getcwd()}/An-Pan-Launcher')
    os.system("del game-launcher.zip")
