class FileLog:
    def __init__(self, version):
        self.version = version

    def read(self):
        file = open('../version', 'a')
        file.close()
        file = open('../version', 'r', encoding='utf-8')
        while True:
            line = file.readline()
            if not line:
                break
            if self.version + '\n' == line:
                file.close()
                return False
        file.close()
        return True

    def write(self):
        file = open('../version', 'a', encoding='utf-8')
        file.writelines(self.version+'\n')
        file.close()


class SaveFile:
    def __init__(self):
        pass
