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

def press_key_in_game(window_title, key):
    bring_window_to_front(window_title)
    press(key)
    print(f"Pressed {key} in {window_title}")

def get_window_click_area_randomizer(x_start,y_start,x_end,y_end,window_title,duration):
    #modify x_size=0 or y_size=0 to adjust random of center point
    window = identify_mir(window_title)
    bring_window_to_front(window_title)
    win_width, win_height = window.width, window.height
    print(x_start,y_start,x_end,y_end)
    # Swap values if start is bigger than  end
    if x_start > x_end:
        x_start, x_end = x_end, x_start  
    if y_start > y_end:
        y_start, y_end = y_end, y_start
    print(x_start,y_start,x_end,y_end)
    #make area smaller by 01% to avoid edge clicking
    #starting x and y higher, and ending x and y smaller, to make area smaller
    x_start *=1.01
    y_start *=1.01
    x_end *=0.99
    y_end *=0.99
    print("final size")
    print(x_start,y_start,x_end,y_end)
    #get pixel space rects on different mir sizes based on percent of reference position
    x_start = int(window.left + win_width * x_start)
    y_start = int(window.top + win_height * y_start)
    x_end = int(window.left + win_width * x_end)
    y_end = int(window.top + win_height * y_end)
    print("final pos")
    print(x_start,y_start,x_end,y_end)
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


