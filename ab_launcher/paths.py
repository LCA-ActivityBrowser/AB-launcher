import os
import sys
import appdirs

# local files
LOCAL = os.path.split(__file__)[0]
ROOT = os.path.split(LOCAL)[0]

if sys.platform == "win32":
    ENV_DIR = os.path.join(ROOT, "environment")
    PKGS_DIR = os.path.join(ROOT, "pkgs")
    ENV_PY_DIR = os.path.join(ENV_DIR, "python.exe")

elif sys.platform == "darwin":
    ENV_DIR = os.path.join(ROOT, "environment")
    PKGS_DIR = os.path.join(ROOT, "pkgs")
    ENV_PY_DIR = os.path.join(ENV_DIR, "bin", "python")
