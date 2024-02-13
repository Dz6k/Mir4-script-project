import threading
import win32gui, win32ui, win32con
from random import randint, choice
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
import pyautogui
# Variáveis globais
parar_threads = False

# variables
ultimate = True # use ultimate set to True // don't use ultimate set to False


def stealthfarm_ultimate(game):
    global parar_threads
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
        try:
            sleep(possibilities)
        except:
            sleep(choice(possibilities))
        if ultimate:    
            win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)

    
def stealthfarm(game):
    global parar_threads
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
        try:
            sleep(possibilities)
        except:
            sleep(choice(possibilities))
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)

def loop_tab(game):
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)

    global parar_threads
    while not parar_threads:
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.2)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        sleep(0.2)

def stop_threads():
    
    global parar_threads
    parar_threads = True

def start():
    global parar_threads
    parar_threads = False
    instancias = pyautogui.prompt(text='Numero das janela', title='Seletor')
    global possibilities
    escolher_time = pyautogui.prompt(title='Loop', text='Escolha o tempo, em segundos, da troca de alvo\nCaso nao queira escolher, é so prosseguir sem digitar nada')
    escolher_time

    if len(escolher_time) > 0:
        possibilities = int(escolher_time)
    else:
        possibilities = 1.75,2,2.25,2.5,2.75,3
    if instancias:
        process = []
        for indice in str(instancias):
            try:
                app = Application().connect(title=f'Mir4G[{indice}]') 
                app_text = app.window().texts() 
                process += app_text
            except:
                ...

    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm, args=(i,), name=thread_name)
        tab = threading.Thread(target=loop_tab, args=(i,), name=thread_name)
        farm.start()
        tab.start()
def start_ultimate():
    global parar_threads
    parar_threads = False
    instancias = pyautogui.prompt(text='Numero das janela', title='Seletor')
    global possibilities
    escolher_time = pyautogui.prompt(title='Loop', text='Escolha o tempo, em segundos, da troca de alvo\nCaso nao queira escolher, é so prosseguir sem digitar nada')
    escolher_time

    if len(escolher_time) > 0:
        possibilities = int(escolher_time)
    else:
        possibilities = 1.75,2,2.25,2.5,2.75,3
    if instancias:
        process = []
        for indice in str(instancias):
            try:
                app = Application().connect(title=f'Mir4G[{indice}]') 
                app_text = app.window().texts() 
                process += app_text
            except:
                ...

    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm_ultimate, args=(i,), name=thread_name)
        tab = threading.Thread(target=loop_tab, args=(i,), name=thread_name)
        
        farm.start()
        tab.start()
