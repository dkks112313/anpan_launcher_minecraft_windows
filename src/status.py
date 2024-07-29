import requests


def check_internet_connection():
    url = 'https://www.google.com'
    try:
        response = requests.get(url, timeout=2)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False
