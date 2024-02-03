# lib   
import threading
import win32gui, win32ui, win32con
from random import randint, choice
from mousekey import MouseKey
from time import sleep
from pywinauto import Application

# variables
ultimate = True # use ultimate set to True // don't use ultimate set to False
possibilities = 1.75,2,2.25,2.5,2.75,3

def stealthfarm_ultimate(game):
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    #os.system('cls')
    #print(f'{game} iniciado.')
    # find the mir4 
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    
    # auto atack
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    sleep(0.2)

    while True:
        # tab
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        
        # select a random mob
        for i in range(randint(2,4)):
            win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
        # confirm atack
        sleep(0.3)
        win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
        
        # more tab >.<
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        sleep(choice(possibilities))
        if ultimate:    
            win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x52, 0)

def stealthfarm(game):
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    #os.system('cls')
    #print(f'{game} iniciado.')
    # find the mir4 
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    
    # auto atack
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    sleep(0.2)

    while True:
        # tab
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        
        # select a random mob
        for i in range(randint(2,4)):
            win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
        # confirm atack
        sleep(0.3)
        win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
        
        # more tab >.<
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        sleep(choice(possibilities))

def loop_tab(game):
    # find the mir4 
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)

    # tab is never too much, right?
    while True:
        # tab
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.2)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        sleep(0.2)

def start():
    # Search all mir4 process
    process = []
    for indice in range(0,20):
        try:
            app = Application().connect(title=f'Mir4G[{indice}]') 
            app_text = app.window().texts() 
            process += app_text
        except:
            ...

    #os.system('cls')
    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm, args=(i,), name=thread_name)
        tab = threading.Thread(target=loop_tab, args=(i,), name=thread_name)
        farm.start()
        tab.start()

def start_ultimate():
    # Search all mir4 process
    process = []
    for indice in range(0,20):
        try:
            app = Application().connect(title=f'Mir4G[{indice}]') 
            app_text = app.window().texts() 
            process += app_text
        except:
            ...

    #os.system('cls')
    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm_ultimate, args=(i,), name=thread_name)
        tab = threading.Thread(target=loop_tab, args=(i,), name=thread_name)
        farm.start()
        tab.start()

