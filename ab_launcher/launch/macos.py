# macos can set the right environmental variables and launch from the main thread
import importlib
import sys

from ab_launcher import paths
from ab_launcher.gui.splashscreen import Splash

post = ['/lib/python311.zip', '/lib/python3.11', '/lib/python3.11/lib-dynload', '/lib/python3.11/site-packages']


def macos_launch():
    Splash().notify("Setting environment")
    Splash().undefined_progress()

    for path in reversed(post):
        sys.path.insert(0, paths.ENV_DIR + path)

    importlib.invalidate_caches()

    Splash().notify("Loading numpy")
    import numpy

    Splash().notify("Loading pandas")
    import pandas

    Splash().notify("Loading PySide2")
    import PySide2

    Splash().notify("Loading bw2data")
    import bw2data

    Splash().notify("Loading bw2io")
    import bw2io

    Splash().notify("Loading bw2calc")
    import bw2calc

    Splash().notify("Loading Activity Browser")
    Splash().set_progress(100)

    Splash().after(500, Splash().destroy)
