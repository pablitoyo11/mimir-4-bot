from ReturnCompareSSnRef import cut_and_compare
#def cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file):
from ClickAtMir import get_window_click_space_randomizer
#def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):


#example use
window_title = "Mir4G[1]"
#english area
##x_percent = 0.755
##y_percent = 0.816
##width_percent = 0.94
##height_percent = 0.885
#chinesse area
x_percent = 0.780
y_percent = 0.815
width_percent = 0.945
height_percent = 0.885
output_file = "respawn1"

def respawn_check():
    SSnRef_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
    # Click at the matched region if confidence is above the threshold
    threshold= 0.95
    if SSnRef_val >= threshold:
##        print(f"match found with confidence {SSnRef_val}, clicking")
##        print("respawn_on")
        # Transform search area to smaller clickable area, to avoid edge click and missmatch
        smaller_xs = x_percent / 0.98 
        smaller_ys = y_percent / 0.98
        smaller_xe = width_percent * 0.98
        smaller_ye = height_percent * 0.98
        duration = 0.000001
        get_window_click_space_randomizer(smaller_xs,smaller_ys,smaller_xe,smaller_ye,window_title,duration)
        return "respawn_on"
    else:
##        print(f"No match found with confidence. Best: {SSnRef_val}")
##        print("respawn_off")
        return "respawn_off"




