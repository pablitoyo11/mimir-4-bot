import MouseFunctions
from MirWindowHandler import identify_mir,bring_window_to_front
import random
from pyautogui import press
##from collections import namedtuple

"""
def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):
def get_window_click_map_randomizer(x_percent,y_percent,window_title,duration):
"""
##window_title = "Mir4G[1]"

def press_key_in_game(key, window_title):
    bring_window_to_front(window_title)
    press(key)
    print(f"Pressed {key} in {window_title}")

def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):
    window = identify_mir(window_title)
    bring_window_to_front(window_title)
    win_width, win_height = window.width, window.height
    #make area smaller by 01% to avoid edge clicking
    #start x higher, and ending y should be smaller, to make area smaller
    xs_percent *=1.01
    ys_percent *=1.01
    xe_percent *=0.99
    ye_percent *=0.99
    #get pixel space rects on different mir sizes based on percent of reference position
    x_start = int(window.left + win_width * xs_percent)
    y_start = int(window.top + win_height * ys_percent)
    x_end = int(window.left + win_width * xe_percent)
    y_end = int(window.top + win_height * ye_percent)
##    ClickSpace = namedtuple('ClickSpace', ['x_start', 'y_start', 'x_end', 'y_end'])
##    return ClickSpace(x_start, y_start, x_end, y_end)
##    duration = 1
    #randomize a target point inside clickable space
    target_x = random.uniform(x_start, x_end)
    target_y = random.uniform(y_start, y_end)
    #move to location and click
    MouseFunctions.move_mouse_with_pyhm(target_x,target_y,duration)
    MouseFunctions.click_current_position()
    print(f"clicked at {target_x},{target_y} at {window_title}")

def get_window_click_map_randomizer(x_percent,y_percent,window_title,duration):
    window = identify_mir(window_title)
    bring_window_to_front(window_title)
    win_width, win_height = window.width, window.height
    #randomize target point inside clickable space adding 1 pixel random to map click
    target_x = (int(window.left + win_width * x_percent) + random.randint(-1, 1))
    target_y = (int(window.top + win_height * y_percent) + random.randint(0, 1)) #no negativo en y porque normalmente los menus se abren hacia arriba, y hacia abajo clickea fuera del objetivo
##    duration = random.uniform(0,50)
##    MouseFunctions.move_mouse_with_pyhm(target_x,target_y,duration)
##    ClickSpace = namedtuple('ClickSpace', ['x_pointran', 'y_pointran'])
##    return ClickSpace(x_start, y_start, x_end, y_end)
    #move to location and click
    MouseFunctions.move_mouse_with_pyhm(target_x,target_y,duration)
    MouseFunctions.click_current_position()
    print(f"clicked at {target_x},{target_y} at {window_title}")


##get_window_click_pos(xs_percent,ys_percent,xe_percent,ye_percent,window_title)   
##get_window_click_space_randomizer(0.1,0.0,0.3,0.39,"Mir4G[1]",1)
##get_window_click_map_randomizer(0.50,0.50,"Mir4G[1]",0.00001)
#click should be random pos between start-end

#move_mouse_with_pyhm(target_x,target_y,duration)
##target_x = random.uniform(ClickSpace.x_start, ClickSpace.x_end)
##target_y = random.uniform(ClickSpace.y_start, ClickSpace.y_end)
##duration = 0.001
##MouseFunctions.move_mouse_with_pyhm(target_x,target_y,duration)
##MouseFunctions.click_current_position()

##get_window_click_map_randomizer(0.5,0.9,"Mir4G[1]",5)

# respawn.py
"""
def respawn_action():
    print("This is the respawn action.")
    window_title = "Mir4G[1]"
    mir_window = MirWindowHandler.identify_mir(window_title)
    if mir_window:
        print(f"Identified window: {mir_window}")
"""


