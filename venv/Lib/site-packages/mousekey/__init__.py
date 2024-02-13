# Thanks to:
# https://stackoverflow.com/questions/62189991/how-to-wrap-the-sendinput-function-to-python-using-ctypes
# https://stackoverflow.com/questions/73941056/how-to-send-mouse-clicks
# https://pywinauto.readthedocs.io/en/latest/
# https://stackoverflow.com/questions/47704008/fastest-way-to-get-all-the-points-between-two-x-y-coordinates-in-python
# https://stackoverflow.com/a/35756376/15096247

import copy
import itertools
import os
import sys
import warnings
from collections import namedtuple
from ctypes import wintypes, Structure, POINTER, Union, byref, sizeof
from ctypes.wintypes import DWORD, WORD, HWND, UINT, WPARAM, LPARAM, LPVOID, BOOL
from math import floor
from random import uniform
import numpy as np
import kthread
import string
import time
import ctypes
import six
import keyboard as key_b
from ctypes_rgb_values import get_rgb_values
from ctypes_window_info import get_window_infos
from flatten_everything import flatten_everything, ProtectedTuple

BlockInput = ctypes.windll.user32.BlockInput
BlockInput.argtypes = [wintypes.BOOL]
BlockInput.restype = wintypes.BOOL

childcounter = sys.modules[__name__]
childcounter.rightnow = None


def get_elements_from_hwnd(hwnd):
    return _get_elements_from_coords(coordx=None, coordy=None, hwnd=hwnd)


def get_elements_from_xy(x, y):
    return _get_elements_from_coords(coordx=x, coordy=y, hwnd=None)


def _get_elements_from_coords(coordx=None, coordy=None, hwnd=None):
    WindowInfoxx = namedtuple(
        "WindowInfo",
        "parent pid title windowtext hwnd length tid status coords_client dim_client coords_win dim_win class_name path",
    )
    oldlen = 0
    newlen = 1
    wholeli = []
    if hwnd is None:
        firstitem = get_all_infos_point(coordx, coordy)
    else:
        firstitem = get_all_infos_point(hwnd_=hwnd)

    firstitem_ = list(set(flatten_everything(firstitem)))
    allh = [
        v
        for v in [
            r[4] if len(r) > 4 else None
            for r in firstitem_
            if isinstance(r, ProtectedTuple)
        ]
        if v is not None
    ]

    while oldlen != newlen:
        oldlen = newlen
        didi = [get_all_infos_point(hwnd_=s) for s in allh]
        newlente = [
            h for h in (set(flatten_everything(didi))) if isinstance(h, ProtectedTuple)
        ]
        allh = [c[4] for c in newlente if len(c) > 4]
        wholeli.append(newlente)
        wholeli = list(set(flatten_everything(wholeli)))
        newlen = len(wholeli)
    df = [WindowInfoxx(*q) for q in (set(flatten_everything(wholeli)))]
    if hwnd is None:
        rv = WindowInfoxx(*firstitem[(coordx, coordy)]["foundelement"])
    else:
        rv = WindowInfoxx(*firstitem[(0, 0)]["foundelement"])

    return {"element": rv, "family": df}


def get_all_infos_point(coordx=None, coordy=None, hwnd_=None):
    TRUE = 1

    class __WindowEnumerator(object):
        """
        Window enumerator class. Used internally by the window enumeration APIs.
        """

        def __init__(self):
            self.hwnd = list()

        def __call__(self, hwnd, lParam):
            ##        print(hwnd  # XXX DEBUG)
            self.hwnd.append(hwnd)
            return TRUE

    def find_elements(hwnd):

        user32 = ctypes.WinDLL("user32")
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

        GetWindowRect = ctypes.windll.user32.GetWindowRect
        GetClientRect = ctypes.windll.user32.GetClientRect
        WindowInfoxx = namedtuple(
            "WindowInfo",
            "parent pid title windowtext hwnd length tid status coords_client dim_client coords_win dim_win class_name path",
        )

        def get_window_text(hWnd):
            length = ctypes.windll.user32.GetWindowTextLengthW(hWnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hWnd, buf, length + 1)
            return buf.value

        class RECT(ctypes.Structure):
            _fields_ = [
                ("left", ctypes.c_long),
                ("top", ctypes.c_long),
                ("right", ctypes.c_long),
                ("bottom", ctypes.c_long),
            ]

        WNDENUMPROCA = ctypes.WINFUNCTYPE(
            BOOL,
            HWND,
            LPARAM,
        )
        result = []

        @WNDENUMPROCA
        def enum_proc2(hWnd, lParam):
            status = "invisible"
            if user32.IsWindowVisible(hWnd):
                status = "visible"
            pid = wintypes.DWORD()
            tid = user32.GetWindowThreadProcessId(hWnd, ctypes.byref(pid))
            length = user32.GetWindowTextLengthW(hWnd) + 1
            title = ctypes.create_unicode_buffer(length)
            user32.GetWindowTextW(hWnd, title, length)
            rect = RECT()
            GetClientRect(hWnd, ctypes.byref(rect))
            left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
            w, h = right - left, bottom - top
            coords_client = left, right, top, bottom
            dim_client = w, h
            rect = RECT()
            GetWindowRect(hWnd, ctypes.byref(rect))
            left, right, top, bottom = rect.left, rect.right, rect.top, rect.bottom
            w, h = right - left, bottom - top
            coords_win = left, right, top, bottom
            dim_win = w, h
            length_ = 257
            title = ctypes.create_unicode_buffer(length_)
            user32.GetClassNameW(hWnd, title, length_)
            classname = title.value
            try:
                windowtext = get_window_text(hWnd)
            except Exception:
                windowtext = ""
            try:
                coa = kernel32.OpenProcess(0x1000, 0, pid.value)
                path = (ctypes.c_wchar * 260)()
                size = ctypes.c_uint(260)
                kernel32.QueryFullProcessImageNameW(coa, 0, path, byref(size))
                filepath = path.value
                ctypes.windll.kernel32.CloseHandle(coa)
            except Exception as fe:
                filepath = ""
            if childcounter.rightnow is None:
                assc = -1
            else:
                assc = childcounter.rightnow
            result.append(
                (
                    WindowInfoxx(
                        assc,
                        pid.value,
                        title.value,
                        windowtext,
                        hWnd,
                        length,
                        tid,
                        status,
                        coords_client,
                        dim_client,
                        coords_win,
                        dim_win,
                        classname,
                        filepath,
                    )
                )
            )
            return True

        enum_proc2(hwnd, 0)
        return result

    def WindowFromPoint(x, y):
        """Return hwnd"""
        x = int(x)
        y = int(y)
        point = POINT()
        point.x = x
        point.y = y

        ac = ctypes.windll.user32.WindowFromPoint(point)
        try:
            return ac

        except Exception as iu:
            print(iu)
            return []

    def GetParent(hWnd):
        _GetParent = ctypes.windll.user32.GetParent
        _GetParent.argtypes = [HWND]
        _GetParent.restype = HWND

        hWndParent = _GetParent(hWnd)
        return hWndParent

    def GetAncestor(hWnd, gaFlags=1):
        _GetAncestor = ctypes.windll.user32.GetAncestor
        _GetAncestor.argtypes = [HWND, UINT]
        _GetAncestor.restype = HWND

        hWndParent = _GetAncestor(hWnd, gaFlags)
        return hWndParent

    def GetDesktopWindow():
        _GetDesktopWindow = ctypes.windll.user32.GetDesktopWindow
        _GetDesktopWindow.argtypes = []
        _GetDesktopWindow.restype = HWND
        return _GetDesktopWindow()

    def get_all_children(parent_hwnd):
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, ctypes.py_object)

        user32 = ctypes.WinDLL("user32")
        user32.GetForegroundWindow.argtypes = ()
        user32.GetForegroundWindow.restype = wintypes.HWND
        user32.EnumChildWindows.argtypes = wintypes.HWND, WNDENUMPROC, ctypes.py_object
        user32.EnumChildWindows.restype = wintypes.BOOL

        @WNDENUMPROC
        def callback(hwnd, obj):
            obj.append(hwnd)
            return True

        obj = []

        user32.EnumChildWindows(parent_hwnd, callback, obj)
        return obj

    if hwnd_ is None:
        pointx = coordx, coordy
        co = WindowFromPoint(*pointx)
    else:
        co = hwnd_
        pointx = 0, 0
    child = find_elements(co)
    dla = GetDesktopWindow()
    child = [c for c in child if c.hwnd != dla]
    didi = {}
    if child:
        didi = {
            pointx: {
                "foundelement": ProtectedTuple(x),
                "all_elements": [ProtectedTuple(e) for e in find_elements(x.hwnd)],
                "ancestor": [ProtectedTuple(rr) for rr in find_elements(gg)]
                if (gg := (GetAncestor(x.hwnd))) is not None
                else None,
                "parent": [ProtectedTuple(h) for h in find_elements(g)]
                if (g := (GetParent(x.hwnd))) is not None
                else None,
                "all_children": [
                    [ProtectedTuple(rr) for rr in find_elements(tra)]
                    for tra in get_all_children(x.hwnd)
                ],
                "whole_family": list(
                    j[0]
                    for j in list(
                        set(
                            flatten_everything(
                                [
                                    ProtectedTuple(m)
                                    for m in [
                                    find_elements(r)
                                    for r in list(
                                        flatten_everything(
                                            [
                                                [
                                                    list(
                                                        set(
                                                            [
                                                                z
                                                                for z in flatten_everything(
                                                                GetParent(p)
                                                            )
                                                                if isinstance(
                                                                z, int
                                                            )
                                                            ]
                                                        )
                                                    )
                                                    for p in flatten_everything(
                                                    [[y.hwnd for y in x]]
                                                )
                                                ]
                                                for x in (
                                                [
                                                    find_elements(tra)
                                                    for tra in get_all_children(
                                                    x.hwnd
                                                )
                                                ]
                                            )
                                            ]
                                        )
                                    )
                                ]
                                ]
                            )
                        )
                    )
                ),
            }
            for x in child
        }
    return didi


