# lib   
import threading
import os
import win32gui, win32ui, win32con
from random import randint, choice
from mousekey import MouseKey
from time import sleep

# variables
ultimate = True # use ultimate set to True // don't use ultimate set to False
possibilities = 1.75,2,2.25,2.5,2.75,3

# for stop execution: press CTRL + E 
mkey = MouseKey()
mkey.enable_failsafekill('ctrl+e')

def stealthfarm(game):

    # find the mir4 
    window_name = f'Mir4G[{game}]'
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
            sleep(0.05)
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
            sleep(0.05)
            win.SendMessage(win32con.WM_KEYUP, 0x52, 0)

def loop_tab():
    # find the mir4 
    window_name = 'Mir4G[1]'
    hwnd = win32gui.FindWindow(None,window_name)
    win = win32ui.CreateWindowFromHandle(hwnd)

        
    while True:
        # tab
        win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
        sleep(0.2)
        win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
        sleep(0.2)

os.system('cls')
if instancia:=input('Qual número do jogo instanciado: '):
    os.system('cls')
    print('iniciado.')
    try:
        farm = threading.Thread(target=stealthfarm(instancia)) 
        tab = threading.Thread(target=loop_tab())
        farm.start()
        tab.start()
    except win32ui.error:
        print('instancia errada, verifique e tente novamente,')

