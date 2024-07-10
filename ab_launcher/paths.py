import os
import sys
import appdirs

# local files
LOCAL = os.path.split(__file__)[0]

# runners
INSTALL = os.path.join(LOCAL, "runners", "install-runner.py")
LAUNCH = os.path.join(LOCAL, "runners", "launch-runner.py")

# dirs
AB_DIR = appdirs.AppDirs("ActivityBrowser", "pylca").user_data_dir
BASE_DIR = os.path.join(AB_DIR, "base")
ENV_DIR = os.path.join(AB_DIR, "environment")
PKGS_DIR = os.path.join(AB_DIR, "pkgs")

if sys.platform == "win32":
    ENV_PY_DIR = os.path.join(ENV_DIR, "python.exe")
    BASE_PY_DIR = os.path.join(BASE_DIR, "python.exe")
elif sys.platform == "darwin":
    ENV_PY_DIR = os.path.join(ENV_DIR, "bin", "python")
    BASE_PY_DIR = os.path.join(BASE_DIR, "bin", "python")

