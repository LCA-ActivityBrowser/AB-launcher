import sys
from conda.cli import main
from conda.base import context


if __name__ == "__main__":
    context.always_copy = False
    context.always_softlink = True
    result = main("create", "-p", sys.argv[1], "--file", sys.argv[2], "--verbose", "--verbose", "--yes")
    sys.exit(result)
