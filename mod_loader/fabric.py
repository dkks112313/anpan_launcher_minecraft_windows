import sys
import subprocess
import uuid
import minecraft_launcher_lib

options = {
    'username': 'denchi',
    'uuid': str(uuid.uuid4()),
    'token': '',
}


def split_fabric_version(text):
    lists = 'fabric-loader-0.16.0-'+text
    return lists


def main():
    vanilla_version = input("Select the Minecraft version for which you want to install fabric:")

    if not minecraft_launcher_lib.fabric.is_minecraft_version_supported(vanilla_version):
        print("This version is not supported by fabric")
        sys.exit(0)

    callback = {
        "setStatus": lambda text: print(text)
    }

    minecraft_launcher_lib.fabric.install_fabric(vanilla_version,
                                                 minecraft_directory='C:\\Users\\ovcha\\AppData\\Roaming\\.minecraft',
                                                 callback=callback)

    command = minecraft_launcher_lib.command.get_minecraft_command(split_fabric_version(vanilla_version),
                                                                   minecraft_directory='C:\\Users\\ovcha\\AppData\\Roaming\\.minecraft',
                                                                   options=options)

    subprocess.Popen(command, creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":
    main()
