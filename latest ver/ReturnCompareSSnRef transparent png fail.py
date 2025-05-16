from MirWindowHandler import save_part_of_image

import cv2
import numpy as np

def cut_and_compare(window_title, x_percent, y_percent, width_percent, height_percent, output_file):
    # Cut from screenshot and save
    save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file)
    
    # Load the image and ref image
    large_image = cv2.imread(f"tmpscreens/{window_title}/{output_file}.png")
    icon_image = cv2.imread(f"refimages/{output_file}.png", cv2.IMREAD_UNCHANGED)
    
    # Check if the images were loaded successfully
    if large_image is None:
        raise FileNotFoundError("The large image could not be loaded. Please check the file path.")
    if icon_image is None:
        raise FileNotFoundError("The icon image could not be loaded. Please check the file path.")
    
    # Convert the large image to grayscale
    large_gray = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    
    # Extract the alpha channel from the template (icon) and create a mask
    alpha_channel = icon_image[:, :, 3]
    _, mask = cv2.threshold(alpha_channel, 1, 255, cv2.THRESH_BINARY)
    
    # Convert the template (icon) to grayscale
    icon_gray = cv2.cvtColor(icon_image[:, :, :3], cv2.COLOR_BGR2GRAY)
    
    # Apply the mask to the grayscale template
    icon_gray = cv2.bitwise_and(icon_gray, icon_gray, mask=mask)
    
    # Perform template matching
    result = cv2.matchTemplate(large_gray, icon_gray, cv2.TM_CCOEFF_NORMED)
    
    # Get the best match position
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    # Set a confidence threshold
    # threshold = 0.95
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