def failsafe_kill():
    try:
        os._exit(1)
    except Exception:
        # shouldn't raise an Exception, but "Doppelt hält besser"
        try:
            os.system(f"taskkill /pid {os.getpid()}")
        except Exception:
            pass
        try:
            os.system(f"taskkill /pid {os.getppid()}")
        except Exception:
            pass


def start_failsafe(hotkey="ctrl+e"):
    key_b.add_hotkey(hotkey, failsafe_kill)


SHORT = ctypes.c_short

VK_LBUTTON = 0x01  # Left mouse button
VK_RBUTTON = 0x02  # Right mouse button
VK_CANCEL = 0x03  # Control-break processing
VK_MBUTTON = 0x04  # Middle mouse button (three-button mouse)
VK_XBUTTON1 = 0x05  # X1 mouse button
VK_XBUTTON2 = 0x06  # X2 mouse button
VK_BACK = 0x08  # BACKSPACE key
VK_TAB = 0x09  # TAB key
VK_CLEAR = 0x0C  # CLEAR key
VK_RETURN = 0x0D  # ENTER key
VK_SHIFT = 0x10  # SHIFT key
VK_CONTROL = 0x11  # CTRL key
VK_MENU = 0x12  # ALT key
VK_PAUSE = 0x13  # PAUSE key
VK_CAPITAL = 0x14  # CAPS LOCK key
VK_KANA = 0x15  # IME Kana mode
VK_HANGUEL = 0x15  # IME Hanguel mode (maintained for compatibility; use VK_HANGUL)
VK_HANGUL = 0x15  # IME Hangul mode
VK_JUNJA = 0x17  # IME Junja mode
VK_FINAL = 0x18  # IME final mode
VK_HANJA = 0x19  # IME Hanja mode
VK_KANJI = 0x19  # IME Kanji mode
VK_ESCAPE = 0x1B  # ESC key
VK_CONVERT = 0x1C  # IME convert
VK_NONCONVERT = 0x1D  # IME nonconvert
VK_ACCEPT = 0x1E  # IME accept
VK_MODECHANGE = 0x1F  # IME mode change request
VK_SPACE = 0x20  # SPACEBAR
VK_PRIOR = 0x21  # PAGE UP key
VK_NEXT = 0x22  # PAGE DOWN key
VK_END = 0x23  # END key
VK_HOME = 0x24  # HOME key
VK_LEFT = 0x25  # LEFT ARROW key
VK_UP = 0x26  # UP ARROW key
VK_RIGHT = 0x27  # RIGHT ARROW key
VK_DOWN = 0x28  # DOWN ARROW key
VK_SELECT = 0x29  # SELECT key
VK_PRINT = 0x2A  # PRINT key
VK_EXECUTE = 0x2B  # EXECUTE key
VK_SNAPSHOT = 0x2C  # PRINT SCREEN key
VK_INSERT = 0x2D  # INS key
VK_DELETE = 0x2E  # DEL key
VK_HELP = 0x2F  # HELP key
VK_0 = 0x30  # 0 key
VK_1 = 0x31  # 1 key
VK_2 = 0x32  # 2 key
VK_3 = 0x33  # 3 key
VK_4 = 0x34  # 4 key
VK_5 = 0x35  # 5 key
VK_6 = 0x36  # 6 key
VK_7 = 0x37  # 7 key
VK_8 = 0x38  # 8 key
VK_9 = 0x39  # 9 key
VK_A = 0x41  # A key
VK_B = 0x42  # B key
VK_C = 0x43  # C key
VK_D = 0x44  # D key
VK_E = 0x45  # E key
VK_F = 0x46  # F key
VK_G = 0x47  # G key
VK_H = 0x48  # H key
VK_I = 0x49  # I key
VK_J = 0x4A  # J key
VK_K = 0x4B  # K key
VK_L = 0x4C  # L key
VK_M = 0x4D  # M key
VK_N = 0x4E  # N key
VK_O = 0x4F  # O key
VK_P = 0x50  # P key
VK_Q = 0x51  # Q key
VK_R = 0x52  # R key
VK_S = 0x53  # S key
VK_T = 0x54  # T key
VK_U = 0x55  # U key
VK_V = 0x56  # V key
VK_W = 0x57  # W key
VK_X = 0x58  # X key
VK_Y = 0x59  # Y key
VK_Z = 0x5A  # Z key
VK_LWIN = 0x5B  # Left Windows key (Natural keyboard)
VK_RWIN = 0x5C  # Right Windows key (Natural keyboard)
VK_APPS = 0x5D  # Applications key (Natural keyboard)
VK_SLEEP = 0x5F  # Computer Sleep key
VK_NUMPAD0 = 0x60  # Numeric keypad 0 key
VK_NUMPAD1 = 0x61  # Numeric keypad 1 key
VK_NUMPAD2 = 0x62  # Numeric keypad 2 key
VK_NUMPAD3 = 0x63  # Numeric keypad 3 key
VK_NUMPAD4 = 0x64  # Numeric keypad 4 key
VK_NUMPAD5 = 0x65  # Numeric keypad 5 key
VK_NUMPAD6 = 0x66  # Numeric keypad 6 key
VK_NUMPAD7 = 0x67  # Numeric keypad 7 key
VK_NUMPAD8 = 0x68  # Numeric keypad 8 key
VK_NUMPAD9 = 0x69  # Numeric keypad 9 key
VK_MULTIPLY = 0x6A  # Multiply key
VK_ADD = 0x6B  # Add key
VK_SEPARATOR = 0x6C  # Separator key
VK_SUBTRACT = 0x6D  # Subtract key
VK_DECIMAL = 0x6E  # Decimal key
VK_DIVIDE = 0x6F  # Divide key
VK_F1 = 0x70  # F1 key
VK_F2 = 0x71  # F2 key
VK_F3 = 0x72  # F3 key
VK_F4 = 0x73  # F4 key
VK_F5 = 0x74  # F5 key
VK_F6 = 0x75  # F6 key
VK_F7 = 0x76  # F7 key
VK_F8 = 0x77  # F8 key
VK_F9 = 0x78  # F9 key
VK_F10 = 0x79  # F10 key
VK_F11 = 0x7A  # F11 key
VK_F12 = 0x7B  # F12 key
VK_F13 = 0x7C  # F13 key
VK_F14 = 0x7D  # F14 key
VK_F15 = 0x7E  # F15 key
VK_F16 = 0x7F  # F16 key
VK_F17 = 0x80  # F17 key
VK_F18 = 0x81  # F18 key
VK_F19 = 0x82  # F19 key
VK_F20 = 0x83  # F20 key
VK_F21 = 0x84  # F21 key
VK_F22 = 0x85  # F22 key
VK_F23 = 0x86  # F23 key
VK_F24 = 0x87  # F24 key
VK_NUMLOCK = 0x90  # NUM LOCK key
VK_SCROLL = 0x91  # SCROLL LOCK key
VK_LSHIFT = 0xA0  # Left SHIFT key
VK_RSHIFT = 0xA1  # Right SHIFT key
VK_LCONTROL = 0xA2  # Left CONTROL key
VK_RCONTROL = 0xA3  # Right CONTROL key
VK_LMENU = 0xA4  # Left MENU key
VK_RMENU = 0xA5  # Right MENU key
VK_BROWSER_BACK = 0xA6  # Browser Back key
VK_BROWSER_FORWARD = 0xA7  # Browser Forward key
VK_BROWSER_REFRESH = 0xA8  # Browser Refresh key
VK_BROWSER_STOP = 0xA9  # Browser Stop key
VK_BROWSER_SEARCH = 0xAA  # Browser Search key
VK_BROWSER_FAVORITES = 0xAB  # Browser Favorites key
VK_BROWSER_HOME = 0xAC  # Browser Start and Home key
VK_VOLUME_MUTE = 0xAD  # Volume Mute key
VK_VOLUME_DOWN = 0xAE  # Volume Down key
VK_VOLUME_UP = 0xAF  # Volume Up key
VK_MEDIA_NEXT_TRACK = 0xB0  # Next Track key
VK_MEDIA_PREV_TRACK = 0xB1  # Previous Track key
VK_MEDIA_STOP = 0xB2  # Stop Media key
VK_MEDIA_PLAY_PAUSE = 0xB3  # Play/Pause Media key
VK_LAUNCH_MAIL = 0xB4  # Start Mail key
VK_LAUNCH_MEDIA_SELECT = 0xB5  # Select Media key
VK_LAUNCH_APP1 = 0xB6  # Start Application 1 key
VK_LAUNCH_APP2 = 0xB7  # Start Application 2 key
VK_OEM_1 = 0xBA  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the ';:' key
VK_OEM_PLUS = 0xBB  # For any country/region, the '+' key
VK_OEM_COMMA = 0xBC  # For any country/region, the ',' key
VK_OEM_MINUS = 0xBD  # For any country/region, the '-' key
VK_OEM_PERIOD = 0xBE  # For any country/region, the '.' key
VK_OEM_2 = 0xBF  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the '/?' key
VK_OEM_3 = 0xC0  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the '`~' key
VK_OEM_4 = 0xDB  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the '[{' key
VK_OEM_5 = 0xDC  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the '\|' key
VK_OEM_6 = 0xDD  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the ']}' key
VK_OEM_7 = 0xDE  # Used for miscellaneous characters; it can vary by keyboard.For the US standard keyboard, the 'single-quote/double-quote' key
VK_OEM_8 = 0xDF  # Used for miscellaneous characters; it can vary by keyboard.
VK_OEM_102 = (
    0xE2  # Either the angle bracket key or the backslash key on the RT 102-key keyboard
)
VK_PROCESSKEY = 0xE5  # IME PROCESS key
VK_PACKET = 0xE7  # Used to pass Unicode characters as if they were keystrokes. The VK_PACKET key is the low word of a 32-bit Virtual Key value used for non-keyboard input methods. For more information, see Remark in KEYBDINPUT, SendInput, WM_KEYDOWN, and WM_KeyUp
VK_ATTN = 0xF6  # Attn key
VK_CRSEL = 0xF7  # CrSel key
VK_EXSEL = 0xF8  # ExSel key
VK_EREOF = 0xF9  # Erase EOF key
VK_PLAY = 0xFA  # Play key
VK_ZOOM = 0xFB  # Zoom key
VK_NONAME = 0xFC  # Reserved
VK_PA1 = 0xFD  # PA1 key
VK_OEM_CLEAR = 0xFE  # Clear key
allkeys = {
    "control-break processing": 3,
    "backspace": 8,
    "tab": 9,
    "clear": 254,
    "enter": 13,
    "shift": 16,
    "ctrl": 17,
    "alt": 18,
    "pause": 19,
    "caps lock": 20,
    "ime hangul mode": 21,
    "ime junja mode": 23,
    "ime final mode": 24,
    "ime kanji mode": 25,
    "esc": 27,
    "ime convert": 28,
    "ime nonconvert": 29,
    "ime accept": 30,
    "ime mode change request": 31,
    "spacebar": 32,
    "page up": 33,
    "page down": 34,
    "end": 35,
    "home": 36,
    "left": 37,
    "up": 38,
    "right": 39,
    "down": 40,
    "select": 41,
    "print": 42,
    "execute": 43,
    "print screen": 44,
    "insert": 45,
    "delete": 46,
    "help": 47,
    "0": 96,
    "1": 97,
    "2": 98,
    "3": 99,
    "4": 100,
    "5": 101,
    "6": 102,
    "7": 103,
    "8": 104,
    "9": 105,
    "a": 65,
    "b": 66,
    "c": 67,
    "d": 68,
    "e": 69,
    "f": 70,
    "g": 71,
    "h": 72,
    "i": 73,
    "j": 74,
    "k": 75,
    "l": 76,
    "m": 77,
    "n": 78,
    "o": 79,
    "p": 80,
    "q": 81,
    "r": 82,
    "s": 83,
    "t": 84,
    "u": 85,
    "v": 86,
    "w": 87,
    "x": 88,
    "y": 89,
    "z": 90,
    "left windows": 91,
    "right windows": 92,
    "applications": 93,
    "sleep": 95,
    "*": 106,
    "+": 187,
    "separator": 108,
    "-": 189,
    "decimal": 110,
    "/": 111,
    "f1": 112,
    "f2": 113,
    "f3": 114,
    "f4": 115,
    "f5": 116,
    "f6": 117,
    "f7": 118,
    "f8": 119,
    "f9": 120,
    "f10": 121,
    "f11": 122,
    "f12": 123,
    "f13": 124,
    "f14": 125,
    "f15": 126,
    "f16": 127,
    "f17": 128,
    "f18": 129,
    "f19": 130,
    "f20": 131,
    "f21": 132,
    "f22": 133,
    "f23": 134,
    "f24": 135,
    "num lock": 144,
    "scroll lock": 145,
    "left shift": 160,
    "right shift": 161,
    "left ctrl": 162,
    "right ctrl": 163,
    "left menu": 164,
    "right menu": 165,
    "browser back": 166,
    "browser forward": 167,
    "browser refresh": 168,
    "browser stop": 169,
    "browser search key": 170,
    "browser favorites": 171,
    "browser start and home": 172,
    "volume mute": 173,
    "volume down": 174,
    "volume up": 175,
    "next track": 176,
    "previous track": 177,
    "stop media": 178,
    "play/pause media": 179,
    "start mail": 180,
    "select media": 181,
    "start application 1": 182,
    "start application 2": 183,
    ",": 188,
    ".": 190,
    "ime process": 229,
    "attn": 246,
    "crsel": 247,
    "exsel": 248,
    "erase eof": 249,
    "play": 250,
    "zoom": 251,
    "reserved ": 252,
    "pa1": 253,
    "CONTROL-BREAK PROCESSING": 3,
    "BACKSPACE": 8,
    "TAB": 9,
    "CLEAR": 254,
    "ENTER": 13,
    "SHIFT": 16,
    "CTRL": 17,
    "ALT": 18,
    "PAUSE": 19,
    "CAPS LOCK": 20,
    "IME HANGUL MODE": 21,
    "IME JUNJA MODE": 23,
    "IME FINAL MODE": 24,
    "IME KANJI MODE": 25,
    "ESC": 27,
    "IME CONVERT": 28,
    "IME NONCONVERT": 29,
    "IME ACCEPT": 30,
    "IME MODE CHANGE REQUEST": 31,
    "SPACEBAR": 32,
    "PAGE UP": 33,
    "PAGE DOWN": 34,
    "END": 35,
    "HOME": 36,
    "LEFT": 37,
    "UP": 38,
    "RIGHT": 39,
    "DOWN": 40,
    "SELECT": 41,
    "PRINT": 42,
    "EXECUTE": 43,
    "PRINT SCREEN": 44,
    "INSERT": 45,
    "DELETE": 46,
    "HELP": 47,
    "A": 65,
    "B": 66,
    "C": 67,
    "D": 68,
    "E": 69,
    "F": 70,
    "G": 71,
    "H": 72,
    "I": 73,
    "J": 74,
    "K": 75,
    "L": 76,
    "M": 77,
    "N": 78,
    "O": 79,
    "P": 80,
    "Q": 81,
    "R": 82,
    "S": 83,
    "T": 84,
    "U": 85,
    "V": 86,
    "W": 87,
    "X": 88,
    "Y": 89,
    "Z": 90,
    "LEFT WINDOWS": 91,
    "RIGHT WINDOWS": 92,
    "APPLICATIONS": 93,
    "SLEEP": 95,
    "SEPARATOR": 108,
    "DECIMAL": 110,
    "F1": 112,
    "F2": 113,
    "F3": 114,
    "F4": 115,
    "F5": 116,
    "F6": 117,
    "F7": 118,
    "F8": 119,
    "F9": 120,
    "F10": 121,
    "F11": 122,
    "F12": 123,
    "F13": 124,
    "F14": 125,
    "F15": 126,
    "F16": 127,
    "F17": 128,
    "F18": 129,
    "F19": 130,
    "F20": 131,
    "F21": 132,
    "F22": 133,
    "F23": 134,
    "F24": 135,
    "NUM LOCK": 144,
    "SCROLL LOCK": 145,
    "LEFT SHIFT": 160,
    "RIGHT SHIFT": 161,
    "LEFT CTRL": 162,
    "RIGHT CTRL": 163,
    "LEFT MENU": 164,
    "RIGHT MENU": 165,
    "BROWSER BACK": 166,
    "BROWSER FORWARD": 167,
    "BROWSER REFRESH": 168,
    "BROWSER STOP": 169,
    "BROWSER SEARCH KEY": 170,
    "BROWSER FAVORITES": 171,
    "BROWSER START AND HOME": 172,
    "VOLUME MUTE": 173,
    "VOLUME DOWN": 174,
    "VOLUME UP": 175,
    "NEXT TRACK": 176,
    "PREVIOUS TRACK": 177,
    "STOP MEDIA": 178,
    "PLAY/PAUSE MEDIA": 179,
    "START MAIL": 180,
    "SELECT MEDIA": 181,
    "START APPLICATION 1": 182,
    "START APPLICATION 2": 183,
    "IME PROCESS": 229,
    "ATTN": 246,
    "CRSEL": 247,
    "EXSEL": 248,
    "ERASE EOF": 249,
    "PLAY": 250,
    "ZOOM": 251,
    "RESERVED ": 252,
    "PA1": 253,
    "CONTROL-BREAK_PROCESSING": 3,
    "CAPS_LOCK": 20,
    "IME_HANGUL_MODE": 21,
    "IME_JUNJA_MODE": 23,
    "IME_FINAL_MODE": 24,
    "IME_KANJI_MODE": 25,
    "IME_CONVERT": 28,
    "IME_NONCONVERT": 29,
    "IME_ACCEPT": 30,
    "IME_MODE_CHANGE_REQUEST": 31,
    "PAGE_UP": 33,
    "PAGE_DOWN": 34,
    "PRINT_SCREEN": 44,
    "LEFT_WINDOWS": 91,
    "RIGHT_WINDOWS": 92,
    "NUM_LOCK": 144,
    "SCROLL_LOCK": 145,
    "LEFT_SHIFT": 160,
    "RIGHT_SHIFT": 161,
    "LEFT_CTRL": 162,
    "RIGHT_CTRL": 163,
    "LEFT_MENU": 164,
    "RIGHT_MENU": 165,
    "BROWSER_BACK": 166,
    "BROWSER_FORWARD": 167,
    "BROWSER_REFRESH": 168,
    "BROWSER_STOP": 169,
    "BROWSER_SEARCH_KEY": 170,
    "BROWSER_FAVORITES": 171,
    "BROWSER_START_AND_HOME": 172,
    "VOLUME_MUTE": 173,
    "VOLUME_DOWN": 174,
    "VOLUME_UP": 175,
    "NEXT_TRACK": 176,
    "PREVIOUS_TRACK": 177,
    "STOP_MEDIA": 178,
    "PLAY/PAUSE_MEDIA": 179,
    "START_MAIL": 180,
    "SELECT_MEDIA": 181,
    "START_APPLICATION_1": 182,
    "START_APPLICATION_2": 183,
    "IME_PROCESS": 229,
    "ERASE_EOF": 249,
    "RESERVED_": 252,
    "control-break_processing": 3,
    "caps_lock": 20,
    "ime_hangul_mode": 21,
    "ime_junja_mode": 23,
    "ime_final_mode": 24,
    "ime_kanji_mode": 25,
    "ime_convert": 28,
    "ime_nonconvert": 29,
    "ime_accept": 30,
    "ime_mode_change_request": 31,
    "page_up": 33,
    "page_down": 34,
    "print_screen": 44,
    "left_windows": 91,
    "right_windows": 92,
    "num_lock": 144,
    "scroll_lock": 145,
    "left_shift": 160,
    "right_shift": 161,
    "left_ctrl": 162,
    "right_ctrl": 163,
    "left_menu": 164,
    "right_menu": 165,
    "browser_back": 166,
    "browser_forward": 167,
    "browser_refresh": 168,
    "browser_stop": 169,
    "browser_search_key": 170,
    "browser_favorites": 171,
    "browser_start_and_home": 172,
    "volume_mute": 173,
    "volume_down": 174,
    "volume_up": 175,
    "next_track": 176,
    "previous_track": 177,
    "stop_media": 178,
    "play/pause_media": 179,
    "start_mail": 180,
    "select_media": 181,
    "start_application_1": 182,
    "start_application_2": 183,
    "ime_process": 229,
    "erase_eof": 249,
    "reserved_": 252,
}

