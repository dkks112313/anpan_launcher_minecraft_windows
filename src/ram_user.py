import psutil


def ram_size():
    total = psutil.virtual_memory()
    ram = int(total.total / (1024 ** 3))

    return ram
