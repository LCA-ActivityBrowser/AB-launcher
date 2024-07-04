import os

# local files
LOCAL = os.path.split(__file__)[0]

# runners
INSTALL = os.path.join(LOCAL, "runners", "install-runner.py")
LAUNCH = os.path.join(LOCAL, "runners", "launch-runner.py")

