import os
import sys
from conda.cli import main

LOCAL = os.path.split(__file__)[0]

def download_env_spec():
    print("Downloading environment specification...")
    if sys.platform == "win32":
        return os.path.join(LOCAL, "download", "win-environment_spec.txt")
    elif sys.platform == "darwin":
        return os.path.join(LOCAL, "download", "mac-environment_spec.txt")
    else:
        raise OSError


if __name__ == "__main__":
    spec_file = download_env_spec()
    main("env", "update", "--prune", "--file", spec_file, "--name", "base", "--quiet")
