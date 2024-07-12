import os
import sys
import shutil
import urllib.request

from ab_launcher import paths
from ab_launcher.gui.splashscreen import splash
from ab_launcher.setup.conda import explicit_updater


def download_env_spec():
    splash.undefined_progress()
    splash.notify("Downloading environment specification...")

    if sys.platform == "win32":
        env_spec_url = "https://github.com/mrvisscher/AB-launcher/raw/b9a16902e2d3fa97e17539fe88e38fb575ab9a9d/ab_launcher/download/win-environment_spec.txt"
    elif sys.platform == "darwin":
        env_spec_url = "https://github.com/mrvisscher/AB-launcher/raw/ca56eb1dafb7ff0cfda42fb51927afd453a0c68e/ab_launcher/download/mac-environment_spec.txt"
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