emptyLong = ctypes.c_ulong()
user32 = ctypes.WinDLL("user32", use_last_error=True)
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
INPUT_HARDWARE = 2
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
KEYEVENTF_SCANCODE = 0x0008
MAPVK_VK_TO_VSC = 0
wintypes.ULONG_PTR = wintypes.WPARAM

MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
MOUSEEVENTF_ABSOLUTE = 0x8000

MOUSEEVENTF_MIDDLEDOWN = 0x0020
MOUSEEVENTF_MIDDLEUP = 0x0040
MOUSEEVENTF_RIGHTDOWN = 0x0008
MOUSEEVENTF_RIGHTUP = 0x0010

ULONG_PTR = ctypes.c_ulong if sizeof(ctypes.c_void_p) == 4 else ctypes.c_ulonglong


class POINT_(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int), ("y", ctypes.c_int)]


class CURSORINFO(ctypes.Structure):
    _fields_ = [
        ("cbSize", ctypes.c_uint),
        ("flags", ctypes.c_uint),
        ("hCursor", ctypes.c_void_p),
        ("ptScreenPos", POINT_),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = (
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    )


class KEYBDINPUT(ctypes.Structure):
    _fields_ = (
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    )

    def __init__(self, *args, **kwds):
        super(KEYBDINPUT, self).__init__(*args, **kwds)
        if not self.dwFlags & KEYEVENTF_UNICODE:
            self.wScan = user32.MapVirtualKeyExW(self.wVk, MAPVK_VK_TO_VSC, 0)


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = (
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    )


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.wintypes.LONG), ("y", ctypes.wintypes.LONG)]


