import win32gui, win32ui, win32con
from random import randint, choice
from time import sleep
import random

class Stealthfarm:
    '''farm script in all windows index Mir4G[]'''
    def __init__(self):
        self.__game: str = None
        self.__ultimate: bool = False
        self.__POSSIBILITIES = [round(random.uniform(1, 3), 3) for _ in range(10)]
        self.__stop: bool = False
        
    # property and setter for control script
    @property
    def game(self):
        return self.__game
    
    @game.setter
    def game(self, window_name: str):
        self.__game = window_name
        
    @property
    def ultimate(self):
        return self.__ultimate
    
    @ultimate.setter
    def ultimate(self, value: bool):
        self.__ultimate = value
        
    @property
    def stop(self):
        return self.__stop
    
    @stop.setter
    def stop(self, value: bool):
        self.__stop = value
        
    def run(self):
        self.win = win32ui.CreateWindowFromHandle(
            win32gui.FindWindow(
                None,
                self.__game[0]
            )
        )
        self.win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
        sleep(0.01)
        self.win.SendMessage(win32con.WM_KEYUP, 0x42, 0)
        sleep(0.2)

        while not self.__stop:
            self.win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
            sleep(0.1)
            self.win.SendMessage(win32con.WM_KEYUP, 0x09, 0)
            
            for i in range(randint(2,4)):
                self.win.SendMessage(win32con.WM_KEYUP, 0x21, 0)
                sleep(0.01)
                self.win.SendMessage(win32con.WM_KEYDOWN, 0x21, 0)
            
            sleep(0.3)
            self.win.SendMessage(win32con.WM_KEYDOWN, 0x46, 0)
            sleep(0.01)
            self.win.SendMessage(win32con.WM_KEYUP, 0x46, 0)
            
            self.win.SendMessage(win32con.WM_KEYDOWN, 0x09, 0)
            sleep(0.1)
            self.win.SendMessage(win32con.WM_KEYUP, 0x09, 0)

            sleep(choice(self.__POSSIBILITIES))

            if self.__ultimate:
                self.win.SendMessage(win32con.WM_KEYDOWN, 0x52, 0)
                sleep(0.01)
                self.win.SendMessage(win32con.WM_KEYUP, 0x52, 0)
                
        self.win.SendMessage(win32con.WM_KEYDOWN, 0x42, 0)
        sleep(0.01)
        self.win.SendMessage(win32con.WM_KEYUP, 0x42, 0)

