import os
import sys
import shutil
import urllib.request
import json

from ab_launcher import paths
from ab_launcher.gui.splashscreen import splash
from ab_launcher.setup.conda import explicit_updater


def download_env_spec():
    splash.undefined_progress()
    splash.notify("Downloading environment specification...")

    base_url = "https://api.github.com/repos/mrvisscher/AB-launcher/contents/ab_releases/"
    current_url = base_url + "current.json"
    path, _ = urllib.request.urlretrieve(current_url)
    with open(path) as json_file:
        current = json.load(json_file)["ab"]

    if sys.platform == "win32":
        env_spec_url = base_url + "windows/win-environment-" + current + ".txt"
    elif sys.platform == "darwin":
        env_spec_url = base_url + "macos/macos-environment-" + current + ".txt"
    else:
        raise OSError
    path, _ = urllib.request.urlretrieve(env_spec_url)

    # rename to a .txt file, because that's what conda supports
    txt_path = path + ".txt"
    os.rename(path, txt_path)

    return txt_path


def set_flag_file():
    # create installed file as a flag that installation was successful
    with open(os.path.join(paths.AB_DIR, "installed"), "w") as file:
        file.writelines(["Installed"])


def parse_env_spec(file_loc: str) -> list[str]:
    specs = []

    with open(file_loc, 'r') as file:
        for line in file.readlines():
            if line.startswith('#') or line.startswith('@'):
                continue
            specs.append(line.strip())

    return specs


def post_install():
    shutil.rmtree(paths.PKGS_DIR)


def setup():
    spec_file = download_env_spec()

    specs = parse_env_spec(spec_file)

    explicit_updater(specs, splash)

    post_install()

    set_flag_file()