def get_cursor():
    pos = POINT_()
    user32.GetCursorPos(ctypes.byref(pos))
    return pos.x, pos.y


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = (("ki", KEYBDINPUT), ("mi", MOUSEINPUT), ("hi", HARDWAREINPUT))

    _anonymous_ = ("_input",)
    _fields_ = (("type", wintypes.DWORD), ("_input", _INPUT))


LPINPUT = ctypes.POINTER(INPUT)


def _check_count(result, func, args):
    if result == 0:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (
    wintypes.UINT,  # nInputs
    LPINPUT,  # pInputs
    ctypes.c_int,
)  # cbSize


def Press(keycode, delay=0.5):
    if isinstance(keycode, str):
        hexKeyCode = allkeys.get(keycode)
    else:
        hexKeyCode = keycode
    x = INPUT(type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
    time.sleep(delay)
    x = INPUT(
        type=INPUT_KEYBOARD, ki=KEYBDINPUT(wVk=hexKeyCode, dwFlags=KEYEVENTF_KEYUP)
    )
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))


class DUMMYUNIONNAME(Union):
    _fields_ = [("mi", MOUSEINPUT), ("ki", KEYBDINPUT), ("hi", HARDWAREINPUT)]


lib = ctypes.WinDLL("user32")
lib.SendInput.argtypes = wintypes.UINT, POINTER(INPUT), ctypes.c_int
lib.SendInput.restype = wintypes.UINT


def send_scancode(code):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    i.ki = KEYBDINPUT(0, code, KEYEVENTF_SCANCODE, 0, 0)
    lib.SendInput(1, byref(i), sizeof(INPUT))
    i.ki.dwFlags |= KEYEVENTF_KEYUP
    lib.SendInput(1, byref(i), sizeof(INPUT))


def send_unicode(s):
    i = INPUT()
    i.type = INPUT_KEYBOARD
    for c in s:
        i.ki = KEYBDINPUT(0, ord(c), KEYEVENTF_UNICODE, 0, 0)
        lib.SendInput(1, byref(i), sizeof(INPUT))
        i.ki.dwFlags |= KEYEVENTF_KEYUP
        lib.SendInput(1, byref(i), sizeof(INPUT))


LPINPUT = ctypes.POINTER(INPUT)

user32.SendInput.errcheck = _check_count
user32.SendInput.argtypes = (
    wintypes.UINT,
    LPINPUT,
    ctypes.c_int,
)


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", DWORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class KeybdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", WORD),
        ("wScan", WORD),
        ("dwFlags", DWORD),
        ("time", DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", DWORD), ("wParamL", WORD), ("wParamH", WORD)]


class InputList(ctypes.Union):
    _fields_ = [("mi", MouseInput), ("ki", KeybdInput), ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("inputList", InputList)]


def get_resolution():
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


def move_rel(x, y):
    mouseFlag = MOUSEEVENTF_MOVE
    inputList = InputList()
    inputList.mi = MouseInput(x, y, 0, mouseFlag, 0, ctypes.pointer(emptyLong))
    windowsInput = Input(emptyLong, inputList)
    ctypes.windll.user32.SendInput(
        1, ctypes.pointer(windowsInput), ctypes.sizeof(windowsInput)
    )


def move(
        x,
        y,
):
    relative = False
    mouseFlag = MOUSEEVENTF_MOVE

    if not relative:
        mouseFlag |= MOUSEEVENTF_ABSOLUTE
        xr, yr = get_resolution()
        x = floor(x / xr * 65535)
        y = floor(y / yr * 65535)

    inputList = InputList()
    inputList.mi = MouseInput(x, y, 0, mouseFlag, 0, ctypes.pointer(emptyLong))

    windowsInput = Input(emptyLong, inputList)
    ctypes.windll.user32.SendInput(
        1, ctypes.pointer(windowsInput), ctypes.sizeof(windowsInput)
    )


def _mouse_click(flags):
    x = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, flags, 0, 0))
    user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(INPUT))


def calculate_all_coords(ends):
    d0, d1 = np.diff(ends, axis=0)[0]
    if np.abs(d0) > np.abs(d1):
        return np.c_[
            np.arange(
                ends[0, 0], ends[1, 0] + np.sign(d0), np.sign(d0), dtype=np.int32
            ),
            np.arange(
                ends[0, 1] * np.abs(d0) + np.abs(d0) // 2,
                ends[0, 1] * np.abs(d0) + np.abs(d0) // 2 + (np.abs(d0) + 1) * d1,
                d1,
                dtype=np.int32,
            )
            // np.abs(d0),
        ]
    else:
        return np.c_[
            np.arange(
                ends[0, 0] * np.abs(d1) + np.abs(d1) // 2,
                ends[0, 0] * np.abs(d1) + np.abs(d1) // 2 + (np.abs(d1) + 1) * d0,
                d0,
                dtype=np.int32,
            )
            // np.abs(d1),
            np.arange(
                ends[0, 1], ends[1, 1] + np.sign(d1), np.sign(d1), dtype=np.int32
            ),
        ]


def add_random_n_places(a, n, low=-10, high=10):
    out = a.astype(int)
    idx = np.random.choice(a.size, n, replace=False)
    out.flat[idx] += np.random.randint(low=low, high=high, size=n)
    return out


def natural_mouse_movement(
        x,
        y,
        min_variation=-2,
        max_variation=2,
        use_every=1,
        sleeptime=(0.005, 0.009),
        print_coords=True,
        percent=90,
):
    nowx, nowy = get_cursor()
    coordtomove = x, y
    futx, futy = coordtomove
    allco = np.array([[nowx, nowy], [futx, futy]])

    alla = calculate_all_coords(allco)
    alla = add_random_n_places(
        alla,
        n=int(alla.shape[0] * percent / 100),
        low=min_variation,
        high=max_variation,
    )
    alla = np.repeat(alla, 4, axis=0)
    alla = alla[::use_every]
    alla = np.vstack([alla, [futx, futy]])
    alla = np.array(list(reversed(tuple([p[-1] for p in log_split(reversed(alla))]))))

    for x in alla:
        if print_coords:
            print(f"{x}         ", end="\r")

        move(int(x[0]), int(x[1]))
        time.sleep(uniform(*sleeptime))


def left_click_xy_natural_relative(
        x,
        y,
        delay=0.1,
        sleeptime=(0.00005, 0.00009),
        print_coords=True,
):
    natural_mouse_movement_relative(
        x,
        y,
        sleeptime=sleeptime,
        print_coords=print_coords,
    )
    left_click(delay=delay)


def log_split(*args):
    def logsplit(lst):
        iterator = iter(lst)
        for n, e in enumerate(iterator):
            yield itertools.chain([e], itertools.islice(iterator, n))

    if len(args) > 1:
        for x in logsplit(zip(*args)):
            yield list(x)
    else:
        for x in logsplit(args[0]):
            yield list(x)


