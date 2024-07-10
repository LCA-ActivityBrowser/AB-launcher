import subprocess
import sys

from ab_launcher import paths, main


class Launcher:

    def __init__(self, notifier: main.Main):
        self.notifier: main.Main = notifier

    def threaded_launch(self):
        self.notifier.notify("Loading packages")
        self.notifier.undefined_progress()

        flags = 0
        if sys.platform == "win32":
            flags = subprocess.CREATE_NO_WINDOW

        launcher = subprocess.Popen(
            [paths.PY_DIR, paths.LAUNCH],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=flags,
        )

        stream = ""
        anchors = ["Loading numpy",
                   "Loading pandas",
                   "Loading PySide2",
                   "Loading bw2data",
                   "Loading bw2io",
                   "Loading bw2calc",
                   "Loading Activity Browser",
                   "Done"
                   ]

        while anchors:
            char = launcher.stdout.read(1)
            if sys.stdout:
                sys.stdout.write(char)
            stream += char
            if anchors and anchors[0] in stream:
                self.notifier.notify(anchors.pop(0), False)
                stream = ""

        if sys.stdout:
            sys.stdout.write("\n")

        self.notifier.launch_done()

