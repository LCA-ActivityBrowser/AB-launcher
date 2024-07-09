import os
import sys
import subprocess

import appdirs

from ab_launcher import LAUNCH

# appdata dirs
AB_DIR = appdirs.AppDirs("ActivityBrowser", "pylca").user_data_dir
ENV_DIR = os.path.join(AB_DIR, "environment")
PY_DIR = os.path.join(ENV_DIR, "python.exe")
PKGS_DIR = os.path.join(AB_DIR, "pkgs")

# set conda environmental variables
os.environ["CONDA_PREFIX"] = ENV_DIR
os.environ["CONDA_PKGS_DIRS"] = PKGS_DIR
os.environ["CONDA_REGISTER_ENVS"] = "false"


def env_exists() -> bool:
    if not os.path.isdir(AB_DIR):
        os.makedirs(AB_DIR, exist_ok=True)
        return False

    if not os.path.isfile(os.path.join(AB_DIR, "installed")):
        return False

    return True


# launch as a subprocess
if __name__ == "__main__":
    print("AB-launcher version 0.0.0")
    if not env_exists():
        print("Installing the Activity Browser")
        from ab_launcher.install import install
        exit_code = install()
        if exit_code != 0:
            sys.exit(exit_code)

    print("Launching the Activity Browser")
    launcher = subprocess.Popen(
        [PY_DIR, LAUNCH],
    )
    launcher.wait()