def natural_mouse_movement_relative(
        x,
        y,
        sleeptime=(0.00005, 0.00009),
        print_coords=True,
):
    nowx, nowy = 0, 0
    coordtomove = x * 2, y * 2
    futx, futy = coordtomove
    allco = np.array([[nowx, nowy], [futx, futy]])
    alla = calculate_all_coords(allco)
    alla = np.vstack([alla, [futx, futy]])
    difa1 = np.diff(alla[..., 0], prepend=0)
    difa2 = np.diff(alla[..., 1], prepend=0)
    alla = np.vstack([difa1, difa2]).T
    for x in alla:
        if print_coords:
            print(f"{x}         ", end="\r")

        move_rel(int(x[0]), int(x[1]))
        time.sleep(uniform(*sleeptime))


def left_click(delay=0.1):
    _mouse_click(MOUSEEVENTF_LEFTDOWN)
    time.sleep(delay)
    _mouse_click(MOUSEEVENTF_LEFTUP)


def left_mouse_down():
    _mouse_click(MOUSEEVENTF_LEFTDOWN)


def left_mouse_up():
    _mouse_click(MOUSEEVENTF_LEFTUP)


def right_mouse_down():
    _mouse_click(MOUSEEVENTF_RIGHTDOWN)


def right_mouse_up():
    _mouse_click(MOUSEEVENTF_RIGHTUP)


def middle_mouse_down():
    _mouse_click(MOUSEEVENTF_MIDDLEDOWN)


def middle_mouse_up():
    _mouse_click(MOUSEEVENTF_MIDDLEUP)


def left_click_xy(x, y, delay=0.1):
    move(x, y)
    left_click(delay=delay)


def left_click_xy_natural(
        x,
        y,
        delay=0.1,
        min_variation=-3,
        max_variation=3,
        use_every=4,
        sleeptime=(0.005, 0.009),
        print_coords=True,
        percent=90,
):
    natural_mouse_movement(
        x,
        y,
        min_variation=min_variation,
        max_variation=max_variation,
        use_every=use_every,
        sleeptime=sleeptime,
        print_coords=print_coords,
        percent=percent,
    )
    left_click(delay=delay)


def right_click(delay=0.1):
    _mouse_click(MOUSEEVENTF_RIGHTDOWN)
    time.sleep(delay)
    _mouse_click(MOUSEEVENTF_RIGHTUP)


def right_click_xy(x, y, delay=0.1):
    move(x, y)
    right_click(delay=delay)


def right_click_xy_natural(
        x,
        y,
        delay=0.1,
        min_variation=-1,
        max_variation=1,
        use_every=1,
        sleeptime=(0.005, 0.009),
        print_coords=True,
        percent=90,
):
    natural_mouse_movement(
        x,
        y,
        min_variation=min_variation,
        max_variation=max_variation,
        use_every=use_every,
        sleeptime=sleeptime,
        print_coords=print_coords,
        percent=percent,
    )
    right_click(delay=delay)


def right_click_xy_natural_relative(
        x,
        y,
        delay=0.1,
        sleeptime=(0.00005, 0.00009),
        print_coords=True,
):
    natural_mouse_movement_relative(
        x,
        y,
        sleeptime=sleeptime,
        print_coords=print_coords,
    )
    right_click(delay=delay)


def middle_click(delay=0.1):
    _mouse_click(MOUSEEVENTF_MIDDLEDOWN)
    time.sleep(delay)
    _mouse_click(MOUSEEVENTF_MIDDLEUP)


def middle_click_xy(x, y, delay=0.1):
    move(x, y)
    middle_click(delay=delay)


def middle_click_xy_natural(
        x,
        y,
        delay=0.1,
        min_variation=-3,
        max_variation=3,
        use_every=4,
        sleeptime=(0.005, 0.009),
        print_coords=True,
        percent=90,
):
    natural_mouse_movement(
        x,
        y,
        min_variation=min_variation,
        max_variation=max_variation,
        use_every=use_every,
        sleeptime=sleeptime,
        print_coords=print_coords,
        percent=percent,
    )
    middle_click(delay=delay)


def middle_click_xy_relative(
        x,
        y,
        delay=0.1,
        sleeptime=(0.00005, 0.00009),
        print_coords=True,
):
    natural_mouse_movement_relative(
        x,
        y,
        sleeptime=sleeptime,
        print_coords=print_coords,
    )
    middle_click(delay=delay)


def is_cursor_shown():
    GetCursorInfo = ctypes.windll.user32.GetCursorInfo
    GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
    info = CURSORINFO()
    info.cbSize = ctypes.sizeof(info)
    if GetCursorInfo(ctypes.byref(info)):
        if info.flags & 0x00000001:
            return True
    return False


def get_active_window():
    pid = ctypes.wintypes.DWORD()
    active = ctypes.windll.user32.GetForegroundWindow()
    active_window = ctypes.windll.user32.GetWindowThreadProcessId(
        active, ctypes.byref(pid)
    )
    ac = {"pid": pid.value, "foreground": active, "active_window": active_window}
    try:
        return [
            x
            for x in get_window_infos()
            if x.pid == ac["pid"]
               and x.hwnd == ac["foreground"]
               and x.tid == ac["active_window"]
        ][0]
    except Exception:
        return []


DEBUG = 0
INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 1
KEYEVENTF_KEYUP = 2
KEYEVENTF_UNICODE = 4
KEYEVENTF_SCANCODE = 8
VK_SHIFT = 16
VK_CONTROL = 17
VK_MENU = 18

CODES = {
    "BACK": 8,
    "BACKSPACE": 8,
    "BKSP": 8,
    "BREAK": 3,
    "BS": 8,
    "CAP": 20,
    "CAPSLOCK": 20,
    "DEL": 46,
    "DELETE": 46,
    "DOWN": 40,
    "END": 35,
    "ENTER": 13,
    "ESC": 27,
    "F1": 112,
    "F2": 113,
    "F3": 114,
    "F4": 115,
    "F5": 116,
    "F6": 117,
    "F7": 118,
    "F8": 119,
    "F9": 120,
    "F10": 121,
    "F11": 122,
    "F12": 123,
    "F13": 124,
    "F14": 125,
    "F15": 126,
    "F16": 127,
    "F17": 128,
    "F18": 129,
    "F19": 130,
    "F20": 131,
    "F21": 132,
    "F22": 133,
    "F23": 134,
    "F24": 135,
    "HELP": 47,
    "HOME": 36,
    "INS": 45,
    "INSERT": 45,
    "LEFT": 37,
    "LWIN": 91,
    "NUMLOCK": 144,
    "PGDN": 34,
    "PGUP": 33,
    "PRTSC": 44,
    "RIGHT": 39,
    "RMENU": 165,
    "RWIN": 92,
    "SCROLLLOCK": 145,
    "SPACE": 32,
    "TAB": 9,
    "UP": 38,
    "VK_ACCEPT": 30,
    "VK_ADD": 107,
    "VK_APPS": 93,
    "VK_ATTN": 246,
    "VK_BACK": 8,
    "VK_CANCEL": 3,
    "VK_CAPITAL": 20,
    "VK_CLEAR": 12,
    "VK_CONTROL": 17,
    "VK_CONVERT": 28,
    "VK_CRSEL": 247,
    "VK_DECIMAL": 110,
    "VK_DELETE": 46,
    "VK_DIVIDE": 111,
    "VK_DOWN": 40,
    "VK_END": 35,
    "VK_EREOF": 249,
    "VK_ESCAPE": 27,
    "VK_EXECUTE": 43,
    "VK_EXSEL": 248,
    "VK_F1": 112,
    "VK_F2": 113,
    "VK_F3": 114,
    "VK_F4": 115,
    "VK_F5": 116,
    "VK_F6": 117,
    "VK_F7": 118,
    "VK_F8": 119,
    "VK_F9": 120,
    "VK_F10": 121,
    "VK_F11": 122,
    "VK_F12": 123,
    "VK_F13": 124,
    "VK_F14": 125,
    "VK_F15": 126,
    "VK_F16": 127,
    "VK_F17": 128,
    "VK_F18": 129,
    "VK_F19": 130,
    "VK_F20": 131,
    "VK_F21": 132,
    "VK_F22": 133,
    "VK_F23": 134,
    "VK_F24": 135,
    "VK_FINAL": 24,
    "VK_HANGEUL": 21,
    "VK_HANGUL": 21,
    "VK_HANJA": 25,
    "VK_HELP": 47,
    "VK_HOME": 36,
    "VK_INSERT": 45,
    "VK_JUNJA": 23,
    "VK_KANA": 21,
    "VK_KANJI": 25,
    "VK_LBUTTON": 1,
    "VK_LCONTROL": 162,
    "VK_LEFT": 37,
    "VK_LMENU": 164,
    "VK_LSHIFT": 160,
    "VK_LWIN": 91,
    "VK_MBUTTON": 4,
    "VK_MENU": 18,
    "VK_MODECHANGE": 31,
    "VK_MULTIPLY": 106,
    "VK_NEXT": 34,
    "VK_NONAME": 252,
    "VK_NONCONVERT": 29,
    "VK_NUMLOCK": 144,
    "VK_NUMPAD0": 96,
    "VK_NUMPAD1": 97,
    "VK_NUMPAD2": 98,
    "VK_NUMPAD3": 99,
    "VK_NUMPAD4": 100,
    "VK_NUMPAD5": 101,
    "VK_NUMPAD6": 102,
    "VK_NUMPAD7": 103,
    "VK_NUMPAD8": 104,
    "VK_NUMPAD9": 105,
    "VK_OEM_CLEAR": 254,
    "VK_PA1": 253,
    "VK_PAUSE": 19,
    "VK_PLAY": 250,
    "VK_PRINT": 42,
    "VK_PRIOR": 33,
    "VK_PROCESSKEY": 229,
    "VK_RBUTTON": 2,
    "VK_RCONTROL": 163,
    "VK_RETURN": 13,
    "VK_RIGHT": 39,
    "VK_RMENU": 165,
    "VK_RSHIFT": 161,
    "VK_RWIN": 92,
    "VK_SCROLL": 145,
    "VK_SELECT": 41,
    "VK_SEPARATOR": 108,
    "VK_SHIFT": 16,
    "VK_SNAPSHOT": 44,
    "VK_SPACE": 32,
    "VK_SUBTRACT": 109,
    "VK_TAB": 9,
    "VK_UP": 38,
    "ZOOM": 251,
}
CODE_NAMES = dict((entry[1], entry[0]) for entry in CODES.items())
MODIFIERS = {
    "+": VK_SHIFT,
    "^": VK_CONTROL,
    "%": VK_MENU,
}
ascii_vk = {
    " ": 0x20,
    "=": 0xBB,
    ",": 0xBC,
    "-": 0xBD,
    ".": 0xBE,
    ";": 0xBA,
    "/": 0xBF,
    "`": 0xC0,
    "[": 0xDB,
    "\\": 0xDC,
    "]": 0xDD,
    "'": 0xDE,
}
ascii_vk.update(dict((c, ord(c)) for c in string.ascii_uppercase + string.digits))
ascii_vk.update(dict((c, ord(c.upper())) for c in string.ascii_lowercase))

