import os
from pathlib import Path
import sys
from conda.cli import main

ROOT = Path(__file__).parent.parent


def download_env_spec():
    print("Downloading environment specification...")
    if sys.platform == "win32":
        return os.path.join(ROOT, "download", "win-environment_spec.txt")
    elif sys.platform == "darwin":
        return os.path.join(ROOT, "download", "mac-environment_spec.txt")
    else:
        raise OSError


if __name__ == "__main__":
    spec_file = download_env_spec()
    main("env", "update", "--prune", "--file", spec_file, "--name", "base", "--quiet")
