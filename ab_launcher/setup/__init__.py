import os
import sys
import shutil
import urllib.request
import json

from ab_launcher import paths
from ab_launcher.gui.splashscreen import splash
from ab_launcher.setup.conda import explicit_updater


class Setup:
    current = None

    def download_env_spec(self):
        splash.undefined_progress()
        splash.notify("Downloading environment specification...")

        base_url = "https://raw.githubusercontent.com/mrvisscher/AB-launcher/main/ab_releases/"
        current_url = base_url + "current.json"
        path, _ = urllib.request.urlretrieve(current_url)
        with open(path) as json_file:
            self.current = json.load(json_file)["dev"]  # should be configurable between dev and stable

        if sys.platform == "win32":
            env_spec_url = base_url + "dev/windows/win-environment-" + self.current + ".txt"
        elif sys.platform == "darwin":
            env_spec_url = base_url + "dev/macos/macos-environment-" + self.current + ".txt"
        else:
            raise OSError
        path, _ = urllib.request.urlretrieve(env_spec_url)

        return path

    def set_config_file(self):
        # create installed file as a flag that installation was successful
        with open(os.path.join(paths.AB_DIR, "config"), "w") as file:
            data = {
                "launcher": {
                    "launcher_version": "0.0.0",
                    "ab_version": self.current,
                    "ignored_updates": [],
                }
            }

            file.write(json.dumps(data))

    def parse_env_spec(self, file_loc: str) -> list[str]:
        specs = []

        with open(file_loc, 'r') as file:
            for line in file.readlines():
                if line.startswith('#') or line.startswith('@'):
                    continue
                specs.append(line.strip())

        return specs

    def post_install(self):
        try:
            shutil.rmtree(paths.PKGS_DIR)
        except FileNotFoundError:
            # no pkg dir to worry about
            pass


def setup():
    setupper = Setup()
    spec_file = setupper.download_env_spec()

    specs = setupper.parse_env_spec(spec_file)

    explicit_updater(specs, splash)

    setupper.post_install()

    setupper.set_config_file()

