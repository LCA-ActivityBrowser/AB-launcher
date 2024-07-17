import threading
import os
import sys

import ab_launcher
import ab_launcher.gui.splashscreen as gui


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
    # divert the console subprocess to the right functionality
    if "--abconsole" in sys.argv:
        from ab_launcher.console import console_subprocess
        console_subprocess()
        exit()

    # run with a console if requested through the arguments
    if "-c" in sys.argv or "--console" in sys.argv or os.environ.get("AB_CONSOLE", False):
        from ab_launcher.console import start_console
        console_subprocess = start_console()  # save subprocess from being garbage collected

    manager = Manager()
    manager.start()

    gui.splash.mainloop()

    # if we're on MacOS we will run AB in the main thread, this will make it take over the app icon that we've built for
    if sys.platform == "darwin":
        from activity_browser import run_activity_browser
        run_activity_browser()
