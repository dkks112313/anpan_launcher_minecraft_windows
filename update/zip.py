import os
import shutil
import zipfile


def update_and_cleaning():
    file_except = 'update.exe'

    files_remove = os.listdir(os.getcwd())
    for i in files_remove:
        if os.path.isdir(i):
            shutil.rmtree(f'{os.getcwd()}/{i}')

    with zipfile.ZipFile('game-launcher.zip', 'r') as zip_ref:
        zip_ref.extractall()

    files = os.listdir(os.path.join(os.getcwd(), 'An-Pan-Launcher'))

    for file in files:
        if file == file_except:
            continue

        shutil.move(f'{os.getcwd()}/An-Pan-Launcher/{file}', f'{os.getcwd()}/{file}')

    shutil.rmtree(f'{os.getcwd()}/An-Pan-Launcher')
    os.system("del game-launcher.zip")
