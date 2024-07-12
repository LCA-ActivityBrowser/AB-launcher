import tkinter as tk
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





