import sys
import tkinter as tk
from tkinter import ttk
import os
import threading

from ab_launcher import paths, utils, widgets


def env_exists() -> bool:
    if not os.path.isdir(paths.AB_DIR):
        os.makedirs(paths.AB_DIR, exist_ok=True)
        return False

    if not os.path.isfile(os.path.join(paths.AB_DIR, "installed")):
        return False

    return True


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
        self.label.place(x=10, y=257)

        # Create and pack the install button
        self.install_button = ttk.Button(self, text="Install Activity Browser", command=self.install_confirmed)

        # Create (but don't pack) the progress bar
        self.progress_bar = widgets.SpecialProgressBar()

        self.center_window()

        # if sys.platform == "win32":
        #     self.center_window()
        # else:
        #     self.geometry('500x320+100+100')

    def center_window(self):
        x, y = utils.get_active_screen_center()
        self.geometry(f'500x293+{x-250}+{y-150}')

    def mainloop(self, n=0):
        if not env_exists():
            self.install()
        else:
            self.progress_bar.place(x=0, y=285)
            self.launch()
        super().mainloop(n)

    def install(self):
        self.install_button.place(x=350, y=250)

    def install_confirmed(self):
        from ab_launcher.install import Installer

        installer = Installer(self)

        self.install_button.destroy()
        self.progress_bar.place(x=0, y=285)
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
        if self.progress_bar.looping:
            return
        self.progress_bar.looping = True
        self.progress_bar.loop()

    def set_progress(self, progress: float):
        self.progress_bar.looping = False
        self.progress_bar.set(int(progress))


if __name__ == "__main__":
    Main().mainloop()
