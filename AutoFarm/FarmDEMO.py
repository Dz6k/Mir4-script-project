# lib   
import random
import pyautogui
from mousekey import MouseKey
from time import sleep
from pywinauto import Application
import threading

def farm():
    # check resolution
    RESOLUTION = 1920,1080
    check_resolution = pyautogui.resolution()
    if check_resolution != RESOLUTION:
        return print('Essa aplicacao é somente para monitores 1920x1080')
    
    app = Application().connect(title='Mir4G[1]')   
    app.window().set_focus()
    mkey = MouseKey()
    possibilities = 1.75,2,2.25,2.5,2.75,3
    
    # for stop execution: press CTRL + E 
    mkey.enable_failsafekill('ctrl+e')
    
    # variables

    # start auto atack
    pyautogui.press('b')
    while True:
        #os.system('cls')
        # open battle menu
        sleep(0.2)
        pyautogui.press('tab')
        
        # select mob on battle menu(random selection, not AI or other thing)
        pyautogui.press('pageUP',presses=(random.randint(2,4)))
        pyautogui.press('f')
        sleep(random.choice(possibilities))
        if ultimate:
            pyautogui.press('r')
            
def start_simple_demo():
    farm_demo = threading.Thread(target=farm)
    farm_demo.start()





