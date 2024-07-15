import os

from ab_launcher import paths

SETUP = not os.path.isfile(os.path.join(paths.AB_DIR, "config"))
UPDATE = False

