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
        config['CONFIG']['version_id'] = ""

        with open('config.ini', 'w') as configfile:
            config.write(configfile)


def checker_config_params_to_exist():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if not config.has_option('CONFIG', 'username'):
        config['CONFIG']['username'] = "user"

    if not config.has_option('CONFIG', 'version'):
        config['CONFIG']['version'] = "1.21"

    if not config.has_option('CONFIG', 'ram'):
        config['CONFIG']['ram'] = "4096"

    if not config.has_option('CONFIG', 'snapshot'):
        config['CONFIG']['snapshot'] = "False"

    if not config.has_option('CONFIG', 'alpha'):
        config['CONFIG']['alpha'] = "False"

    if not config.has_option('CONFIG', 'directory'):
        config['CONFIG']['directory'] = ""

    if not config.has_option('CONFIG', 'console'):
        config['CONFIG']['console'] = "False"

    if not config.has_option('CONFIG', 'git'):
        config['CONFIG']['git'] = "True"

    if not config.has_option('CONFIG', 'data'):
        config['CONFIG']['data'] = "False"

    if not config.has_option('CONFIG', 'warning'):
        config['CONFIG']['warning'] = "False"

    if not config.has_option('CONFIG', 'jvm'):
        config['CONFIG']['jvm'] = ""

    if not config.has_option('CONFIG', 'version_id'):
        config['CONFIG']['version_id'] = ""