"""

From here on, almost everything is strongly based on pywinauto:
https://pywinauto.readthedocs.io/en/latest/

        Copyright (c) 2017, Mark Mc Mahon and Contributors
    All rights reserved.

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

     * Redistributions of source code must retain the above copyright notice, this
       list of conditions and the following disclaimer.

     * Redistributions in binary form must reproduce the above copyright notice,
       this list of conditions and the following disclaimer in the documentation
       and/or other materials provided with the distribution.

     * Neither the name of pywinauto nor the names of its
       contributors may be used to endorse or promote products derived from
       this software without specific prior written permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
    AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
    IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
    DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
    FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
    DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
    SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
    CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
    OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    
    
"""


class KeySequenceError(Exception):
    def __str__(self):
        return " ".join(self.args)


class UNION_INPUT_STRUCTS(Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUTX(Structure):
    _pack_ = 8
    _anonymous_ = ("_",)
    _fields_ = [
        ("type", ctypes.c_int),
        ("_", UNION_INPUT_STRUCTS),
    ]


SendInput = ctypes.windll.user32.SendInput
SendInput.restype = wintypes.UINT
SendInput.argtypes = [
    wintypes.UINT,
    ctypes.c_void_p,  # using POINTER(win32structures.INPUT) needs rework in keyboard.py
    ctypes.c_int,
]

GetMessageExtraInfo = ctypes.windll.user32.GetMessageExtraInfo


class KeyAction(object):
    # from https://pywinauto.readthedocs.io/

    """
    Class that represents a single keyboard action
    It represents either a PAUSE action (not really keyboard) or a keyboard
    action (press or release or both) of a particular key.
    """

    def __init__(self, key, down=True, up=True):
        self.key = key
        if isinstance(self.key, six.string_types):
            self.key = six.text_type(key)
        self.down = down
        self.up = up

    def _get_key_info(self):
        """Return virtual_key, scan_code, and flags for the action

        This is one of the methods that will be overridden by sub classes.
        """
        return 0, ord(self.key), KEYEVENTF_UNICODE

    def get_key_info(self):
        """Return virtual_key, scan_code, and flags for the action

        This is one of the methods that will be overridden by sub classes.
        """
        return self._get_key_info()

    def GetInput(self):
        """Build the INPUT structure for the action"""
        actions = 1
        # if both up and down
        if self.up and self.down:
            actions = 2

        inputs = (INPUTX * actions)()

        vk, scan, flags = self._get_key_info()

        for inp in inputs:
            inp.type = INPUT_KEYBOARD

            inp.ki.wVk = vk
            inp.ki.wScan = scan
            inp.ki.dwFlags |= flags

            # it seems to return 0 every time but it's required by MSDN specification
            # so call it just in case
            inp.ki.dwExtraInfo = GetMessageExtraInfo()

        # if we are releasing - then let it up
        if self.up:
            inputs[-1].ki.dwFlags |= KEYEVENTF_KEYUP

        return inputs

    def run(self):
        """Execute the action"""
        inputs = self.GetInput()

        # SendInput() supports all Unicode symbols
        num_inserted_events = SendInput(
            len(inputs), ctypes.byref(inputs), ctypes.sizeof(INPUTX)
        )
        if num_inserted_events != len(inputs):
            raise RuntimeError(
                "SendInput() inserted only "
                + str(num_inserted_events)
                + " out of "
                + str(len(inputs))
                + " keyboard events"
            )

    def _get_down_up_string(self):
        """Return a string that will show whether the string is up or down

        return 'down' if the key is a press only
        return 'up' if the key is up only
        return '' if the key is up & down (as default)
        """
        down_up = ""
        if not (self.down and self.up):
            if self.down:
                down_up = "down"
            elif self.up:
                down_up = "up"
        return down_up

    def key_description(self):
        """Return a description of the key"""
        vk, scan, flags = self._get_key_info()
        desc = ""
        if vk:
            if vk in CODE_NAMES:
                desc = CODE_NAMES[vk]
            else:
                desc = "VK {}".format(vk)
        else:
            desc = "{}".format(self.key)

        return desc

    def __str__(self):
        parts = []
        parts.append(self.key_description())
        up_down = self._get_down_up_string()
        if up_down:
            parts.append(up_down)

        return "<{}>".format(" ".join(parts))

    __repr__ = __str__


class VirtualKeyAction(KeyAction):
    """Represents a virtual key action e.g. F9 DOWN, etc

    Overrides necessary methods of KeyAction
    """

    def _get_key_info(self):
        """Virtual keys have extended flag set"""
        # copied more or less verbatim from
        # http://www.pinvoke.net/default.aspx/user32.sendinput
        if 33 <= self.key <= 46 or 91 <= self.key <= 93:
            flags = KEYEVENTF_EXTENDEDKEY
        else:
            flags = 0
        # This works for %{F4} - ALT + F4
        # return self.key, 0, 0

        # this works for Tic Tac Toe i.e. +{RIGHT} SHIFT + RIGHT
        return self.key, MapVirtualKeyW(self.key, 0), flags

    def run(self):
        """Execute the action"""
        # it works more stable for virtual keys than SendInput
        for inp in self.GetInput():
            # send_scancode(inp)
            Press(inp.ki.wVk)
            # win32api.keybd_event(inp.ki.wVk, inp.ki.wScan, inp.ki.dwFlags)


class EscapedKeyAction(KeyAction):
    """Represents an escaped key action e.g. F9 DOWN, etc

    Overrides necessary methods of KeyAction
    """

    def _get_key_info(self):
        """EscapedKeyAction doesn't send it as Unicode

        The vk and scan code are generated differently.
        """
        vkey_scan = LoByte(VkKeyScanW(self.key))

        return (vkey_scan, MapVirtualKeyW(vkey_scan, 0), 0)

    def key_description(self):
        """Return a description of the key"""
        return "KEsc {}".format(self.key)

    def run(self):
        """Execute the action"""
        # it works more stable for virtual keys than SendInput
        for inp in self.GetInput():
            # win32api.keybd_event(inp.ki.wVk, inp.ki.wScan, inp.ki.dwFlags)
            Press(inp.ki.wVk)


class PauseAction(KeyAction):
    """Represents a pause action"""

    def __init__(self, how_long):
        self.how_long = how_long

    def run(self):
        """Pause for the lenght of time specified"""
        time.sleep(self.how_long)

    def __str__(self):
        return "<PAUSE %1.2f>" % (self.how_long)

    __repr__ = __str__


def handle_code(code, vk_packet):
    """Handle a key or sequence of keys in braces"""
    code_keys = []
    if code in CODES:
        code_keys.append(VirtualKeyAction(CODES[code]))

    elif len(code) == 1:
        if not vk_packet and code in ascii_vk:
            code_keys.append(VirtualKeyAction(ascii_vk[code]))
        else:
            code_keys.append(KeyAction(code))

    # it is a repetition or a pause  {DOWN 5}, {PAUSE 1.3}
    elif " " in code:
        to_repeat, count = code.rsplit(None, 1)
        if to_repeat == "PAUSE":
            try:
                pause_time = float(count)
            except ValueError:
                raise KeySequenceError("invalid pause time %s" % count)
            code_keys.append(PauseAction(pause_time))

        else:
            try:
                count = int(count)
            except ValueError:
                raise KeySequenceError("invalid repetition count {}".format(count))

            # If the value in to_repeat is a VK e.g. DOWN
            # we need to add the code repeated
            if to_repeat in CODES:
                code_keys.extend([VirtualKeyAction(CODES[to_repeat])] * count)
            # otherwise parse the keys and we get back a KeyAction
            else:
                to_repeat = parse_keys(to_repeat, vk_packet=vk_packet)
                if isinstance(to_repeat, list):
                    keys = to_repeat * count
                else:
                    keys = [to_repeat] * count
                code_keys.extend(keys)
    else:
        raise RuntimeError("Unknown code: {}".format(code))

    return code_keys


def parse_keys(
        string,
        with_spaces=False,
        with_tabs=False,
        with_newlines=False,
        modifiers=None,
        vk_packet=True,
        activate_window_before=True,
):
    """Return the parsed keys"""

    keys = []
    if not modifiers:
        modifiers = []

    should_escape_next_keys = False
    index = 0
    while index < len(string):

        c = string[index]
        index += 1
        # check if one of CTRL, SHIFT, ALT has been pressed
        if c in MODIFIERS.keys():
            modifier = MODIFIERS[c]
            # remember that we are currently modified
            modifiers.append(modifier)
            # hold down the modifier key
            keys.append(VirtualKeyAction(modifier, up=False))
            if DEBUG:
                print("MODS+", modifiers)
            continue

        # Apply modifiers over a bunch of characters (not just one!)
        elif c == "(":
            # find the end of the bracketed text
            end_pos = string.find(")", index)
            if end_pos == -1:
                raise KeySequenceError("`)` not found")
            keys.extend(
                parse_keys(
                    string[index:end_pos], modifiers=modifiers, vk_packet=vk_packet
                )
            )
            index = end_pos + 1

        # Escape or named key
        elif c == "{":
            # We start searching from index + 1 to account for the case {}}
            end_pos = string.find("}", index + 1)
            if end_pos == -1:
                raise KeySequenceError("`}` not found")

            code = string[index:end_pos]
            index = end_pos + 1
            key_events = [" up", " down"]
            current_key_event = None
            if any(key_event in code.lower() for key_event in key_events):
                code, current_key_event = code.split(" ")
                should_escape_next_keys = True
            current_keys = handle_code(code, vk_packet)
            if current_key_event is not None:
                if isinstance(current_keys[0].key, six.string_types):
                    current_keys[0] = EscapedKeyAction(current_keys[0].key)

                if current_key_event.strip() == "up":
                    current_keys[0].down = False
                else:
                    current_keys[0].up = False
            keys.extend(current_keys)

        # unmatched ")"
        elif c == ")":
            raise KeySequenceError("`)` should be preceeded by `(`")

        # unmatched "}"
        elif c == "}":
            raise KeySequenceError("`}` should be preceeded by `{`")

        # so it is a normal character
        else:
            # don't output white space unless flags to output have been set
            if (
                    c == " "
                    and not with_spaces
                    or c == "\t"
                    and not with_tabs
                    or c == "\n"
                    and not with_newlines
            ):
                continue

            # output newline
            if c in ("~", "\n"):
                keys.append(VirtualKeyAction(CODES["ENTER"]))

            # safest are the virtual keys - so if our key is a virtual key
            # use a VirtualKeyAction
            # if ord(c) in CODE_NAMES:
            #    keys.append(VirtualKeyAction(ord(c)))

            elif modifiers or should_escape_next_keys:
                keys.append(EscapedKeyAction(c))

            # if user disables the vk_packet option, always try to send a
            # virtual key of the actual keystroke
            elif not vk_packet and c in ascii_vk:
                keys.append(VirtualKeyAction(ascii_vk[c]))

            else:
                keys.append(KeyAction(c))

        # as we have handled the text - release the modifiers
        while modifiers:
            if DEBUG:
                print("MODS-", modifiers)
            keys.append(VirtualKeyAction(modifiers.pop(), down=False))

    # just in case there were any modifiers left pressed - release them
    while modifiers:
        keys.append(VirtualKeyAction(modifiers.pop(), down=False))

    return keys


def LoByte(val):
    """Return the low byte of the value"""
    return val & 0xFF


def send_keys(
        handle,
        keys,
        pause=0.05,
        with_spaces=False,
        with_tabs=False,
        with_newlines=False,
        turn_off_numlock=True,
        vk_packet=True,
        activate_window_before=True,
):
    """Parse the keys and type them"""
    sena = (
        ctypes.c_int(handle),
        ctypes.c_int(WM_ACTIVATE),
        ctypes.c_int(WA_ACTIVE),
        ctypes.c_int(0),
    )
    cuax = None
    if activate_window_before:
        SendMessageA(*sena)
        SendMessage(*sena)
        EnableWindow(handle, bEnable=True)
        cuax = get_cursor()
        # ele = get_fg_window().hwnd
        force_activate_window(handle)

    keys = parse_keys(keys, with_spaces, with_tabs, with_newlines, vk_packet=vk_packet)

    for k in keys:
        k.run()
        time.sleep(pause)
    if activate_window_before:
        move(*cuax)
        time.sleep(0.05)

        deactivate_topmost(handle)


PBYTE256 = ctypes.c_ubyte * 256
WM_ACTIVATE = 0x0006
WA_ACTIVE = 1
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

GetKeyboardState = ctypes.windll.user32.GetKeyboardState
GetKeyboardState.restype = wintypes.BOOL
GetKeyboardState.argtypes = [
    POINTER(ctypes.c_ubyte),
]

GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = wintypes.DWORD
GetWindowThreadProcessId.argtypes = [
    wintypes.HWND,
    POINTER(wintypes.DWORD),
]

GetCurrentThreadId = ctypes.windll.kernel32.GetCurrentThreadId
GetCurrentThreadId.restype = wintypes.DWORD
GetCurrentThreadId.argtypes = []
GetWindowThreadProcessId = ctypes.windll.user32.GetWindowThreadProcessId
GetWindowThreadProcessId.restype = wintypes.DWORD
GetWindowThreadProcessId.argtypes = [
    wintypes.HWND,
    POINTER(wintypes.DWORD),
]
AttachThreadInput = ctypes.windll.user32.AttachThreadInput
AttachThreadInput.restype = wintypes.BOOL
AttachThreadInput.argtypes = [wintypes.DWORD, wintypes.DWORD, wintypes.BOOL]
GetKeyboardLayout = ctypes.windll.user32.GetKeyboardLayout
GetKeyboardLayout.restype = wintypes.HKL
GetKeyboardLayout.argtypes = [
    wintypes.DWORD,
]
VkKeyScanW = ctypes.windll.user32.VkKeyScanW
VkKeyScanW.restype = SHORT
VkKeyScanW.argtypes = [
    wintypes.WCHAR,
]
VkKeyScanExW = ctypes.windll.user32.VkKeyScanExW
VkKeyScanExW.restype = SHORT
VkKeyScanExW.argtypes = [
    wintypes.WCHAR,
    wintypes.HKL,
]
SetKeyboardState = ctypes.windll.user32.SetKeyboardState
SetKeyboardState.restype = wintypes.BOOL
SetKeyboardState.argtypes = [
    POINTER(ctypes.c_ubyte),
]
MapVirtualKeyW = ctypes.windll.user32.MapVirtualKeyW
DrawMenuBar = ctypes.windll.user32.DrawMenuBar
DrawMenuBar.restype = wintypes.BOOL
DrawMenuBar.argstype = [
    wintypes.HWND,
]

PostMessage = ctypes.windll.user32.PostMessageW
PostMessage.restype = wintypes.BOOL
PostMessage.argtypes = [
    wintypes.HWND,
    wintypes.UINT,
    wintypes.WPARAM,
    wintypes.LPARAM,
]
GetMessage = ctypes.windll.user32.GetMessageW
GetMessage.restype = wintypes.BOOL
GetMessage.argtypes = [
    POINTER(wintypes.MSG),
    wintypes.HWND,
    wintypes.UINT,
    wintypes.UINT,
]

SendMessage = ctypes.windll.user32.SendMessageW
SendMessageA = ctypes.windll.user32.SendMessageA


def activate_topmost(hwnd):
    ctypes.windll.user32.BringWindowToTop(hwnd)  # works OK
    HWND_TOPMOST = -1
    SWP_NOSIZE = 1
    SWP_NOMOVE = 2
    user32.SetForegroundWindow(hwnd)
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)
    ctypes.windll.user32.SetWindowPos(
        hwnd, ctypes.wintypes.HWND(HWND_TOPMOST), 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE
    )


