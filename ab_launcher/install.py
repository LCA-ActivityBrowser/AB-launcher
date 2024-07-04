import os
import tarfile
import threading
import subprocess
from tkinter import Tk, ttk

from ab_launcher import LOCAL, INSTALL
from ab_launcher.main import ENV_DIR, PY_DIR


def install():
    # Create the main window
    root = Tk()
    root.title("Installing Activity Browser")

    # Create and place the label
    label = ttk.Label(root, text="Unpacking")
    label.pack(pady=20)

    thread = threading.Thread(target=threaded_install, args=(label, root,))
    thread.start()

    # Return when the thread is finished and the mainloop is destroyed
    return root.mainloop()


def threaded_install(label, root):
    dl = download_base_env(label)
    extract_base_env(label, dl)
    install_spec_env(label)

    root.after(1000, root.destroy)


def download_base_env(label):
    print("Downloading base environment...")
    label.config(text="Downloading base environment...")

    return os.path.join(LOCAL, "download", "environment.tar.gz")


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
