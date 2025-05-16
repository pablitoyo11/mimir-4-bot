##from AutomoveHandler import automove_check
from SSCompare_tmp_ref import automove_check
from MirWindowHandler import capture_window_screenshot
##from RespawnHandler import respawn_check
from SSCompare_tmp_ref import respawn_check
##from OpeningChestHandler import openingchest_check 
from SSCompare_tmp_ref import openingchest_check

try:
    while True:
        window_title = "Mir4G[1]"
        capture_window_screenshot(window_title)
        status = automove_check()
        print(f"This will run forever: {status}")
        status = respawn_check()
        print(f"This will run forever: {status}")
        status = openingchest_check()
        print(f"This will run forever: {status}")
except KeyboardInterrupt:
    print("Stopped by user")

