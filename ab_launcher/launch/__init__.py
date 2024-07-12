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

    if os.path.isfile(os.path.join(paths.LOCAL, "assets", "windows.py")):
        runner = os.path.join(paths.LOCAL, "assets", "windows.py")
    else:
        runner = windows.__file__

    launcher = subprocess.Popen(
        [paths.ENV_PY_DIR, runner],
        stdout=subprocess.PIPE,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
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
            splash.notify(anchors.pop(0), False)
            stream = ""

    if sys.stdout:
        sys.stdout.write("\n")

    splash.after(2000, splash.destroy)

    launcher.wait()


if sys.platform == "darwin":
    launch = macos.macos_launch
else:
    launch = windows_launch

