import os
import sys
import subprocess
import urllib.request

from ab_launcher import paths
from ab_launcher.conda_utils import explicit_updater


class Installer:

    def __init__(self, notifier):
        self.notifier = notifier

    def threaded_install(self):
        try:
            spec_file = self.download_env_spec()

            specs = []

            with open(spec_file, 'r') as file:
                for line in file.readlines():
                    if line.startswith('#') or line.startswith('@'):
                        continue
                    specs.append(line.strip())

            explicit_updater(specs, self.notifier)

            if sys.platform == "darwin":
                post_install = subprocess.Popen(
                    [paths.MAC_POST_INSTALL],
                    cwd=paths.LOCAL,
                )
                post_install.wait()

            # create installed file as a flag that installation was successful
            with open(os.path.join(paths.AB_DIR, "installed"), "w") as file:
                file.writelines(["Installed"])

            self.notifier.after(1, self.notifier.install_done, 0)
        except Exception as e:
            self.notifier.after(1, self.notifier.install_done, 1)
            raise e

    def download_env_spec(self):
        self.notifier.undefined_progress()
        self.notifier.notify("Downloading environment specification...")
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

