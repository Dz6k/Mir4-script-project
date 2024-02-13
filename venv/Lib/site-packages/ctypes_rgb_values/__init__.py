import ctypes
from ctypes import Structure, byref
from ctypes.wintypes import LONG, HGDIOBJ, BOOL
from ansi.colour.rgb import rgb256
from ansi.colour import fg, bg, fx
from time import time, sleep
windll = ctypes.LibraryLoader(ctypes.WinDLL)
windll.shcore.SetProcessDpiAwareness(2)
user32 = ctypes.WinDLL("user32", use_last_error=True)
psapi = ctypes.WinDLL("psapi", use_last_error=True)
gdi32 = ctypes.WinDLL("gdi32", use_last_error=True)
gdi32.DeleteObject.argtypes = [HGDIOBJ]
gdi32.DeleteObject.restypes = BOOL
DeleteObject = gdi32.DeleteObject

LM_BUTTON = 0x01
RM_BUTTON = 0x02


def print_full_col(text, colour):
    return "".join(
        list(
            map(
                str,
                (
                    fx.bold,
                    bg.brightwhite,
                    fg.brightwhite,
                    rgb256(colour[0], colour[1], colour[2]),
                    text,
                    bg.brightwhite,
                    fg.brightwhite,
                    fx.bold,
                    fx.reset,
                ),
            )
        )
    )


class POINT(Structure):
    _fields_ = [("x", LONG), ("y", LONG)]


def get_cursor():
    pos = POINT()
    user32.GetCursorPos(byref(pos))
    return pos.x, pos.y


def get_pixel(x, y, hdc=0):
    dc = user32.GetDC(hdc)
    colorref = gdi32.GetPixel(dc, x, y)
    try:
        DeleteObject(dc)
    except Exception as faq:
        print(faq)
        pass
    return colorref


def is_right_mouse_button_pressed():
    return get_key_state(RM_BUTTON) > 1


def is_left_mouse_button_pressed():
    return get_key_state(LM_BUTTON) > 1


def get_key_state(vkey):
    return user32.GetKeyState(vkey)


def rgba(colorref):
    return tuple((colorref & (0xFF << (i * 8))) >> (i * 8) for i in range(4))


def get_rgb_value_iter(rgb_values=True, rgba_values=True, coords=True, time_value=True):
    while True:
        pixx = get_cursor()
        colorref = get_pixel(*pixx)
        colorprint = rgba(colorref)
        yieldstuff = ()
        if rgb_values:
            yieldstuff += (colorprint[:-1],)
        if rgba_values:
            yieldstuff += (colorprint,)
        if coords:
            yieldstuff += (pixx,)
        if time_value:
            yieldstuff += (time(),)

        yield yieldstuff
        print(
            print_full_col(
                str(f"{colorprint} -> {pixx}         "), colour=colorprint[:-1]
            ),
            end="\r",
        )


def get_rgb_values(
    sleeptime=0.0,
    on_left_click=False,
    on_right_click=False,
    rgb_values=True,
    rgba_values=True,
    coords=True,
    time_value=True,
):
    allfa = []
    it = get_rgb_value_iter(
        rgb_values=rgb_values,
        rgba_values=rgba_values,
        coords=coords,
        time_value=time_value,
    )
    try:
        while True:
            if on_left_click and not on_right_click:
                if not is_left_mouse_button_pressed():
                    continue
            elif on_right_click and not on_left_click:
                if not is_right_mouse_button_pressed():
                    continue
            elif on_left_click and on_right_click:
                if not (
                    is_right_mouse_button_pressed() or is_left_mouse_button_pressed()
                ):
                    continue

            try:
                allfa.append(next(it))
                if sleeptime != 0:
                    sleep(sleeptime)
            except Exception:
                continue
            except KeyboardInterrupt:
                return allfa
    except KeyboardInterrupt:
        return allfa

