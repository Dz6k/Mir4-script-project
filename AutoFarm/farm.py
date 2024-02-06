# lib   
import random
import pyautogui
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
from datetime import datetime
import threading

mkey = MouseKey()
POSSILITIES = 1.75,2,2.25,2.5,2.75,3
# for stop execution: press CTRL + E 
mkey.enable_failsafekill('ctrl+e')

def farm_die_on():
    # check resolution
    RESOLUTION = 1920,1080
        # code stop if resolution is not same FHD
    if pyautogui.resolution() != RESOLUTION:
        pyautogui.alert(button='ok',text='Resolucao nao suportada')
        return farm_die_on
    # Select and focus the mir4 process
    app = Application().connect(title=f'Mir4G[1]')   
    app.window().set_focus()
    
    # variables
    im_live = "yes"
    
    sleep(0.5)
    # start auto atack
    pyautogui.press('b')
    while im_live == "yes":
        # detect if you die    
        try:
            #find the revive button  in especific area on your monitor
            death = pyautogui.locateOnScreen('imagens\morto.png', region=(1621,858,300,170),confidence=0.7)

            # ok, now you're dead and we'll take you for some air
            sleep(15)
            pyautogui.click(death)
            sleep(15)
            
            # open map
            pyautogui.press('f10')
            sleep(1)
            
            # open favorites places
            look_map_x,look_map_y = pyautogui.locateCenterOnScreen('imagens\map.png',confidence=0.7)
            pyautogui.click(x=look_map_x,y=look_map_y, duration=0.5)
            sleep(0.5)

            # select de energy
            energia_x,energia_y = pyautogui.locateCenterOnScreen('imagens\energia.png',confidence=0.7)
            pyautogui.click(x=energia_x,y=energia_y, duration=0.5)
            
            # teleport to and keep mining
            tp_x,tp_y = pyautogui.locateCenterOnScreen('imagens\\tp.png',confidence=0.7)
            pyautogui.click(x=tp_x,y=tp_y, duration=0.5)
            sleep(15)

            pyautogui.press('n')

            # print good bye 
            pyautogui.alert(button='ok',text=f'Você morreu as {datetime.now().strftime("%H:%M")}')

        # if not die, execute this
        except pyautogui.ImageNotFoundException:

            # open battle menu
            sleep(0.2)

            pyautogui.press('tab')

            # select mob on battle menu(random selection, not AI or other thing)

            pyautogui.press('pageUP',presses=(random.randint(2,4)))
            
            sleep(0.3)
            pyautogui.press('f')
            sleep(random.choice(POSSILITIES))
            
def farm_die_on_ultimate():
    # check resolution
    RESOLUTION = 1920,1080
    if pyautogui.resolution() != RESOLUTION:
        pyautogui.alert(button='ok',text='Resolucao nao suportada')
        return farm_die_on_ultimate
        # code stop if resolution is not same FHD

    # Select and focus the mir4 process
    app = Application().connect(title=f'Mir4G[1]')   
    app.window().set_focus()

    # variables
    ultimate = True # use ultimate set to True // don't use ultimate set to False
    im_live = "yes"
    
    sleep(0.5)
    # start auto atack
    pyautogui.press('b')
    
    while im_live == "yes":
        # detect if you die    
        try:
            #find the revive button  in especific area on your monitor
            death = pyautogui.locateOnScreen('imagens\morto.png', region=(1621,858,300,170),confidence=0.7)
            sleep(15)
            pyautogui.click(death)
            sleep(15)
            
            # open map
            pyautogui.press('f10')
            sleep(1)
            
            # open favorites places
            look_map_x,look_map_y = pyautogui.locateCenterOnScreen('imagens\map.png',confidence=0.7)
            pyautogui.click(x=look_map_x,y=look_map_y, duration=0.5)
            sleep(0.5)
            
            # select de energy
            energia_x,energia_y = pyautogui.locateCenterOnScreen('imagens\energia.png',confidence=0.7)
            pyautogui.click(x=energia_x,y=energia_y, duration=0.5)
            
            # teleport to and keep farming
            tp_x,tp_y = pyautogui.locateCenterOnScreen('imagens\\tp.png',confidence=0.7)
            pyautogui.click(x=tp_x,y=tp_y, duration=0.5)
            sleep(15)
            pyautogui.press('n')
            
            # print good bye 
            pyautogui.alert(button='ok',text=f'Você morreu as {datetime.now().strftime("%H:%M")}')
            im_live = "not"
            
        # if not die, execute this
        except pyautogui.ImageNotFoundException:
            
            # open battle menu
            sleep(0.2)
            pyautogui.press('tab')
            
            # select mob on battle menu(random selection, not AI or other thing)
            pyautogui.press('pageUP',presses=(random.randint(2,4)))
            pyautogui.press('f')
            sleep(random.choice(POSSILITIES))
            
            # loop ultimate
            if ultimate:
                pyautogui.press('r')

def start_simple():
        farm = threading.Thread(target=farm_die_on)
        farm.start()

def start_simple_ultimate():    
        farm = threading.Thread(target=farm_die_on_ultimate)
        farm.start()
