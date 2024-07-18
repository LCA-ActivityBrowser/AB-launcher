import os
import sys
import urllib.request

import certifi
import ssl

from ab_launcher import paths, io

# set conda environmental variables
os.environ["CONDA_PREFIX"] = paths.ENV_DIR
os.environ["CONDA_PKGS_DIRS"] = paths.PKGS_DIR
os.environ["CONDA_REGISTER_ENVS"] = "false"
os.environ["CONDA_EXE"] = ""
os.environ["CONDA_PYTHON_EXE"] = ""
os.environ["CONDA_DEFAULT_ENV"] = ""
os.environ["CONDA_ROOT"] = ""

def setup_urllib():
    context = ssl.create_default_context(cafile=certifi.where())
    https_handler = urllib.request.HTTPSHandler(context=context)
    opener = urllib.request.build_opener(https_handler)
    urllib.request.install_opener(opener)

def update_check():
    import json
    import urllib.request

    if SETUP:
        return False

    with open(os.path.join(paths.ROOT, "config"), 'r') as file:
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


SETUP = not os.path.isfile(os.path.join(paths.ROOT, "config"))
UPDATE = update_check()


sys.stdout = io.MultiIO([sys.stdout])
sys.stderr = io.MultiIO([sys.stderr])

setup_urllib()