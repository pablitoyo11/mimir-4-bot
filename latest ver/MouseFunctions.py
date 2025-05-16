import pyHM
import time
import random
from pyHM import mouse

"""
def move_mouse_with_pyhm(target_x, target_y, duration):
def click_current_position():
def drag_mouse(start_x, start_y, target_x, target_y, duration):
"""

def move_mouse_with_pyhm(target_x, target_y, duration):
    duration = random.uniform(2, (duration / 10))
    multiplier = random.uniform(0.5, min(5, duration / 2))
    overshoot_x = target_x + random.uniform(random.uniform(0, 5), random.uniform(9, 11))
    overshoot_y = target_y + random.uniform(random.uniform(0, 5), random.uniform(9, 11))
    mouse.move(overshoot_x, overshoot_y, multiplier)
    time.sleep(random.uniform(0.05,0.15))
    mouse.move(target_x, target_y, multiplier*random.uniform(50,100))

def click_current_position():  
    current_x, current_y = mouse.get_current_position()
    mouse.down()
    time.sleep(random.uniform(0, 0.1))  ##
    mouse.up()

def drag_mouse(start_x, start_y, target_x, target_y, duration):
    from pyHM import mouse
    move_mouse_with_pyhm(start_x, start_y, duration)
    mouse.down()
    time.sleep(random.uniform(0, 0.1))  ##
    move_mouse_with_pyhm(target_x, target_y, duration)
    mouse.up()

def double_click_current_position():
    mouse.double_click()


