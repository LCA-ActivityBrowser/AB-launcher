import subprocess

from ab_launcher import paths, main


class Launcher:

    def __init__(self, notifier: main.Main):
        self.notifier: main.Main = notifier

    def threaded_launch(self):
        launcher = subprocess.Popen(
            [paths.PY_DIR, paths.LAUNCH],
        )
