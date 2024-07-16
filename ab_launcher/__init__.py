import os

from ab_launcher import paths


def update_check():
    import json
    import urllib.request

    if SETUP:
        return False

    with open(os.path.join(paths.AB_DIR, "config"), 'r') as file:
        config = json.load(file)

    current = config["launcher"]["ab_version"]
    branch = config["launcher"]["branch"]

    if os.environ.get("AB_FORCE_VERSION", False):
        latest = os.environ.get("AB_FORCE_VERSION")
    else:
        latest_url = "https://raw.githubusercontent.com/mrvisscher/AB-launcher/main/ab_releases/latest.json"
        path, _ = urllib.request.urlretrieve(latest_url)
        with open(path) as json_file:
            latest = json.load(json_file)[branch]

    return not current == latest


SETUP = not os.path.isfile(os.path.join(paths.AB_DIR, "config"))
UPDATE = update_check()

