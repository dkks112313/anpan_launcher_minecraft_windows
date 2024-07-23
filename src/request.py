import requests
import platform

number_require = 1


def get_json():
    uname_info = platform.uname()

    return {
        'System': f'{uname_info.system}',
        'Name node': f'{uname_info.node}',
        'Release': f'{uname_info.release}',
        'Version': f'{uname_info.version}',
        'Machine': f'{uname_info.machine}',
        'Processor': f'{uname_info.processor}',
        'Count': 1
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
