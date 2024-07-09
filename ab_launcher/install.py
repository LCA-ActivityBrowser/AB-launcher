import os
import sys
import tarfile
import subprocess
import multiprocessing
import urllib.request

from ab_launcher import paths


class Installer:

    def __init__(self, notifier):
        self.notifier = notifier

    def threaded_install(self):
        try:
            dl = self.download_base_env()
            self.extract_base_env(dl)

            dl = self.download_env_spec()
            missing_pkgs = self.check_downloaded_packages(dl)
            if missing_pkgs:
                self.download_spec_packages(missing_pkgs)
            self.install_spec_env(dl)

            # create installed file as a flag that installation was successful
            with open(os.path.join(paths.AB_DIR, "installed"), "w") as file:
                file.writelines(["Installed"])

            self.notifier.after(1, self.notifier.install_done, 0)
        except Exception as e:
            self.notifier.after(1, self.notifier.install_done, 1)
            raise e

    def download_base_env(self):

        def report_hook(block_num, block_size, total_size):
            if total_size == 0:
                return
            percent = (block_num * block_size) / total_size * 100
            self.notifier.set_progress(percent)

        self.notifier.set_progress(0)
        self.notifier.notify("Downloading base environment...")

        if sys.platform == "win32":
            base_env_url = "https://github.com/mrvisscher/AB-launcher/raw/ac3dde812d7faac173e65972fefb29ae7b9e476d/ab_launcher/download/win-environment.tar.gz"
        elif sys.platform == "darwin":
            base_env_url = "https://github.com/mrvisscher/AB-launcher/raw/ac3dde812d7faac173e65972fefb29ae7b9e476d/ab_launcher/download/mac-environment.tar.gz"
        else:
            raise OSError
        path, _ = urllib.request.urlretrieve(base_env_url, reporthook=report_hook)
        return path

    def extract_base_env(self, download):
        self.notifier.notify("Extracting base environment tar...")
        self.notifier.undefined_progress()

        with tarfile.open(download) as file:
            file.extractall(paths.ENV_DIR)

    def download_env_spec(self):
        self.notifier.notify("Downloading environment specification...")
        if sys.platform == "win32":
            env_spec_url = "https://github.com/mrvisscher/AB-launcher/raw/ac3dde812d7faac173e65972fefb29ae7b9e476d/ab_launcher/download/win-environment_spec.txt"
        elif sys.platform == "darwin":
            env_spec_url = "https://github.com/mrvisscher/AB-launcher/raw/ac3dde812d7faac173e65972fefb29ae7b9e476d/ab_launcher/download/mac-environment_spec.txt"
        else:
            raise OSError
        path, _ = urllib.request.urlretrieve(env_spec_url)

        # rename to a .txt file, because that's what conda supports
        txt_path = path + ".txt"
        os.rename(path, txt_path)

        return txt_path

    def check_downloaded_packages(self, env_spec_path: str) -> list[tuple]:
        self.notifier.notify("Checking for downloaded packages...")
        spec_packages = []

        try:
            os.mkdir(paths.PKGS_DIR)
        except FileExistsError:
            pass

        with open(env_spec_path, "r") as file:
            for line in file.readlines():
                if line.startswith('#') or line.startswith('@'):
                    continue

                line = line.strip()
                spec_package = line.split('/')[-1]
                if spec_package in os.listdir(paths.PKGS_DIR):
                    continue
                spec_packages.append((spec_package, line))

        return spec_packages

    def download_spec_packages(self, spec_packages: list[tuple]):
        self.notifier.notify("Downloading necessary packages")
        self.notifier.set_progress(0)
        fin_queue = multiprocessing.Manager().Queue()
        finished = []

        with multiprocessing.Pool(os.cpu_count()) as pool:
            mapping = [(x, y, fin_queue) for x, y in spec_packages]
            pool.map_async(download_worker, mapping, error_callback=print)

            while len(finished) < len(spec_packages):
                percent = (len(finished) / len(spec_packages)) * 100
                self.notifier.set_progress(percent)

                finished.append(fin_queue.get())

    def install_spec_env(self, env_spec_path: str):
        self.notifier.notify("Installing packages")
        self.notifier.undefined_progress()

        installer = subprocess.Popen(
            [paths.PY_DIR, paths.INSTALL, env_spec_path],
            stdout=subprocess.PIPE,
            text=True
        )

        stream = ""
        anchors = ["Collecting package metadata",
                   "Solving environment",
                   "Preparing transaction",
                   "Verifying transaction",
                   "Executing transaction",
                   ]

        while installer.poll() is None:
            char = installer.stdout.read(1)
            sys.stdout.write(char)
            stream += char
            if anchors and anchors[0] in stream:
                self.notifier.notify(anchors.pop(0), False)
                stream = ""

        if installer.poll() != 0:
            raise Exception("Conda install failed")


def download_worker(arg):
    package_name, url, fin_queue = arg
    urllib.request.urlretrieve(url, os.path.join(paths.PKGS_DIR, package_name))
    print(f"Downloaded {package_name}")
    fin_queue.put(package_name)

