import os
import sys
import tarfile
import threading
import subprocess
import urllib.request
from tkinter import Tk, ttk

from ab_launcher import LOCAL, INSTALL
from ab_launcher.main import ENV_DIR, PY_DIR, AB_DIR


class InstallationNotifier(Tk):
    def __init__(self):
        super().__init__()

        # Set window title and size
        self.title("Installation")
        self.geometry("300x100")

        # Make the window non-resizable
        self.resizable(False, False)

        # Create and pack the label
        self.label = ttk.Label(self, text="You are about to install the Activity Browser.")
        self.label.pack(pady=10)

        # Create and pack the install button
        self.install_button = ttk.Button(self, text="Install", command=self.confirmed)
        self.install_button.pack(pady=5)

    def confirmed(self):
        self.install_button.destroy()
        threading.Thread(target=self.in_thread).start()

    def in_thread(self):
        dl = download_base_env(self.label)
        extract_base_env(self.label, dl)
        install_spec_env(self.label)

        # create installed file as a flag that installation was succesful
        with open(os.path.join(AB_DIR, "installed"), "w") as file:
            file.writelines(["Installed"])

        self.after(1000, self.destroy)


def install():
    InstallationNotifier().mainloop()

    return


def download_base_env(label):
    print("Downloading base environment...")
    label.config(text="Downloading base environment...")

    if sys.platform == "win32":
        base_env_url = "https://github.com/mrvisscher/AB-launcher/raw/ac3dde812d7faac173e65972fefb29ae7b9e476d/ab_launcher/download/win-environment.tar.gz"
        path, _ = urllib.request.urlretrieve(base_env_url)
        return path
    elif sys.platform == "darwin":
        return os.path.join(LOCAL, "download", "mac-environment.tar.gz")
    else:
        raise OSError


def extract_base_env(label, download):
    print("Extracting base environment tar...")
    label.config(text="Extracting base environment tar...")

    with tarfile.open(download) as file:
        file.extractall(ENV_DIR)


def install_spec_env(label):
    installer = subprocess.Popen(
        [PY_DIR, INSTALL],
        stdout=subprocess.PIPE,
        text=True
    )

    line = ''
    while installer.poll() is None:
        char = installer.stdout.read(1)
        if char == '' and installer.poll() is not None:
            break
        if char in ('\n', '\r'):
            if line:
                label.config(text=line)
                print(line)
                line = ''
        else:
            line += char
            label.config(text=line)
