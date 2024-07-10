import sys
from conda.cli import main


if __name__ == "__main__":
    result = main("create", "-p", sys.argv[1], "--file", sys.argv[2], "--verbose", "--verbose", "--yes")
    sys.exit(result)
