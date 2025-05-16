import pygetwindow
import pyautogui
from PIL import Image
from time import sleep
import os

"""
def identify_mir(window_title):
def bring_window_to_front(window_title):
def capture_window_screenshot(window_title):
def save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file):
"""

"""
window_title = "Mir4G[1]" #change to variable to be sent from another module
# Replace with title of the window you want to capture
"""
def identify_mir(window_title):
    try:
        print(f"window found: {window_title}")
        return pygetwindow.getWindowsWithTitle(window_title)[0]  #first window to global variable
    except IndexError:
        print(f"No window found with title: {window_title}")
        return

def bring_window_to_front(window_title):
    window=identify_mir(window_title)
    window.activate() # Bring the window to the front
    window.restore()  # Restore the window if it is minimized
    window.resizeTo(640, 375) # Forcing size for image comparison later
##    sleep(0) #Delay might be needed some times waiting computer to bring window to front
    print(f"Window with title '{window_title}' brought to front.")

def capture_window_screenshot(window_title):
    window=identify_mir(window_title)
    bring_window_to_front(window_title)
    x_start, y_start, x_end, y_end = window.left, window.top, window.right, window.bottom
    try:
        # Create folder for screenshots
        folder_path = ("./tmpscreens")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception as error:
        print(f"Error creating folder")
        
    # full screenshot
    screenshot = pyautogui.screenshot()
    # area to cut from window rects(x_start, y_start, x_end, y_end)
    cut_area = (x_start, y_start, x_end, y_end)
    # Cut the defined area from the screenshot
    cropped_image = screenshot.crop(cut_area)
    # Save the cropped image
    cropped_image.save(f"tmpscreens/{window_title}.dev.png")
    


def save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file):
    # Load the image
    image = Image.open(f"tmpscreens/{window_title}.dev.png")
    img_width, img_height = image.size
    
    try:
        # Create folder for screenshots
        folder_path = (f"./tmpscreens/{window_title} dev")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
    except Exception as error:
        print(f"Error creating folder")

    # Calculate the actual pixel values with the % given
    x_start = int(img_width * x_percent)
    y_start = int(img_height * y_percent)
    x_end = int(img_width * width_percent)
    y_end = int(img_height * height_percent)

    # Cut the defined area from the image
    cropped_image = image.crop((x_start, y_start, x_end, y_end))
    cropped_image.save(f"tmpscreens/{window_title} dev/{output_file}.dev.png")    # Save
##    cropped_image.show()     #Show image
    print(f"{output_file} Part of the image has been saved to {window_title} dev _{output_file}.dev.png")


# Example usage
window_title = "Mir4G[1]" # Replace with title of the window you want to capture
output_file = "devarea"
"""
saving mode middle area screen
x_percent = 0.46
y_percent = 0.8
width_percent = 0.537
height_percent = 0.84
"""
"""
center of the screen mining/opening/etc area
x_percent = 0.41
y_percent = 0.655
width_percent = 0.595
height_percent = 0.735
"""
"""
Map name area 515 70 605 85
x_percent = 0.80
y_percent = 0.185
width_percent = 0.945
height_percent = 0.23
"""
x_percent = 00
y_percent = 0
width_percent = 1
height_percent = 1
capture_window_screenshot(window_title)

save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file)

"""
640x375 achicando a mano
1296*759 tamaño que abre
# Example usage: save_part_of_image
# Cut and save part of the image as percentages (x_percent, y_percent, width_percent, height_percent)
window_title = window_title  # Replace with your image file path
x_percent = 0.75
y_percent = 0.25
width_percent = 0.98
height_percent = 0.35
output_file = "part"

save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file)
"""


