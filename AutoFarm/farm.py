from random import randint
import random
import pyautogui
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
from datetime import datetime
import threading
from tkinter import messagebox
import win32gui, win32ui, win32con


POSSIBILITIES = 1.75, 2, 2.25, 2.5, 2.75, 3
parar_threads = False

def farm_die_on(game):
    global parar_threads
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    RESOLUTION = 1920, 1080
    if pyautogui.resolution() != RESOLUTION:
        messagebox.showerror(title='Erro',
                             message='Resolção nao suportada')
        return farm_die_on
    
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    
    im_live = "yes"
    sleep(0.5)
    # b
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    sleep(0.2)
    
    while im_live == "yes" and not parar_threads:
        try:
            death = pyautogui.locateOnScreen('AutoFarm\imagens\morto.png', confidence=0.8,grayscale=False)
            sleep(10)
            mkey.left_click_xy_natural(death[0],death[1])
            #pyautogui.click(death)
            sleep(7)
            pyautogui.press('f10')
            sleep(1)
            lookmap = pyautogui.locateCenterOnScreen('AutoFarm\imagens\map.png', confidence=0.7,grayscale=False)
            mkey.left_click_xy_natural(lookmap[0],lookmap[1])
            # pyautogui.click(x=look_map_x, y=look_map_y, duration=0.5)
            sleep(0.5)
            energia = pyautogui.locateCenterOnScreen('AutoFarm\imagens\energia.png', confidence=0.7,grayscale=False)
            mkey.left_click_xy_natural(energia[0],energia[1])
            sleep(1)
            #pyautogui.click(x=energia_x, y=energia_y, duration=0.5)
            tp = pyautogui.locateOnScreen('AutoFarm\imagens\\tp.png', confidence=0.6,grayscale=False)
            
            mkey.left_click_xy_natural(tp[0],tp[1])
            #pyautogui.click(tp, duration=0.5)
            sleep(10)
            # n
            win.SendMessage(win32con.WM_KEYDOWN, 0x4E, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x4E, 0)
            pyautogui.alert(button='ok', text=f'Você morreu as {datetime.now().strftime("%H:%M")}')
            im_live = "no"
            
        except pyautogui.ImageNotFoundException:
            # tab
            win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
            sleep(0.1)
            win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
            
            # pagup
            for i in range(randint(2,4)):
                win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
                sleep(0.01)
                win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
            sleep(0.3)
            
            # f
            win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
            sleep(random.choice(POSSIBILITIES))


def farm_die_on_ultimate(game):
    global parar_threads
    RESOLUTION = 1920, 1080
    if pyautogui.resolution() != RESOLUTION:
        pyautogui.alert(button='ok', text='Resolucao nao suportada')
        return farm_die_on_ultimate
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    
    im_live = "yes"
    sleep(0.5)
    
    # b
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    sleep(0.2)
    while im_live == "yes" and not parar_threads:
        try:
            death = pyautogui.locateOnScreen('AutoFarm\imagens\morto.png', confidence=0.8)
            sleep(10)
            pyautogui.click(death)
            sleep(10)
            pyautogui.press('f10')
            sleep(1)
            look_map_x, look_map_y = pyautogui.locateCenterOnScreen('AutoFarm\imagens\map.png', confidence=0.7)
            pyautogui.click(x=look_map_x, y=look_map_y, duration=0.5)
            sleep(0.5)
            energia_x, energia_y = pyautogui.locateCenterOnScreen('AutoFarm\imagens\energia.png', confidence=0.7)
            pyautogui.click(x=energia_x, y=energia_y, duration=0.5)
            tp_x, tp_y = pyautogui.locateCenterOnScreen('AutoFarm\imagens\\tp.png', confidence=0.7)
            pyautogui.click(x=tp_x, y=tp_y, duration=0.5)
            sleep(10)
            # n
            win.SendMessage(win32con.WM_KEYDOWN, 0x4E, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x4E, 0)
            pyautogui.alert(button='ok', text=f'Você morreu as {datetime.now().strftime("%H:%M")}')
            im_live = "no"
        except pyautogui.ImageNotFoundException:
            # tab
            win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
            sleep(0.1)
            win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
            
            # pagup
            for i in range(randint(2,4)):
                win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
                sleep(0.01)
                win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
            sleep(0.3)
            
            # f
            win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
            
            sleep(random.choice(POSSIBILITIES))
            # b
            win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
    
def start_simple():
    instancias = pyautogui.prompt(text='Numero das janela', title='Seletor')
    global parar_threads
    parar_threads = False
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
        farm = threading.Thread(target=farm_die_on, args=(i,), name=thread_name)
        farm.start()

def start_simple_ultimate():
    instancias = pyautogui.prompt(text='Numero das janela', title='Seletor')
    global parar_threads
    parar_threads = False
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
        farm = threading.Thread(target=farm_die_on_ultimate, args=(i,), name=thread_name)
        farm.start()



    
