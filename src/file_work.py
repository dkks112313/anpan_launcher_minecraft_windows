import os


class FileLog:
    def __init__(self, minecraft_directory):
        self.path = os.path.join(minecraft_directory)

    def read_version(self):
        file = open('version', 'a')
        file.close()
        file = open('version', 'r', encoding='utf-8')
        while True:
            line = file.readline()
            if not line:
                break
            if self.path + '\n' == line:
                file.close()
                return False
        file.close()
        return True

    def write_version(self):
        with open('version', 'a', encoding='utf-8') as file:
            file.writelines(str(self.path) + '\n')
            file.close()


def check_version_list():
    file = open('version', 'a')
    file.close()
    file = open('version', 'r', encoding='utf-8')
    list_stings = []
    while True:
        line = file.readline()
        if not line:
            break
        if os.path.isdir(line[:len(line) - 1]):
            list_stings.append(line)
    file.close()

    file = open('version', 'w', encoding='utf-8')
    file.writelines(list_stings)
    file.close()
