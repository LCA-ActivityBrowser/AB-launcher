import os
from conda.cli import main

LOCAL = os.path.split(__file__)[0]

def download_env_spec():
    print("Downloading environment specification...")
    return os.path.join(LOCAL, "download", "environment_spec.txt")


if __name__ == "__main__":
    spec_file = download_env_spec()
    main("env", "update", "--prune", "--file", spec_file, "--name", "base", "--quiet")
