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
possibilities = 1.75,2,2.25,2.5,2.75,3

def stealthfarm_ultimate(game):
    global possibilities
    global parar_threads
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')  
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    # b
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    sleep(0.2)

    while not parar_threads:
        # tab
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        # loop randomizado pageup
        for i in range(randint(2,4)):
            win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
        # f
        sleep(0.3)
        win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
        
        try:
            sleep(possibilities)
        except:
            sleep(choice(possibilities))
        # r
        win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
    # b
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)

    
def stealthfarm(game):
    global possibilities
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
        
        # pageup
        for i in range(randint(2,4)):
            win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
        # f
        sleep(0.3)
        win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
        # timing do loop
        try:
            sleep(possibilities)
        except:
            sleep(choice(possibilities))
    # b
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)

# para threads
def stop_threads():
    global parar_threads
    parar_threads = True

# criar threads
def start():
    global parar_threads
    parar_threads = False
    instancias = []
    instancias2 = pyautogui.prompt(text='Numero das janela', title='Seletor')
    if instancias2:
        instancias = [int(x) for x in re.split('[, ]+', instancias2.strip()) if x]
    global possibilities
    escolher_time = pyautogui.prompt(title='Loop', text='Escolha o tempo, em segundos e em numeros inteiros, da troca de alvo\nCaso nao queira escolher, é so prosseguir sem digitar nada')
    escolher_time
    
    # condicional de tempo
    if len(escolher_time) > 0:
        possibilities = int(escolher_time)
    else:
        possibilities = 1.75,2,2.25,2.5,2.75,3
    
    # loop procurando instancias mir4g[]
    if instancias:
        process = []
        for indice in instancias:
            try:
                app = Application().connect(title=f'Mir4G[{indice}]') 
                app_text = app.window().texts() 
                process.append(app_text)
            except:
                ...
    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm_ultimate, args=(i,), name=thread_name)
        
        farm.start()

def start_ultimate():
    global parar_threads
    parar_threads = False
    instancias = []
    instancias2 = pyautogui.prompt(text='Numero das janela', title='Seletor')
    if instancias2:
        instancias = [int(x) for x in re.split('[, ]+', instancias2.strip()) if x]
    global possibilities
    escolher_time = pyautogui.prompt(title='Loop', text='Escolha o tempo, em segundos, da troca de alvo\nCaso nao queira escolher, é so prosseguir sem digitar nada')
    escolher_time
    
    if len(escolher_time) > 0:
        possibilities = int(escolher_time)
    else:
        possibilities = 1.75,2,2.25,2.5,2.75,3
    if instancias:
        process = []
        for indice in instancias:
            try:
                app = Application().connect(title=f'Mir4G[{indice}]') 
                app_text = app.window().texts() 
                process.append(app_text)
            except:
                ...
    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm_ultimate, args=(i,), name=thread_name)
        
        farm.start()
