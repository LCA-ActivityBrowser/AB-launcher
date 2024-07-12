# macos can set the right environmental variables and launch from the main thread
import importlib
import sys

from ab_launcher import paths
from ab_launcher.gui.splashscreen import splash

post = ['\\python311.zip', '\\DLLs', '\\Lib', '', '\\Lib\\site-packages', '\\Lib\\site-packages\\win32', '\\Lib\\site-packages\\win32\\lib', '\\Lib\\site-packages\\Pythonwin', ]


def macos_launch():
    splash.notify("Setting environment")
    splash.undefined_progress()

    for path in reversed(post):
        sys.path.insert(0, paths.ENV_DIR + path)

    importlib.invalidate_caches()

    splash.notify("Loading numpy")
    import numpy

    splash.notify("Loading pandas")
    import pandas

    splash.notify("Loading PySide2")
    import PySide2

    splash.notify("Loading bw2data")
    import bw2data

    splash.notify("Loading bw2io")
    import bw2io

    splash.notify("Loading bw2calc")
    import bw2calc

    splash.notify("Launching Activity Browser")
    splash.set_progress(100)

    splash.after(2000, splash.destroy)