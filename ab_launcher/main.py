import threading
import os
import sys
import multiprocessing

import ab_launcher
import ab_launcher.gui.splashscreen as gui


class Manager(threading.Thread):

    def run(self):
        if ab_launcher.SETUP:
            gui.Splash().ask("First setup, this may take a while", ("Install now", do_setup))
        elif ab_launcher.UPDATE:
            gui.Splash().ask("Update available", ("Install now", do_setup), ("Install later", do_launch))
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
    multiprocessing.freeze_support()

    # run with a console if requested through the arguments
    if "-c" in sys.argv or "--console" in sys.argv or os.environ.get("AB_CONSOLE", False):
        from ab_launcher.console import start_console
        console_subprocess = start_console()  # save subprocess from being garbage collected

    splash = gui.Splash()
    manager = Manager()
    manager.start()

    splash.mainloop()

    # if we're on MacOS we will run AB in the main thread, this will make it take over the app icon that we've built for
    if sys.platform == "darwin":
        from activity_browser import run_activity_browser
        run_activity_browser()
