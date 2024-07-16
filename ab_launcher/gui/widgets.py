import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk


class SpecialProgressBar(ttk.Frame):
    going = "right"
    looping = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        s = ttk.Style()
        s.configure('blue.TFrame', background='#0070c0')
        s.configure('red.TFrame', background='#c00000')

        self.configure(
            height=10,
            width=500
        )

        self.inner = ttk.Frame(
            self,
            height=10,
            width=500,
            style='blue.TFrame'
        )

        self.inner.place(x=100, y=0)

        self.loop()

    def loop(self):
        if self.going == "right":
            new = int(self.inner.place_info()['x']) + 1
            self.inner.place(x=new)
            if new > 500:
                self.going = "left"
                self.inner.configure(style="red.TFrame")
        if self.going == "left":
            new = int(self.inner.place_info()['x']) - 1
            self.inner.place(x=new)
            if new < -500:
                self.going = "right"
                self.inner.configure(style="blue.TFrame")

        if self.looping:
            self.after(1, self.loop)

    def set(self, progress: int):
        x_place = int((progress * 5) - 500)
        self.inner.place(x=x_place)


class SpecialButton(ttk.Label):
    blue = '#0070c0'
    red = '#c00000'

    def __init__(self, callback=lambda: None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

        self.configure(cursor="hand2", padding=5, background=self.blue, foreground="white")

        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_leave)
        self.bind("<ButtonRelease>", self.clicked)

    def set_text(self, text: str):
        self.config(text=text)

    def mouse_enter(self, event):
        self.config(background=self.red)

    def mouse_leave(self, event):
        self.config(background=self.blue)

    def clicked(self, event):
        self.callback()


class SpecialLink(ttk.Label):
    def __init__(self, callback=lambda: None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback = callback

        font = tkFont.Font(self, self.cget("font"))
        font.configure(underline=True, size=10)

        self.configure(cursor="hand2", padding=5, foreground='#0070c0', background='white', font=font)

    def set_text(self, text: str):
        self.config(text=text)

    def clicked(self, event):
        self.callback()


class ButtonLayout(ttk.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        s = ttk.Style()
        s.configure('white.TFrame', background='white')

        self.configure(style="white.TFrame")

    def add_button(self, button_text="", button_type=SpecialButton, callback=lambda: None):
        button = button_type(callback, self)
        button.set_text(button_text)
        button.pack(side="right", padx=5)


if __name__ == "__main__":
    from ab_launcher.gui.splashscreen import splash

    splash.ask("Update available", ("Update now", None), ("Update later", None))

    splash.mainloop()

