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
        config['CONFIG']['jvm'] = ""
        config['CONFIG']['version_id'] = ""

        with open('config.ini', 'w') as configfile:
            config.write(configfile)
