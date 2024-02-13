import random
import pyautogui
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
from datetime import datetime
import threading
from tkinter import messagebox
POSSIBILITIES = 1.75, 2, 2.25, 2.5, 2.75, 3
parar_threads = False

def farm_die_on():
    global parar_threads
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    RESOLUTION = 1920, 1080
    if pyautogui.resolution() != RESOLUTION:
        messagebox.showerror(title='Erro',
                             message='Resolção nao suportada')
        return farm_die_on
    
    app = Application().connect(title=f'Mir4G[1]')
    app.window().set_focus()
    im_live = "yes"
    sleep(0.5)
    pyautogui.press('b')
    while im_live == "yes" and not parar_threads:
        try:
            death = pyautogui.locateOnScreen('imagens\morto.png', region=(1621, 858, 300, 170), confidence=0.7)
            sleep(15)
            pyautogui.click(death)
            sleep(15)
            pyautogui.press('f10')
            sleep(1)
            look_map_x, look_map_y = pyautogui.locateCenterOnScreen('imagens\map.png', confidence=0.7)
            pyautogui.click(x=look_map_x, y=look_map_y, duration=0.5)
            sleep(0.5)
            energia_x, energia_y = pyautogui.locateCenterOnScreen('imagens\energia.png', confidence=0.7)
            pyautogui.click(x=energia_x, y=energia_y, duration=0.5)
            tp_x, tp_y = pyautogui.locateCenterOnScreen('imagens\\tp.png', confidence=0.7)
            pyautogui.click(x=tp_x, y=tp_y, duration=0.5)
            sleep(15)
            pyautogui.press('n')
            pyautogui.alert(button='ok', text=f'Você morreu as {datetime.now().strftime("%H:%M")}')

        except pyautogui.ImageNotFoundException:
            sleep(0.2)
            pyautogui.press('tab')
            pyautogui.press('pageUP', presses=(random.randint(2, 4)))
            sleep(0.3)
            pyautogui.press('f')
            sleep(random.choice(POSSIBILITIES))
    pyautogui.press('b')

def farm_die_on_ultimate():
    global parar_threads
    RESOLUTION = 1920, 1080
    if pyautogui.resolution() != RESOLUTION:
        pyautogui.alert(button='ok', text='Resolucao nao suportada')
        return farm_die_on_ultimate
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    app = Application().connect(title=f'Mir4G[1]')
    app.window().set_focus()
    ultimate = True
    im_live = "yes"
    sleep(0.5)
    pyautogui.press('b')
    while im_live == "yes" and not parar_threads:
        try:
            death = pyautogui.locateOnScreen('imagens\morto.png', region=(1621, 858, 300, 170), confidence=0.7)
            sleep(15)
            pyautogui.click(death)
            sleep(15)
            pyautogui.press('f10')
            sleep(1)
            look_map_x, look_map_y = pyautogui.locateCenterOnScreen('imagens\map.png', confidence=0.7)
            pyautogui.click(x=look_map_x, y=look_map_y, duration=0.5)
            sleep(0.5)
            energia_x, energia_y = pyautogui.locateCenterOnScreen('imagens\energia.png', confidence=0.7)
            pyautogui.click(x=energia_x, y=energia_y, duration=0.5)
            tp_x, tp_y = pyautogui.locateCenterOnScreen('imagens\\tp.png', confidence=0.7)
            pyautogui.click(x=tp_x, y=tp_y, duration=0.5)
            sleep(15)
            pyautogui.press('n')
            pyautogui.alert(button='ok', text=f'Você morreu as {datetime.now().strftime("%H:%M")}')
            im_live = "not"

        except pyautogui.ImageNotFoundException:
            sleep(0.2)
            pyautogui.press('tab')
            pyautogui.press('pageUP', presses=(random.randint(2, 4)))
            pyautogui.press('f')
            sleep(random.choice(POSSIBILITIES))
            if ultimate:
                pyautogui.press('r')
    pyautogui.press('b')
def start_simple():
    global parar_threads
    parar_threads = False
    farm = threading.Thread(target=farm_die_on)
    farm.start()

def start_simple_ultimate():
    global parar_threads
    parar_threads = False
    farm = threading.Thread(target=farm_die_on_ultimate)
    farm.start()

def stop_simple():
    global parar_threads
    parar_threads = True
