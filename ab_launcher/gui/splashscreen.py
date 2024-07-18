import os
import functools

import tkinter as tk
from tkinter import ttk

from ab_launcher import paths
from ab_launcher.gui import utils, widgets


class SingletonMeta(type):
    """
    A metaclass that creates a Singleton base class when called.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Splash(tk.Tk, metaclass=SingletonMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set window properties
        self.overrideredirect(True)
        self.configure(background="white", highlightcolor="lightgrey", highlightthickness=3)

        style = ttk.Style(self)
        style.theme_use('classic')

        # Set splash image
        img = tk.PhotoImage(file=os.path.join(paths.LOCAL, "assets", "splash.png"))
        panel = ttk.Label(self, image=img)
        panel.image = img
        panel["background"] = "white"
        panel.pack()

        # Create and place the label
        self.label = ttk.Label(self, text="Launcher Version: 0.0.0", background="white")
        self.label.configure(background="white")
        self.label.place(x=10, y=275, anchor="sw")

        # Create and place the progress bar
        self.progress_bar = widgets.SpecialProgressBar(self)
        self.progress_bar.place(x=-3, y=293, anchor="sw")

        # Center the window in the active screen
        x, y = utils.get_active_screen_center()
        self.geometry(f'500x293+{x - 250}+{y - 150}')

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

    def ask(self, question: str, option: tuple[str, callable], *args):
        def answered(callback):
            buttons.destroy()
            callback()

        self.notify(question)
        self.set_progress(100)

        buttons = widgets.ButtonLayout(self)
        buttons.place(x=495, y=275, anchor='se')

        buttons.add_button(option[0], callback=functools.partial(answered, option[1]))

        for other_option in args:
            buttons.add_button(
                other_option[0],
                widgets.SpecialLink,
                callback=functools.partial(answered, other_option[1])
            )

