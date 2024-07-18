import multiprocessing
import multiprocessing.connection
import sys
import threading
import time

import tkinter as tk
from tkinter import scrolledtext


class Console(tk.Tk):
    def __init__(self, connection: multiprocessing.connection.Connection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn = connection

        self.title("AB Console")

        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED, background="black", foreground="white")
        self.text.pack(expand=1, fill=tk.BOTH)

        threading.Thread(target=self.capture).start()

    def capture(self):
        while True:
            line = self.conn.recv()

            # break if the widget has been destroyed in the meantime
            try:
                self.winfo_exists()
            except RuntimeError:
                break

            # close console on this escape sequence
            if line == "[0m":
                self.after(1, self.destroy)
                break

            self.text.config(state=tk.NORMAL)
            self.text.insert(tk.END, line)
            self.text.config(state=tk.DISABLED)


class WriteableConnection:
    def __init__(self, connection: multiprocessing.connection.Connection):
        self.conn = connection

    def write(self, __s):
        self.conn.send(__s)


def start_console():
    pipe_in, pipe_out = multiprocessing.Pipe()

    # start the multiprocessing subprocess
    multiprocessing.Process(
        target=console_subprocess,
        args=[pipe_out],
        daemon=True,
    ).start()

    # append the pipe of the console subprocess to the multioutput stdout and stderr. This way all stdout and stderr
    # will be redirected to the subprocess' pipe
    sys.stdout.outputs.append(WriteableConnection(pipe_in))
    sys.stderr.outputs.append(WriteableConnection(pipe_in))

    # wait for the console to launch (to lazy to bother creating a signal)
    time.sleep(1)


def console_subprocess(connection: multiprocessing.connection.Connection):
    Console(connection).mainloop()

