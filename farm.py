# lib   
from mousekey import MouseKey
from time import sleep, time
import random
import pyautogui
import os

mkey = MouseKey()
possibilities = 2.5,2.6,2.7,2.8,2.9,3

# stop execution
mkey.enable_failsafekill('ctrl+e')

# select de windows game(just 1920x1080 resolution)
mkey.left_click_xy_natural(x=1042,y=630,print_coords=False) 


counter = 0
eu_morri = "nao"
contador = 0
pyautogui.press('b')
while eu_morri == "nao":
    try:
        death_x, death_y = pyautogui.locateCenterOnScreen('morto.png',confidence=0.5)
        # go mining for don't keep akf
        os.system('cls')
        print('Voce morreu, em 5 segundos levaremos voce para farmar energia.')
        sleep(5)
        pyautogui.click(death_x,death_y)
        sleep(10)
        pyautogui.press('f10')
        sleep(1)
        look_map_x,look_map_y = pyautogui.locateCenterOnScreen('map.png',confidence=0.7)
        pyautogui.click(x=look_map_x,y=look_map_y, interval=0.5)
        sleep(0.5)
        energia_x,energia_y = pyautogui.locateCenterOnScreen('energia.png',confidence=0.7)
        pyautogui.click(x=energia_x,y=energia_y, interval=0.5)
        tp_x,tp_y = pyautogui.locateCenterOnScreen('tp.png',confidence=0.7)
        pyautogui.click(x=tp_x,y=tp_y, interval=0.5)
        sleep(10)
        pyautogui.press('n')
        eu_morri = "sim"
    
    except:
        os.system('cls')
        contador += 1
        print('ainda vivo', contador)
        # open battle menu
        sleep(0.2)
        pyautogui.press('tab')
        
        # select mob on battle menu(random selection, not AI or other thing)
        pyautogui.press('pageUP',presses=(random.randint(2,3)))
        pyautogui.press('f')
        sleep(random.choice(possibilities))
        counter +=1
        if counter == 6:
            counter -= 6
            pyautogui.press('r')