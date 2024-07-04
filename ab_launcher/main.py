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
os.environ["CONDA_PKGS_DIRS"] = PKGS_DIR
os.environ["CONDA_REGISTER_ENVS"] = "false"


def env_exists() -> bool:
    if not os.path.isdir(AB_DIR):
        os.makedirs(AB_DIR, exist_ok=True)
        return False

    if not os.path.isfile(PY_DIR):
        return False

    return True


# launch as a subprocess
if __name__ == "__main__":
    if not env_exists():
        from ab_launcher.install import install
        install()

    launcher = subprocess.Popen(
        [PY_DIR, LAUNCH],
        stdout=sys.stdout,
        stderr=sys.stderr,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    launcher.wait()
