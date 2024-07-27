import os
import configparser


def check_config_exist():
    if os.path.exists("config.ini"):
        return True

    return False


def create_or_no_new_config():
    if not check_config_exist():
        file = open("config.ini", "a")
        file.close()
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.add_section('CONFIG')
        config['CONFIG']['username'] = "user"
        config['CONFIG']['version'] = "1.21"
        config['CONFIG']['ram'] = "4096"
        config['CONFIG']['snapshot'] = "False"
        config['CONFIG']['alpha'] = "False"
        config['CONFIG']['directory'] = ""
        config['CONFIG']['console'] = "False"
        config['CONFIG']['git'] = "True"
        config['CONFIG']['data'] = "False"
        config['CONFIG']['warning'] = "False"
        config['CONFIG']['jvm'] = ""
        config['CONFIG']['exit'] = "False"
        config['CONFIG']['lang'] = "English"
        config['CONFIG']['version_id'] = ""

        with open('config.ini', 'w') as configfile:
            config.write(configfile)


def checker_config_params_to_exist():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if 'CONFIG' not in config:
        config['CONFIG'] = {}

    default_values = {
        "username": "user",
        "version": "latest",
        "ram": "4096",
        "snapshot": "False",
        "alpha": "False",
        "directory": os.path.join(os.getenv('APPDATA'), '.launch'),
        "console": "False",
        "git": "True",
        "warning": "True",
        "data": "False",
        "jvm": "",
        "exit": "False",
        "lang": "English",
        "version_id": ""
    }

    for key, value in default_values.items():
        if key not in config['CONFIG']:
            config['CONFIG'][key] = value

    with open('config.ini', 'w') as configfile:
        config.write(configfile)
