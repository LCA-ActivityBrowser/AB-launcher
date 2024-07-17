import subprocess
import threading
import sys
import os
import io

import ab_launcher
import ab_launcher.gui.splashscreen as gui

# set conda environmental variables
os.environ["CONDA_PREFIX"] = ab_launcher.paths.ENV_DIR
os.environ["CONDA_PKGS_DIRS"] = ab_launcher.paths.PKGS_DIR
os.environ["CONDA_REGISTER_ENVS"] = "false"
os.environ["CONDA_EXE"] = ""
os.environ["CONDA_PYTHON_EXE"] = ""
os.environ["CONDA_DEFAULT_ENV"] = ""
os.environ["CONDA_ROOT"] = ""

# stdio fallbacks when built without terminal
if not sys.stdout:
    sys.stdout = io.StringIO()
    sys.stdin = io.StringIO()
    sys.stderr = io.StringIO()


class Manager(threading.Thread):

    def run(self):
        if ab_launcher.SETUP:
            gui.splash.ask("First setup, this may take a while", ("Install now", do_setup))
        elif ab_launcher.UPDATE:
            gui.splash.ask("Update available", ("Install now", do_setup), ("Install later", do_launch))
        else:
            do_launch()


def do_setup():
    from ab_launcher.setup import setup

    thread = threading.Thread(
        name="setup",
        target=setup
    )
    thread.start()


def do_launch():
    from ab_launcher.launch import launch

    thread = threading.Thread(
        name="launch",
        target=launch
    )
    thread.start()


if __name__ == "__main__":
    manager = Manager()
    manager.start()

    gui.splash.mainloop()

    # if we're on MacOS we will run AB in the main thread, this will make it take over the app icon that we've built for
    if sys.platform == "darwin":
        from activity_browser import run_activity_browser
        run_activity_browser()
