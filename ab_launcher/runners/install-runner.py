import os
import sys
import urllib.request
from pathlib import Path

from conda.cli import main

ROOT = Path(__file__).parent.parent


def download_env_spec():
    print("Downloading environment specification...")
    if sys.platform == "win32":
        env_spec_url = "https://github.com/mrvisscher/AB-launcher/raw/ac3dde812d7faac173e65972fefb29ae7b9e476d/ab_launcher/download/win-environment_spec.txt"
    elif sys.platform == "darwin":
        env_spec_url = "https://github.com/mrvisscher/AB-launcher/raw/ac3dde812d7faac173e65972fefb29ae7b9e476d/ab_launcher/download/mac-environment_spec.txt"
    else:
        raise OSError
    path, _ = urllib.request.urlretrieve(env_spec_url, "env_spec.txt")
    return path


if __name__ == "__main__":
    spec_file = download_env_spec()
    main("env", "update", "--prune", "--file", spec_file, "--name", "base", "--quiet")
