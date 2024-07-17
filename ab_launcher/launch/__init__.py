import sys
import subprocess
import os

from ab_launcher import paths
from ab_launcher.gui.splashscreen import splash
from ab_launcher.launch import windows
from ab_launcher.launch import macos


def windows_launch():
    splash.notify("Loading packages")
    splash.undefined_progress()

    # find the python file we will start the subprocess on
    # it's either in the assets folder (when built to an .exe)
    if os.path.isfile(os.path.join(paths.LOCAL, "assets", "windows.py")):
        runner = os.path.join(paths.LOCAL, "assets", "windows.py")
    # or we can just take the one right here (maybe also works when built to exe)
    else:
        runner = windows.__file__

    # open a subprocess, combine stdout and stderr, and make sure to create no window
    launcher = subprocess.Popen(
        [paths.ENV_PY_DIR, runner],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )

    # different stages we encounter throughout the loading process
    anchors = ["Loading numpy",
               "Loading pandas",
               "Loading PySide2",
               "Loading bw2data",
               "Loading bw2io",
               "Loading bw2calc",
               "Loading Activity Browser",
               "Done"
               ]

    # while there are anchors iterate over them to show progress
    while anchors:
        line = launcher.stdout.readline()
        if anchors and anchors[0] in line:
            splash.notify(anchors.pop(0), False)
        sys.stdout.write(line)

    # if all anchors are gone, it means loading is done and we can destroy the splashscreen
    splash.after(2000, splash.destroy)

    # keep redirecting the stdout/err of the subprocess to our stdout to make them show up in the debug window
    # and our own console
    while launcher.poll() is None:
        line = launcher.stdout.readline()
        sys.stdout.write(line)


if sys.platform == "darwin":
    launch = macos.macos_launch
else:
    launch = windows_launch

