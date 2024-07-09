import tkinter as tk
from tkinter import ttk
import os
import threading

from ab_launcher import paths


def env_exists() -> bool:
    if not os.path.isdir(paths.AB_DIR):
        os.makedirs(paths.AB_DIR, exist_ok=True)
        return False

    if not os.path.isfile(os.path.join(paths.AB_DIR, "installed")):
        return False

    return True


class Main(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.overrideredirect(True)
        self.configure(background="white")

        # Set splash image
        img = tk.PhotoImage(file=os.path.join(paths.LOCAL, "assets", "splash.png"))
        panel = ttk.Label(self, image=img, background="white")
        panel.image = img
        panel.pack()

        # Create and pack the label
        self.label = ttk.Label(self, text="Launcher Version: 0.0.0", background="white")
        self.label.pack(fill="x", expand=1)

        # Create and pack the install button
        self.install_button = ttk.Button(self, text="Install", command=self.install_confirmed)

        # Create (but don't pack) the progress bar
        self.progress = tk.IntVar()
        self.progress_bar = ttk.Progressbar(self, maximum=100, variable=self.progress)

    def mainloop(self, n=0):
        if not env_exists():
            self.install()
        else:
            self.progress_bar.pack(fill="x", expand=1)
            self.launch()
        super().mainloop(n)

    def install(self):
        self.install_button.pack(pady=5)

    def install_confirmed(self):
        from ab_launcher.install import Installer

        installer = Installer(self)

        self.install_button.destroy()
        self.progress_bar.pack(fill="x", expand=1)
        threading.Thread(target=installer.threaded_install).start()

    def install_done(self, code: int):
        if code != 0:
            self.notify("Installation failed...")
            self.after(5000, self.destroy)
        else:
            self.launch()

    def launch(self):
        from ab_launcher.launch import Launcher

        launcher = Launcher(self)
        threading.Thread(target=launcher.threaded_launch).start()

    def launch_done(self):
        self.after(1000, self.destroy)

    def notify(self, message, also_print=True):
        if also_print:
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


if __name__ == "__main__":
    Main().mainloop()
