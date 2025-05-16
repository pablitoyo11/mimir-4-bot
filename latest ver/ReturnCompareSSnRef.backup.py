##from MouseFunctions import move_mouse_with_pyhm, click_current_position
##def move_mouse_with_pyhm(target_x, target_y, duration):
##def click_current_position():

from ClickAtMir import get_window_click_space_randomizer
##def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):
from MirWindowHandler import save_part_of_image
##def save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file):


##640x375 res for all tests and size for ref images and search
"""
window_title = "Mir4G[1]"  # Replace with mir and your image file path
x_percent = 0.74
y_percent = 0.80
width_percent = 0.95
height_percent = 0.90
output_file = "respawn"
save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file)
"""
""" area to search
x_percent = 0.74
y_percent = 0.80
width_percent = 0.95
height_percent = 0.90
"""
""" ref image
x_percent = 0.755
y_percent = 0.816
width_percent = 0.935
height_percent = 0.885
"""

import cv2

def cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file):
# Cut from screenshot and save
    save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file)
# Load the image and ref image
    large_image = cv2.imread(f"tmpscreens/{window_title}/{output_file}.png")
    icon_image = cv2.imread(f"refimages/{output_file}.png")
# Convert images to grayscale
    large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    icon_gray = cv2.cvtColor(icon_image, cv2.COLOR_BGR2GRAY)
# Perform template matching
    result = cv2.matchTemplate(large_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
# Get the best match position
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# Set a confidence threshold
    #threshold = 0.95
    return max_val

"""
# Draw a rectangle around the matched region if confidence is above the threshold
    if max_val >= threshold:
        print(f"Respawn match found with confidence {max_val}, clicking")
        ##def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):
        
        xs_percent = 0.755
        ys_percent = 0.816
        xe_percent = 0.935
        ye_percent = 0.885
        window_title = "Mir4G[1]"
        duration = 0.000001
        get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration)
        
    else:
        print(f"No Respawn match found with confidence. Best match confidence: {max_val}")
"""
"""
# Save the result
cv2.imwrite('result.png', large_image)

# Display the result
cv2.imshow('Result', large_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""








