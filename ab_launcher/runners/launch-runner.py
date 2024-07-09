
def import_modules():
    print("Loading numpy")
    import numpy

    print("Loading pandas")
    import pandas

    print("Loading PySide2")
    import PySide2

    print("Loading bw2data")
    import bw2data

    print("Loading bw2io")
    import bw2io

    print("Loading bw2calc")
    import bw2calc

    print("Loading Activity Browser")
    import activity_browser

    print("Done")

def launch():
    from activity_browser import run_activity_browser
    run_activity_browser()



if __name__ == "__main__":
    import_modules()
    launch()
