# lib   
from mousekey import MouseKey
from time import sleep, time
import random
import pyautogui
import os
from datetime import datetime


mkey = MouseKey()

# for stop execution: press CTRL + E 
mkey.enable_failsafekill('ctrl+e')
# select de windows game(just 1920x1080 resolution) 
# !! change de x= and y= if your resolution be diferent !! 
mkey.left_click_xy_natural(x=1456,y=502,print_coords=False) 

# nothing to see.....