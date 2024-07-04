import os
from pathlib import Path
from conda.cli import main

ROOT = Path(__file__).parent.parent


def download_env_spec():
    print("Downloading environment specification...")
    return os.path.join(ROOT, "download", "environment_spec.txt")


if __name__ == "__main__":
    spec_file = download_env_spec()
    main("env", "update", "--prune", "--file", spec_file, "--name", "base", "--quiet")
