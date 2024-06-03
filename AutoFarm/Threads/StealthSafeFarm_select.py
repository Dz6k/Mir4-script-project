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
import pyautogui
from tkinter import messagebox


# Variáveis globais
tentativa = False
target_color = np.array([155, 9, 9])

# Variável global para controle de parada
parar_threads = False

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
    while not tentativa and not parar_threads:
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
            sleep(0.56)
            for i in range(10):
                win.SendMessage(win32con.WM_KEYDOWN, 0x30, 0)
                sleep(0.01)
                win.SendMessage(win32con.WM_KEYUP, 0x30, 0)
            break

# Função principal de farm
def stealthfarm(game):
    global possibilities
    global tentativa
    
    mkey = MouseKey()
    mkey.enable_failsafekill('ctrl+e')
    
    window_name = f'{game}'
    hwnd = win32gui.FindWindow(None, window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)
    
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.1)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
    while not tentativa and not parar_threads:
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
        sleep(0.2)
        win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x46, 0)

        # mais tab >.<
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.1)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        try:
            sleep(possibilities)
        except:
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
            break
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)     
    
def stealthfarm_ultimate(game):
    global possibilities
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
    
    global tentativa
    while not tentativa and not parar_threads:
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
        # r
        win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
        sleep(0.01)
        win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
        try:
            sleep(possibilities)
        except:
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
            break
        
    win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
    sleep(0.01)
    win.SendMessage(win32con.WM_KEYUP, 0x42, 0)     
    
def stop_safe():
    global parar_threads
    global tentativa
    tentativa = False
    parar_threads = True

def stop_safe():
    global parar_threads
    global tentativa
    tentativa = False
    parar_threads = True

def start_safe():
    messagebox.showwarning(title='Aviso',
                           message='Esta funcao ainda esta em fase de teste!\nEm breve mudaremos a maneira de deteccao!')
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

def start_safe_ultimate():
    global parar_threads
    messagebox.showwarning(title='Aviso',
                           message='Esta funcao ainda esta em fase de teste!\nEm breve mudaremos a maneira de deteccao!')
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
        color_check = threading.Thread(target=color_check_thread, args=(i,), name=thread_name)
        color_check.start()
        farm.start()
