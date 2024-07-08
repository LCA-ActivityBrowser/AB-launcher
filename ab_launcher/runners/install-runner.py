import sys
from conda.cli import main


if __name__ == "__main__":
    main("env", "update", "--prune", "--file", sys.argv[1], "--name", "base", "--quiet")
