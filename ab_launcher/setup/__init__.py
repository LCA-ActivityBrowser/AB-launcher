import os
import sys
import shutil
import urllib.request
import json

from ab_launcher import paths
from ab_launcher.gui.splashscreen import Splash
from ab_launcher.setup.conda import explicit_updater


class Setup:
    latest = None

    def download_env_spec(self):
        Splash().undefined_progress()
        Splash().notify("Downloading environment specification...")

        base_url = "https://raw.githubusercontent.com/mrvisscher/AB-launcher/main/ab_releases/"

        if os.environ.get("AB_FORCE_VERSION", False):
            self.latest = os.environ.get("AB_FORCE_VERSION")
        else:
            latest_url = base_url + "latest.json"
            path, _ = urllib.request.urlretrieve(latest_url)
            with open(path) as json_file:
                self.latest = json.load(json_file)["dev"]  # should be configurable between dev and stable

        if sys.platform == "win32":
            env_spec_url = base_url + "dev/windows/win-environment-" + self.latest + ".txt"
        elif sys.platform == "darwin":
            env_spec_url = base_url + "dev/macos/mac-environment-" + self.latest + ".txt"
        else:
            raise OSError
        path, _ = urllib.request.urlretrieve(env_spec_url)

        return path

    def set_config_file(self):
        # create installed file as a flag that installation was successful
        with open(os.path.join(paths.ROOT, "config"), "w") as file:
            data = {
                "launcher": {
                    "launcher_version": "0.0.0",
                    "ab_version": self.latest,
                    "ignored_updates": [],
                    "branch": "dev"
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
    from ab_launcher.launch import launch

    setupper = Setup()
    spec_file = setupper.download_env_spec()

    specs = setupper.parse_env_spec(spec_file)

    explicit_updater(specs, Splash())

    setupper.post_install()

    setupper.set_config_file()

    launch()

