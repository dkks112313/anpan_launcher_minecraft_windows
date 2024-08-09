import requests

REPO = "dkks112313/An-Pan-Launcher"
ASSET_NAME = "An-Pan-Launcher.exe"


def get_latest_version():
    response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
    release_data = response.json()

    return release_data.get("name")
