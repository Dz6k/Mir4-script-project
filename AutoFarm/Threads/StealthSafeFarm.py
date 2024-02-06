import threading
import win32gui
import win32ui
import win32con
from random import randint, choice
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
import numpy as np
from PIL import ImageGrab


# Variáveis globais
tentativa = False
ultimate = True  # use ultimate set to True // don't use ultimate set to False
possibilities = [1.75, 2, 2.25, 2.5, 2.75, 3]
target_color = np.array([155, 9, 9])

# Função para verificar a cor na região de interesse
def check_color_in_roi(roi, target_color):
    color_difference = np.abs(roi - target_color)
    mean_difference = np.mean(color_difference, axis=(0, 1))
    return np.all(mean_difference < 50)  # Ajuste o limite conforme necessário

def capture_screen(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    screenshot = ImageGrab.grab(bbox=(rect[0], rect[1], rect[2], rect[3]))
    img = np.array(screenshot)
    img = img[:, :, :3]  # Remover o canal alpha
    return img

def color_check_thread(game):
    global tentativa
    while not tentativa:
        hwnd = win32gui.FindWindow(None, game)
        screenshot = capture_screen(hwnd)

        top_left_roi = screenshot[:100, :100]
        top_right_roi = screenshot[:100, -100:]
        bottom_left_roi = screenshot[-100:, :100]
        bottom_right_roi = screenshot[-100:, -100:]

        # Se a cor alvo for encontrada em algum dos cantos, pressionar a tecla "0"
        if (check_color_in_roi(top_left_roi, target_color) or
            check_color_in_roi(top_right_roi, target_color) or
            check_color_in_roi(bottom_left_roi, target_color) or
            check_color_in_roi(bottom_right_roi, target_color)):
        
            win = win32ui.CreateWindowFromHandle(hwnd)
            for x in range(3):
                win.SendMessage(win32con.WM_KEYDOWN, 0xA0, 0)
                sleep(0.01)
                win.SendMessage(win32con.WM_KEYUP, 0xA0, 0)
            sleep(0.2)
            for i in range(10):
                win.SendMessage(win32con.WM_KEYDOWN, 0x30, 0)
                sleep(0.01)
                win.SendMessage(win32con.WM_KEYUP, 0x30, 0)
            tentativa = True
        
# Função principal de farm
def stealthfarm(game):
    global tentativa
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None, window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.1)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    while not tentativa:
        # tab
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)

        # select a random mob
        for i in range(randint(2, 4)):
            win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)

        # confirmar ataque
        sleep(0.3)
        win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x46, 0)

        # mais tab >.<
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        sleep(choice(possibilities))
        
        # Capturar a tela e verificar a cor nos cantos da aplicação
        screenshot = capture_screen(hwnd)
        top_left_roi = screenshot[:100, :100]
        top_right_roi = screenshot[:100, -100:]
        bottom_left_roi = screenshot[-100:, :100]
        bottom_right_roi = screenshot[-100:, -100:]

        # Se a cor alvo for encontrada em algum dos cantos, pressionar a tecla "0"
        if (check_color_in_roi(top_left_roi, target_color) or
            check_color_in_roi(top_right_roi, target_color) or
            check_color_in_roi(bottom_left_roi, target_color) or
            check_color_in_roi(bottom_right_roi, target_color)):
            sleep(2)
            tentativa = True
            
def stealthfarm_ultimate(game):
    global tentativa
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    # auto atack
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    
    while not tentativa:
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
        if ultimate:    
            win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
            sleep(0.01)
            win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
        sleep(choice(possibilities))
        
        # Capturar a tela e verificar a cor nos cantos da aplicação
        screenshot = capture_screen(hwnd)
        top_left_roi = screenshot[:100, :100]
        top_right_roi = screenshot[:100, -100:]
        bottom_left_roi = screenshot[-100:, :100]
        bottom_right_roi = screenshot[-100:, -100:]

        # Se a cor alvo for encontrada em algum dos cantos, pressionar a tecla "0"
        if (check_color_in_roi(top_left_roi, target_color) or
            check_color_in_roi(top_right_roi, target_color) or
            check_color_in_roi(bottom_left_roi, target_color) or
            check_color_in_roi(bottom_right_roi, target_color)):
            sleep(2)
            tentativa = True
            
def start_safe():
    process = []

    for indice in range(0, 10):
        try:
            app = Application().connect(title=f'Mir4G[{indice}]')
            app_text = app.window().texts()
            process += app_text
        except:
            ...

    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm, args=(i,), name=thread_name)
        color_check = threading.Thread(target=color_check_thread, args=(i,), name=thread_name)
        color_check.start()
        farm.start()
        
def start__safe_ultimate():
    process = []

    for indice in range(0, 10):
        try:
            app = Application().connect(title=f'Mir4G[{indice}]')
            app_text = app.window().texts()
            process += app_text
        except:
            ...

    for i in process:
        thread_name = f"MinhaThread-{i}"
        farm = threading.Thread(target=stealthfarm_ultimate, args=(i,), name=thread_name)
        color_check = threading.Thread(target=color_check_thread, args=(i,), name=thread_name)
        color_check.start()
        farm.start()