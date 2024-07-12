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

# stdio fallbacks when built without terminal
if not sys.stdout:
    sys.stdout = io.StringIO()
    sys.stdin = io.StringIO()
    sys.stderr = io.StringIO()


class Manager(threading.Thread):

    def run(self):
        if ab_launcher.SETUP:
            do_setup()

        do_launch()


def do_setup():
    from ab_launcher.setup import setup

    thread = threading.Thread(
        name="setup",
        target=setup
    )
    thread.start()
    thread.join()


def do_launch():
    from ab_launcher.launch import launch
    launch()


if __name__ == "__main__":
    manager = Manager()
    manager.start()

    gui.splash.mainloop()

    if sys.platform == "darwin":
        from activity_browser import run_activity_browser
        run_activity_browser()
