# lib   
from mousekey import MouseKey
from time import sleep, time
import random
import pyautogui
import os
from datetime import datetime

mkey = MouseKey()
possibilities = 2.5,2.6,2.7,2.8,2.9,3

# for stop execution: press CTRL + E 
mkey.enable_failsafekill('ctrl+e')

# select de windows game(just 1920x1080 resolution) 
# !! change de x= and y= if your resolution be diferent !! 
mkey.left_click_xy_natural(x=1042,y=630,print_coords=False) 

# variables
counter = 0
im_live = "yes"
counter2 = 0
pyautogui.press('b')

while im_live == "yes":
    # detect if you die
    try:
        death_x, death_y = pyautogui.locateCenterOnScreen('morto.png',confidence=0.5)
        
        # ok, now you're dead and we'll take you for some air
        os.system('cls')
        print('Voce morreu, em 5 segundos levaremos voce para farmar energia.')
        sleep(5)
        pyautogui.click(death_x,death_y)
        os.system('cls')
        print('A caminho do farm de energia, aguarde.')
        sleep(7)
        
        # open map
        pyautogui.press('f10')
        sleep(1)
        
        # open favorites places
        look_map_x,look_map_y = pyautogui.locateCenterOnScreen('map.png',confidence=0.7)
        pyautogui.click(x=look_map_x,y=look_map_y, interval=0.5)
        sleep(0.5)
        
        # select de energy
        energia_x,energia_y = pyautogui.locateCenterOnScreen('energia.png',confidence=0.7)
        pyautogui.click(x=energia_x,y=energia_y, interval=0.5)
        
        # teleport to and keep mining
        tp_x,tp_y = pyautogui.locateCenterOnScreen('tp.png',confidence=0.7)
        pyautogui.click(x=tp_x,y=tp_y, interval=0.5)
        sleep(10)
        pyautogui.press('n')
        os.system('cls')
        
        # print good bye 
        print(f'Você morreu as {datetime.now().strftime("%H:%M")}')
        im_live = "not"
    # if not die, execute this
    except:
        os.system('cls')
        counter2 += 1
        print('ainda vivo', counter2)
        # open battle menu
        sleep(0.2)
        pyautogui.press('tab')
        
        # select mob on battle menu(random selection, not AI or other thing)
        pyautogui.press('pageUP',presses=(random.randint(2,4)))
        pyautogui.press('f')
        sleep(random.choice(possibilities))
        counter +=1
        if counter == 6:
            counter -= 6
            pyautogui.press('r')