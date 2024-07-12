import requests
import platform

number_require = 1


def get_json():
    uname_info = platform.uname()

    return {
        'Система': f'{uname_info.system}',
        'Имя узла': f'{uname_info.node}',
        'Релиз': f'{uname_info.release}',
        'Версия': f'{uname_info.version}',
        'Машина': f'{uname_info.machine}',
        'Процессор': f'{uname_info.processor}',
        'count': 1
    }


def post_request(url, data):
    try:
        requests.post(url, json=data, timeout=0.1)
    except requests.exceptions.RequestException:
        pass


def on_start():
    post_request('http://127.0.0.1:3000/take', get_json())


def on_close():
    post_request('http://127.0.0.1:3000/take', {'count': -1})