def force_activate_window(hwnd):
    activate_topmost(hwnd)
    time.sleep(0.01)
    WM_SYSCOMMAND = ctypes.c_int(0x0112)
    SC_SIZE = ctypes.c_int(0xF000)
    user32.SetForegroundWindow(hwnd)
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)
    t = kthread.KThread(
        target=lambda: SendMessage(hwnd, WM_SYSCOMMAND, SC_SIZE, 0), name="baba"
    )
    t.start()
    # SendMessage(hwnd, WM_SYSCOMMAND, 0xF120, 0)
    time.sleep(0.1)
    left_click()
    deactivate_topmost(hwnd)


def deactivate_topmost(hwnd):
    activate_window(hwnd)
    activate_window(hwnd)


def activate_window(hwnd):
    HWND_TOPMOST = -1
    SWP_NOSIZE = 1
    SWP_NOMOVE = 2
    ctypes.windll.user32.SetWindowPos(
        hwnd, ctypes.wintypes.HWND(1), 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE
    )
    ctypes.windll.user32.BringWindowToTop(hwnd)
    ctypes.windll.user32.SetWindowPos(
        hwnd, ctypes.wintypes.HWND(-2), 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE
    )

    user32.SetForegroundWindow(hwnd)
    if user32.IsIconic(hwnd):
        user32.ShowWindow(hwnd, 9)


def EnableWindow(hWnd, bEnable=True):
    _EnableWindow = ctypes.windll.user32.EnableWindow
    _EnableWindow.argtypes = [HWND, BOOL]
    _EnableWindow.restype = bool
    return _EnableWindow(hWnd, bool(bEnable))


def get_fg_window():
    return _get_elements_from_coords(hwnd=ctypes.windll.user32.GetForegroundWindow())[
        "element"
    ]


