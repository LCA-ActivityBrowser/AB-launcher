import subprocess
import sys
import os
import importlib

from ab_launcher import paths, main

os.environ["CONDA_PREFIX"] = paths.ENV_DIR

redlist = ["logging"]

class Launcher:

    def __init__(self, notifier: main.Main):
        self.notifier: main.Main = notifier

    def threaded_launch(self):
        self.notifier.notify("Setting environment")
        self.notifier.undefined_progress()
        post = ['/lib/python311.zip', '/lib/python3.11', '/lib/python3.11/lib-dynload', '/lib/python3.11/site-packages']

        for path in reversed(post):
            sys.path.insert(0, paths.ENV_DIR + path)

        importlib.invalidate_caches()

        self.notifier.notify("Loading numpy")
        import numpy

        self.notifier.notify("Loading pandas")
        import pandas

        self.notifier.notify("Loading PySide2")
        import PySide2

        self.notifier.notify("Loading bw2data")
        import bw2data

        self.notifier.notify("Loading bw2io")
        import bw2io

        self.notifier.notify("Loading bw2calc")
        import bw2calc

        self.notifier.notify("Launching Activity Browser")
        self.notifier.set_progress(100)

        self.notifier.launch_done()

    def threaded_launch_bak(self):
        self.notifier.notify("Loading packages")
        self.notifier.undefined_progress()

        flags = 0
        if sys.platform == "win32":
            flags = subprocess.CREATE_NO_WINDOW

        launcher = subprocess.Popen(
            [paths.ENV_PY_DIR, paths.LAUNCH],
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

