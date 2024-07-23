import requests

REPO = "dkks112313/An-Pan-Launcher"
ASSET_NAME = "An-Pan-Launcher.exe"


def get_latest_version():
    response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
    release_data = response.json()

    return release_data.get("name")


'''
def get_latest_exe():
    response = requests.get(f"https://api.github.com/repos/{REPO}/releases/latest")
    release_data = response.json()

    asset_url = None
    for asset in release_data.get("assets", []):
        if asset["name"] == ASSET_NAME:
            asset_url = asset["browser_download_url"]
            break

    if not asset_url:
        print(f"Error: Asset with named {ASSET_NAME} not found in latest release.")
        exit(1)

    response = requests.get(asset_url)
    with open(ASSET_NAME, "wb") as file:
        file.write(response.content)

    print(f"File {ASSET_NAME} success installed.")
'''
