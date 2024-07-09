import os
import appdirs

# local files
LOCAL = os.path.split(__file__)[0]

# runners
INSTALL = os.path.join(LOCAL, "runners", "install-runner.py")
LAUNCH = os.path.join(LOCAL, "runners", "launch-runner.py")

# dirs
AB_DIR = appdirs.AppDirs("ActivityBrowser", "pylca").user_data_dir
ENV_DIR = os.path.join(AB_DIR, "environment")
PY_DIR = os.path.join(ENV_DIR, "python.exe")
PKGS_DIR = os.path.join(AB_DIR, "pkgs")