def send_keystrokes(
        handle,
        keystrokes,
        with_spaces=True,
        with_tabs=True,
        with_newlines=True,
        activate_window_before=True,
):
    """
    Silently send keystrokes to the control in an inactive window

    It parses modifiers Shift(+), Control(^), Menu(%) and Sequences like "{TAB}", "{ENTER}"
    For more information about Sequences and Modifiers navigate to module `keyboard`_

    .. _`keyboard`: pywinauto.keyboard.html

    Due to the fact that each application handles input differently and this method
    is meant to be used on inactive windows, it may work only partially depending
    on the target app. If the window being inactive is not essential, use the robust
    `type_keys`_ method.

    .. _`type_keys`: pywinauto.base_wrapper.html#pywinauto.base_wrapper.BaseWrapper.type_keys
    """

    sena = (
        ctypes.c_int(handle),
        ctypes.c_int(WM_ACTIVATE),
        ctypes.c_int(WA_ACTIVE),
        ctypes.c_int(0),
    )
    if activate_window_before:
        SendMessageA(*sena)
        SendMessage(*sena)
        EnableWindow(handle, bEnable=True)
        force_activate_window(handle)

    target_thread_id = GetWindowThreadProcessId(handle, None)
    current_thread_id = GetCurrentThreadId()
    attach_success = AttachThreadInput(target_thread_id, current_thread_id, True) != 0
    if not attach_success:
        warnings.warn(
            "Failed to attach app's thread to the current thread's message queue",
            UserWarning,
            stacklevel=2,
        )

    keyboard_state_stack = [PBYTE256()]
    GetKeyboardState(keyboard_state_stack[-1])

    input_locale_id = GetKeyboardLayout(0)
    context_code = 0

    keys = parse_keys(keystrokes, with_spaces, with_tabs, with_newlines)
    key_combos_present = any([isinstance(k, EscapedKeyAction) for k in keys])
    if key_combos_present:
        warnings.warn(
            "Key combinations may or may not work depending on the target app",
            UserWarning,
            stacklevel=2,
        )

    try:
        for key in keys:
            vk, scan, flags = key.get_key_info()

            if vk == VK_MENU or context_code == 1:
                down_msg, up_msg = WM_SYSKEYDOWN, WM_SYSKEYUP
            else:
                down_msg, up_msg = WM_KEYDOWN, WM_KEYUP

            repeat = 1
            shift_state = 0
            unicode_codepoint = flags & KEYEVENTF_UNICODE != 0
            if unicode_codepoint:
                char = chr(scan)
                vk_with_flags = VkKeyScanExW(char, input_locale_id)
                vk = vk_with_flags & 0xFF
                shift_state = (vk_with_flags & 0xFF00) >> 8
                scan = MapVirtualKeyW(vk, 0)

            if key.down and vk > 0:
                new_keyboard_state = copy.deepcopy(keyboard_state_stack[-1])

                new_keyboard_state[vk] |= 128
                if shift_state & 1 == 1:
                    new_keyboard_state[VK_SHIFT] |= 128
                keyboard_state_stack.append(new_keyboard_state)

                lparam = (
                        repeat << 0
                        | scan << 16
                        | (flags & 1) << 24
                        | context_code << 29
                        | 0 << 31
                )

                SetKeyboardState(keyboard_state_stack[-1])
                PostMessage(handle, down_msg, vk, lparam)
                if vk == VK_MENU:
                    context_code = 1

                # a delay for keyboard state to take effect
                time.sleep(0.01)

            if key.up and vk > 0:
                keyboard_state_stack.pop()

                lparam = (
                        repeat << 0
                        | scan << 16
                        | (flags & 1) << 24
                        | context_code << 29
                        | 1 << 30
                        | 1 << 31
                )

                PostMessage(handle, up_msg, vk, lparam)
                SetKeyboardState(keyboard_state_stack[-1])

                if vk == VK_MENU:
                    context_code = 0

                # a delay for keyboard state to take effect
                time.sleep(0.01)

    except Exception as e:
        print("fehler")
        SetKeyboardState(keyboard_state_stack[0])

    if attach_success:
        AttachThreadInput(target_thread_id, current_thread_id, False)
    if activate_window_before:
        time.sleep(0.1)

        deactivate_topmost(handle)


def get_single_element_from_coord(x, y):
    return _get_elements_from_coords(coordx=x, coordy=y)["element"]


def get_single_element_from_hwnd(hwnd):
    return _get_elements_from_coords(hwnd=hwnd)["element"]


def press_multiple_keys(keystopress, presstime=1.1, percentofregularpresstime=100):
    presstime *= 10000
    presstime = int(presstime)
    segtim = presstime / 200000
    allk = [
        [k[0], len(k[1]), k[1]]
        for k in zip(keystopress, list(log_split(range(presstime))))
    ]
    print(allk)
    timehold = sum([k[1] * 100 / percentofregularpresstime for k in allk])
    restsleep = presstime - timehold
    threadlist = []
    presstime /= 10000
    restsleep /= 10000
    for ini, k in enumerate(allk):
        subnu = k[1] * 100 / percentofregularpresstime / 10
        threadlist.append(
            kthread.KThread(
                target=Press,
                name=str(time.time()) + str(ini),
                args=(k[0], (presstime - subnu) / 10),
            )
        )
        threadlist[-1].start()
        time.sleep(subnu)
    time.sleep(restsleep + segtim)


def press_multiple_keys_own_interval(keystopress, presstime=1.1):
    totalpresstime = presstime

    sleeptimeall = np.hstack(
        [np.diff(np.array([x[0] for x in keystopress]), axis=0), np.array([0])]
    )
    restssleep = totalpresstime - np.max(sleeptimeall)
    threadlist = []
    ini = 0
    for k, tim in zip(keystopress, sleeptimeall):
        ausfu = totalpresstime - k[0]
        threadlist.append(
            kthread.KThread(
                target=Press, name=str(time.time()) + str(ini), args=(k[1], ausfu)
            )
        )
        threadlist[-1].start()
        time.sleep(tim)
        ini += 1
        print(ausfu, tim, k)
    time.sleep(restssleep)


def block_user_input():
    return BlockInput(True)


def unblock_user_input():
    return BlockInput(False)


class MouseKey:
    def __init__(self):
        self.block_user_input = block_user_input
        self.unblock_user_input = unblock_user_input

        self.get_active_window = get_active_window
        self.send_unicode = send_unicode
        self.middle_click_xy_natural = middle_click_xy_natural
        self.middle_click_xy_relative = middle_click_xy_relative
        self.middle_click_xy = middle_click_xy
        self.middle_click = middle_click
        self.right_click_xy_natural = right_click_xy_natural
        self.right_click_xy = right_click_xy
        self.right_click = right_click
        self.left_click_xy_natural = left_click_xy_natural
        self.left_click_xy = left_click_xy
        self.left_click = left_click
        self.move_to = move
        self.move_relative = move_rel
        self.move_to_natural = natural_mouse_movement
        self.get_screen_resolution = get_resolution
        self.press_key = Press
        self.get_cursor_position = get_cursor
        self.is_cursor_shown = is_cursor_shown
        self.get_all_windows = get_window_infos
        self.send_keystrokes_to_hwnd = send_keystrokes
        self.activate_window = activate_window
        self.activate_topmost = activate_topmost
        self.deactivate_topmost = deactivate_topmost
        self.send_keys_to_hwnd = send_keys
        self.enable_failsafekill = start_failsafe
        self.get_elements_from_coords = get_elements_from_xy
        self.get_elements_from_hwnd = get_elements_from_hwnd
        self.get_single_element_from_coords = get_single_element_from_coord
        self.get_single_element_from_hwnd = get_single_element_from_hwnd
        self.left_click_xy_natural_relative = left_click_xy_natural_relative
        self.move_to_natural_relative = natural_mouse_movement_relative
        self.right_click_xy_natural_relative = right_click_xy_natural_relative
        self.force_activate_window = force_activate_window
        self.press_keys_simultaneously = press_multiple_keys
        self.press_keys_simultaneously_own_interval = press_multiple_keys_own_interval
        self.show_all_keys = allkeys
        self.left_mouse_down = left_mouse_down
        self.left_mouse_up = left_mouse_up
        self.right_mouse_down = right_mouse_down
        self.right_mouse_up = right_mouse_up
        self.middle_mouse_down = middle_mouse_down
        self.middle_mouse_up = middle_mouse_up
        self.t = kthread.KThread(target=self._get_cursor, name="get_cursor")
        self.show_cur = False

    def _kill_coord(self):
        self.show_cur = False
        time.sleep(0.05)
        self.show_cur = True

    def force_activate_window(self, hwnd):
        self.force_activate_window(hwnd)
        self.deactivate_topmost(hwnd)
        return self

    def _get_cursor(self):
        while True:
            if self.show_cur is False:
                break
            time.sleep(0.001)
            print(f"{get_cursor()}         ", end="\r")

    def start_showing_cursor_position(self, exit_keys="ctrl+l"):
        try:
            key_b.remove_hotkey(exit_keys)
        except Exception:
            pass
        if exit_keys not in key_b.__dict__["_hotkeys"]:
            key_b.add_hotkey(exit_keys, self._kill_coord)
        self.show_cur = True
        if not self.t.is_alive():
            try:
                self.t.start()
            except RuntimeError:
                self.t = kthread.KThread(target=self._get_cursor, name="get_cursor")
                self.t.start()
        else:
            try:
                self.t.kill()
            except Exception:
                pass
            self.t = kthread.KThread(target=self._get_cursor, name="get_cursor")
            self.t.start()

    def stop_showing_cursor_position(self):
        self.show_cur = False

    def show_rgb_values_at_mouse_position(
            self,
            sleeptime=0.01,
            on_left_click=False,
            on_right_click=False,
            rgb_values=True,
            rgba_values=True,
            coords=True,
            time_value=True,
    ):
        return get_rgb_values(
            sleeptime=sleeptime,
            on_left_click=on_left_click,
            on_right_click=on_right_click,
            rgb_values=rgb_values,
            rgba_values=rgba_values,
            coords=coords,
            time_value=time_value,
        )
