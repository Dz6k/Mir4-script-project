# type: ignore
import threading
import win32gui, win32ui, win32con
from random import randint, choice
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
import pyautogui
import re
import random

# Variáveis globais
parar_threads = False


def stealthfarm(game, ult: bool = False):
    possibilities = [round(random.uniform(1, 3), 3) for _ in range(10)]
    global parar_threads
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')  
    window_name = f'{game[0]}'
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

        sleep(choice(possibilities))

        if ult is True:
            # r
            win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
    # b
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)


# para threads
def stop_threads_manual():
    global parar_threads
    parar_threads = True

# criar threads


def start_manual():
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
                # print(app)
                # print(app_text)
                process.append(app_text)
                for i in process:
                    thread_name = f"MinhaThread-{i}"
                    farm = threading.Thread(
                        target=stealthfarm, args=(i, False), name=thread_name)

                    farm.start()
            except:
                ...


def start_ultimate_manual():
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
                for i in process:
                    thread_name = f"MinhaThread-{i}"
                    farm = threading.Thread(
                        target=stealthfarm, args=(i, True), name=thread_name)

                    farm.start()
            except:
                ...
