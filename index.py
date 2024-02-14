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














def start_simple():
    instancias = pyautogui.prompt(text='Numero da janela(Apenas uma janela!)', title='Seletor')
    global parar_threads
    parar_threads = False
    if instancias:
        process = []
        for indice in str(instancias):
            try:
                app = Application().connect(title=f'Mir4G[{indice}]') 
                app_text = app.window().texts() 
                app_text2 = app.window()
                
                print(app_text,app_text2)
                process += app_text
            except:
                pass

start_simple()