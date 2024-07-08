import os
import sys
import tarfile
import threading
import subprocess
import urllib.request
from tkinter import Tk, ttk, IntVar

from ab_launcher import LOCAL, INSTALL
from ab_launcher.main import ENV_DIR, PY_DIR, AB_DIR


class InstallationNotifier(Tk):
    def __init__(self, install_fn):
        super().__init__()

        self.install_fn = install_fn

        # Set window title and size
        self.title("Installation")
        self.geometry("300x100")
        self.iconbitmap(os.path.join(LOCAL, "assets", "activity-browser.ico"))

        # Make the window non-resizable
        self.resizable(False, False)

        # Create and pack the label
        self.label = ttk.Label(self, text="You are about to install the Activity Browser.")
        self.label.pack(pady=10)

        # Create and pack the install button
        self.install_button = ttk.Button(self, text="Install", command=self.confirmed)
        self.install_button.pack(pady=5)

        # Create (but don't pack) the progress bar
        self.progress = IntVar()
        self.progress_bar = ttk.Progressbar(self, maximum=100, variable=self.progress)

    def confirmed(self):
        self.install_button.destroy()
        self.progress_bar.pack(padx=10, fill="x", expand=1)
        threading.Thread(target=self.install_fn).start()

    def success(self):
        self.progress_bar.destroy()
        self.notify("Installation successful")
        launch_button = ttk.Button(self, text="Launch the Activity Browser", command=self.destroy)
        launch_button.pack(pady=5)

    def notify(self, message):
        print(message)
        self.label.config(text=message)

    def undefined_progress(self):
        setattr(self.progress_bar, "undefined_progress", True)
        self.progress_bar.config(mode="indeterminate")
        self.progress_bar.start(5)
        self.progress.set(0)

    def set_progress(self, progress: float):
        if getattr(self.progress_bar, "undefined_progress", False):
            setattr(self.progress_bar, "undefined_progress", False)
            self.progress_bar.config(mode="determinate")
            self.progress_bar.stop()
        self.progress.set(int(progress))


class Installer:

    def __init__(self):
        self.exit_code = 0
        self.notifier = InstallationNotifier(self.threaded_install)

    def start(self):
        self.notifier.mainloop()
        return self.exit_code

    def quit(self, code):
        self.exit_code = code
        if code == 0:
            self.notifier.success()
        else:
            self.notifier.notify("Installation failed")

    def threaded_install(self):
        try:
            dl = self.download_base_env()
            self.extract_base_env(dl)

            dl = self.download_env_spec()
            self.install_spec_env(dl)

            # create installed file as a flag that installation was successful
            with open(os.path.join(AB_DIR, "installed"), "w") as file:
                file.writelines(["Installed"])

            self.quit(0)
        except:
            self.quit(1)

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
            file.extractall(ENV_DIR)

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

    def install_spec_env(self, path):
        installer = subprocess.Popen(
            [PY_DIR, INSTALL, path],
            stdout=subprocess.PIPE,
            text=True
        )

        stream = ""
        line = ""
        anchors = ["Collecting package metadata",
                   "Solving environment",
                   "Preparing transaction",
                   "Verifying transaction",
                   "Executing transaction",
                   ]

        while installer.poll() is None:
            char = installer.stdout.read(1)
            line += char
            stream += char

            if char == '' and installer.poll() is not None:
                break
            if char in ('\n', '\r'):
                if line:
                    print(line)
                    line = ''
            if anchors and anchors[0] in stream:
                self.notifier.notify(anchors.pop(0))

        if installer.poll() != 0:
            raise Exception("Conda install failed")


def install():
    return Installer().start()

