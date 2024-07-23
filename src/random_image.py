import random
from pathlib import Path


def random_image():
    x = random.randint(1, 17)
    return f"content\\{x}.jpg"


def random_image2():
    path = Path('content')
    file = [x for x in path.iterdir() if x.is_file()]
    if len(file) == 0:
        return ""
    index = random.randint(0, len(file) - 1)

    image_list = []
    for image_name in path.iterdir():
        if image_name.is_file():
            image_list.append(image_name.name)

    return f"content\\{image_list[index]}"
