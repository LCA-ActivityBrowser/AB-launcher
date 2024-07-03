import os
import sys
from tkinter import Tk, ttk

import appdirs
import tarfile
import subprocess
import threading
import io

# local files
LOCAL = os.path.split(__file__)[0]
INSTALL = os.path.join(LOCAL, "install.py")
LAUNCH = os.path.join(LOCAL, "launch.py")

# appdata dirs
AB_DIR = appdirs.AppDirs("ActivityBrowser", "pylca").user_data_dir
ENV_DIR = os.path.join(AB_DIR, "environment")
PKGS_DIR = os.path.join(AB_DIR, "pkgs")

if sys.platform == "win32":
    PY_DIR = os.path.join(ENV_DIR, "python.exe")
elif sys.platform == "darwin":
    PY_DIR = os.path.join(ENV_DIR, "bin", "python")
else:
    raise OSError

os.environ["CONDA_PKGS_DIRS"] = PKGS_DIR
os.environ["CONDA_REGISTER_ENVS"] = "false"


def env_exists() -> bool:
    if not os.path.isdir(AB_DIR):
        os.makedirs(AB_DIR, exist_ok=True)
        return False

    if not os.path.isfile(PY_DIR):
        return False

    return True


def install_base_env() -> bool:
    # Create the main window
    root = Tk()
    root.title("Installing base environment")

    # Create and place the label
    label = ttk.Label(root, text="Unpacking")
    label.pack(pady=20)

    thread = threading.Thread(target=threaded_install, args=(label, root,))
    thread.start()

    root.after(2000, check_thread, thread, root)

    # Run the Tkinter event loop
    root.mainloop()

    return env_exists()


def check_thread(thread: threading.Thread, root):
    if not thread.is_alive():
        root.after(1, root.destroy)


def threaded_install(label, root):
    dl = download_base_env(label)
    extract_base_env(label, dl)
    install_spec_env(label)
    root.destroy()
    print("Root destroyed")


def download_base_env(label):
    print("Downloading base environment...")
    label.config(text="Downloading base environment...")

    if sys.platform == "win32":
        return os.path.join(LOCAL, "download", "win-environment.tar.gz")
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


# launch as a subprocess
if __name__ == "__main__":
    if not env_exists():
        install_base_env()

    launcher = subprocess.Popen(
        [PY_DIR, LAUNCH],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    launcher.wait()
