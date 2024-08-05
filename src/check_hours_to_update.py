import sys
import time
import json
from datetime import datetime, timedelta
import minecraft_launcher_lib
from packaging import version


def default_converter(o):
    if isinstance(o, datetime):
        return o.isoformat()
    raise TypeError("Can't to transform object")


def save_last_execution_time():
    with open("last_execution.json", "w") as file:
        json.dump({"last_execution": datetime.now().isoformat()}, file)


def load_last_execution_time():
    try:
        with open("last_execution.json", "r") as file:
            data = json.load(file)
            return datetime.fromisoformat(data["last_execution"])
    except FileNotFoundError:
        return None


def perform_task():
    checking_json()
    save_last_execution_time()


def should_run_task():
    last_execution = load_last_execution_time()
    if last_execution is None:
        return True
    return datetime.now() - last_execution >= timedelta(days=1)


def split_forge(versio):
    app = ''
    for i in versio:
        if i == '-':
            break
        app += i

    return app


def checking_json():
    version_vanilla = minecraft_launcher_lib.utils.get_version_list()

    version_forge = []
    for version_info in minecraft_launcher_lib.utils.get_version_list():
        if minecraft_launcher_lib.forge.find_forge_version(version_info['id']):
            version_forge.append(split_forge(minecraft_launcher_lib.forge.find_forge_version(version_info['id'])))
    '''for version_info in minecraft_launcher_lib.forge.list_forge_versions():
        app = ''
        for i in version_info:
            if i == '-':
                break
            else:
                app += i

        if not (version.parse('1.1') <= version.parse(app) <= version.parse('1.12.2')):
            version_forge.append(version_info)'''

    version_fabric = []
    for i in minecraft_launcher_lib.fabric.get_all_minecraft_versions():
        if minecraft_launcher_lib.fabric.is_minecraft_version_supported(i['version']):
            version_fabric.append(i)

    version_qulit = []
    for i in minecraft_launcher_lib.quilt.get_all_minecraft_versions():
        if minecraft_launcher_lib.quilt.is_minecraft_version_supported(i['version']):
            version_qulit.append(i)

    with open('version_vanilla.json', 'w', encoding='utf-8') as file:
        json.dump(version_vanilla, file, default=default_converter, indent=4, ensure_ascii=False)

    with open('version_forge.json', 'w', encoding='utf-8') as file:
        json.dump(version_forge, file, default=default_converter, indent=4, ensure_ascii=False)

    with open('version_fabric.json', 'w', encoding='utf-8') as file:
        json.dump(version_fabric, file, default=default_converter, indent=4, ensure_ascii=False)

    with open('version_qulit.json', 'w', encoding='utf-8') as file:
        json.dump(version_qulit, file, default=default_converter, indent=4, ensure_ascii=False)


if should_run_task():
    perform_task()
