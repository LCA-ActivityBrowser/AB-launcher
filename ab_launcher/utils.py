import sys
import argparse


def win_get_display():
    import typing as T
    import ctypes
    import ctypes.wintypes

    CCHDEVICENAME = 32
    # gdi32.GetDeviceCaps keys for monitor size in mm
    HORZSIZE = 4
    VERTSIZE = 6

    MonitorEnumProc = ctypes.WINFUNCTYPE(
        ctypes.c_int,
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(ctypes.wintypes.RECT),
        ctypes.c_double,
    )

    class MONITORINFOEXW(ctypes.Structure):
        _fields_ = [
            ("cbSize", ctypes.wintypes.DWORD),
            ("rcMonitor", ctypes.wintypes.RECT),
            ("rcWork", ctypes.wintypes.RECT),
            ("dwFlags", ctypes.wintypes.DWORD),
            ("szDevice", ctypes.wintypes.WCHAR * CCHDEVICENAME),
        ]

    monitors = []

    def check_primary(rct: T.Any) -> bool:
        return rct.left == 0 and rct.top == 0

    def callback(monitor: T.Any, dc: T.Any, rect: T.Any, data: T.Any) -> int:
        info = MONITORINFOEXW()
        info.cbSize = ctypes.sizeof(MONITORINFOEXW)
        if ctypes.windll.user32.GetMonitorInfoW(monitor, ctypes.byref(info)):
            name = info.szDevice
        else:
            name = None

        h_size = ctypes.windll.gdi32.GetDeviceCaps(dc, HORZSIZE)
        v_size = ctypes.windll.gdi32.GetDeviceCaps(dc, VERTSIZE)

        rct = rect.contents
        monitors.append(
            argparse.Namespace(
                x=rct.left,
                y=rct.top,
                width=rct.right - rct.left,
                height=rct.bottom - rct.top,
                width_mm=h_size,
                height_mm=v_size,
                name=name,
                is_primary=check_primary(rct),
            )
        )
        return 1

    # Make the process DPI aware so it will detect the actual
    # resolution and not a virtualized resolution reported by
    # Windows when DPI virtualization is in use.
    #
    # benshep 2020-03-31: this gives the correct behaviour on Windows 10 when
    # multiple monitors have different DPIs.
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    # On Python 3.8.X GetDC randomly fails returning an invalid DC.
    # To workaround this request a number of DCs until a valid DC is returned.
    for retry in range(100):
        # Create a Device Context for the full virtual desktop.
        dc_full = ctypes.windll.user32.GetDC(None)
        if dc_full > 0:
            # Got a valid DC, break.
            break
        ctypes.windll.user32.ReleaseDC(dc_full)
    else:
        # Fallback to device context 0 that is the whole
        # desktop. This allows fetching resolutions
        # but monitor specific device contexts are not
        # passed to the callback which means that physical
        # sizes can't be read.
        dc_full = 0
    # Call EnumDisplayMonitors with the non-NULL DC
    # so that non-NULL DCs are passed onto the callback.
    # We want monitor specific DCs in the callback.
    ctypes.windll.user32.EnumDisplayMonitors(
        dc_full, None, MonitorEnumProc(callback), 0
    )
    ctypes.windll.user32.ReleaseDC(dc_full)

    yield from monitors


def mac_get_display():
    from AppKit import NSScreen

    screens = NSScreen.screens()

    for screen in screens:
        f = screen.frame
        if callable(f):
            f = f()

        yield argparse.Namespace(
            x=int(f.origin.x),
            y=int(f.origin.y),
            width=int(f.size.width),
            height=int(f.size.height),
            is_primary=check_primary(screens, screen),
        )


def windows_get_mouse_pos():
    from ctypes import windll, Structure, c_long, byref

    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]

    def queryMousePosition():
        pt = POINT()
        windll.user32.GetCursorPos(byref(pt))
        return (pt.x, pt.y)

    pos = queryMousePosition()
    return pos


def mac_get_mouse_pos():
    return
    raise NotImplementedError


def get_active_screen_center():
    pos = get_mouse_pos()
    if not pos:
        return
    for disp in win_get_display():
        if disp.x < pos[0] < disp.x + disp.width and disp.y < pos[1] < disp.y + disp.height:
            x = disp.x + (disp.width / 2)
            y = disp.y + (disp.height / 2)
            return int(x), int(y)


get_display = None
get_mouse_pos = None

if sys.platform == "win32":
    get_display = win_get_display
    get_mouse_pos = windows_get_mouse_pos
elif sys.platform == "darwin":
    get_display = mac_get_display
    get_mouse_pos = mac_get_mouse_pos
