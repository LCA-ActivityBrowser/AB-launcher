import subprocess
import sys

from ab_launcher import paths, main


class Launcher:

    def __init__(self, notifier: main.Main):
        self.notifier: main.Main = notifier

    def threaded_launch(self):
        self.notifier.notify("Installing packages")
        self.notifier.undefined_progress()

        launcher = subprocess.Popen(
            [paths.PY_DIR, paths.LAUNCH],
            stdout=subprocess.PIPE,
            text=True
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
            sys.stdout.write(char)
            stream += char
            if anchors and anchors[0] in stream:
                self.notifier.notify(anchors.pop(0), False)
                stream = ""

        sys.stdout.write("\n")
        launcher.stdout = sys.stdout

        self.notifier.launch_done()

