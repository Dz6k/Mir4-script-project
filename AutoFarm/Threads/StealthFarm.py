# type: ignore
import threading
import win32gui, win32ui, win32con
from random import randint, choice
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
import random

# Variáveis globais
parar_threads = False


def stealthfarm(game, ultimate: bool = False):
    global parar_threads
    POSSIBILITIES = [round(random.uniform(1, 3), 3) for _ in range(10)]
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    sleep(0.2)

    while not parar_threads:
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        
        for i in range(randint(2,4)):
            win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
        
        sleep(0.3)
        win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
        
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)

        sleep(choice(POSSIBILITIES))

        if ultimate is True:
            win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
            
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)


def stop_threads_auto():
    
    global parar_threads
    parar_threads = True


def start_auto():
    global parar_threads
    parar_threads = False
    process = []
    for indice in range(0, 20):
        try:
            app = Application().connect(title=f'Mir4G[{indice}]') 
            app_text = app.window().texts() 
            process += app_text
            for i in process:
                thread_name = f"MinhaThread-{i}"
                farm = threading.Thread(
                    target=stealthfarm, args=(i,), name=thread_name)

                farm.start()
        except:
            ...


def start_auto_ultimate():
    global parar_threads
    parar_threads = False
    process = []
    for indice in range(0, 20):
        try:
            app = Application().connect(title=f'Mir4G[{indice}]') 
            app_text = app.window().texts() 
            process += app_text
            for i in process:
                thread_name = f"MinhaThread-{i}"
                farm = threading.Thread(
                    target=stealthfarm, args=(i, True), name=thread_name)

                farm.start()
        except:
            ...


def run_auto():
    bot = threading.Thread(target=lambda: start_auto()).start()


def run_ultimate():
    bot = threading.Thread(target=lambda: start_auto_ultimate()).start()
