# windows needs to launch from a subprocess directed from the environmental python.exe

def import_modules():
    print("Loading numpy", flush=True)
    import numpy

    print("Loading pandas", flush=True)
    import pandas

    print("Loading PySide2", flush=True)
    import PySide2

    print("Loading bw2data", flush=True)
    import bw2data

    print("Loading bw2io", flush=True)
    import bw2io

    print("Loading bw2calc", flush=True)
    import bw2calc

    print("Loading Activity Browser", flush=True)
    import activity_browser

    print("Done", flush=True)

def launch():
    from activity_browser import run_activity_browser
    run_activity_browser()

if __name__ == "__main__":
    import_modules()
    launch()
