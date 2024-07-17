import subprocess
import sys
import os
import threading

import tkinter as tk
from tkinter import scrolledtext


class Console(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("AB Console")

        self.text = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED, background="black", foreground="white")
        self.text.pack(expand=1, fill=tk.BOTH)

        threading.Thread(target=self.capture).start()

    def capture(self):
        while True:
            line = sys.stdin.readline()
            # close console on this escape sequence
            if line == "[0m":
                self.after(1, self.destroy)
                break

            self.text.config(state=tk.NORMAL)
            self.text.insert(tk.END, line)
            self.text.config(state=tk.DISABLED)


def start_console():
    console = subprocess.Popen(
        [sys.executable, __file__, "--abconsole"],
        stdin=subprocess.PIPE,
        text=True
    )

    # append the stdin of the console subprocess to the multioutput stdout and stderr. This way all stdout and stderr
    # will be redirected to the subprocess' stdin
    sys.stdout.outputs.append(os.fdopen(console.stdin.fileno(), 'w', 1))
    sys.stderr.outputs.append(os.fdopen(console.stdin.fileno(), 'w', 1))

    return console  # return to save subprocess from being garbage collected

def console_subprocess():
    Console().mainloop()


if __name__ == "__main__":
    if "--abconsole" in sys.argv:
        console_subprocess()
        exit()
