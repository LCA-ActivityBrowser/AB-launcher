import os
import sys
import appdirs

# local files
LOCAL = os.path.split(__file__)[0]

if sys.platform == "win32":
    AB_DIR = appdirs.AppDirs("ActivityBrowser", "pylca").user_data_dir
    ENV_DIR = os.path.join(AB_DIR, "environment")
    PKGS_DIR = os.path.join(AB_DIR, "pkgs")
    ENV_PY_DIR = os.path.join(ENV_DIR, "python.exe")

elif sys.platform == "darwin":
    AB_DIR = os.path.join(LOCAL, "AB")
    ENV_DIR = os.path.join(AB_DIR, "environment")
    PKGS_DIR = os.path.join(AB_DIR, "pkgs")
    ENV_PY_DIR = os.path.join(ENV_DIR, "bin", "python")
