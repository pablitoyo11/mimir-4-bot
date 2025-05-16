#ReturnCompareRef.py

from ClickAtMir import get_window_click_space_randomizer
##def get_window_click_space_randomizer(xs_percent,ys_percent,xe_percent,ye_percent,window_title,duration):
from MirWindowHandler import save_part_of_image
##def save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, output_file):
from MirWindowHandler import capture_window_screenshot
import cv2

"""
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
##cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file):
##compare(window_title, area_file, ref_file):
##def automove_check():
##def openingchest_check():
##def respawn_check():
##def map_check(intended_map_ref):


def cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file):
# Cut from saved screenshot and save area
    save_part_of_image(window_title, x_percent, y_percent, width_percent, height_percent, area_file)

def compare(window_title, area_file, ref_file):
# Load the image and ref image
    large_image = cv2.imread(f"tmpscreens/{window_title}/{area_file}.png")
    icon_image = cv2.imread(f"refimages/{ref_file}.png")
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


def respawn_check(window_title):
##    window_title = "Mir4G[1]"
##    #english area
##    x_percent = 0.755
##    y_percent = 0.816
##    width_percent = 0.94
##    height_percent = 0.885
##    chinesse area
    x_percent = 0.780
    y_percent = 0.815
    width_percent = 0.945
    height_percent = 0.885
    area_file = "ActiveScreenRespawn"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #resapwn btn ref1
    area_file = "ActiveScreenRespawn"
    ref_file = "respawn1"
    SSnRef_val = compare(window_title, area_file, ref_file)
##    SSnRef_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
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

def map_check(intended_map_ref, window_title):
##    window_title = "Mir4G[1]"
##    map name area
    print("mapcheck inside print")
    print(intended_map_ref)
    x_percent = 0.80
    y_percent = 0.185
    width_percent = 0.945
    height_percent = 0.23
    area_file = "CurrentMap"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #map ref to be received intended_map
    ref_file = f"map{intended_map_ref}"
##    print(window_title, area_file, ref_file)
    SSnRef_val = compare(window_title, area_file, ref_file)
##    SSnRef_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
    # Click to change map if matching map isn't the intended_map
    threshold= 0.7 # low threshold because of transparent background with notifications poping over
##    print(f" found  confidence {SSnRef_val}")
    if SSnRef_val <= threshold:
        # Transform search area to smaller clickable area, to avoid edge click and missmatch
        smaller_xs = x_percent / 0.98 
        smaller_ys = y_percent / 0.98
        smaller_xe = width_percent * 0.98
        smaller_ye = height_percent * 0.98
        duration = 0.000001
##        get_window_click_space_randomizer(smaller_xs,smaller_ys,smaller_xe,smaller_ye,window_title,duration)
##        print("map_off")        
        return "map_off"
    else:
##        print(f"No match found with confidence. Best: {SSnRef_val}")
##        print("map_on")
        return "map_on"
    

def automove_check(window_title):
    #example use
##    window_title = "Mir4G[1]"
##    area_file = "automove"
##    ref_file = "automovex"

    #area 1 active screen (character on view)
    x_percent = 0.35
    y_percent = 0.74
    width_percent = 0.55
    height_percent = 0.76
    area_file = "ActiveScreenAutomove"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #autmove Ref1
##    Ref1_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
    #autmove Ref1
    area_file = "ActiveScreenAutomove" #duplicated for informative use
    ref_file = "automove1" #reference image
    Ref1_val = compare(window_title, area_file, ref_file)
    #autmove Ref12
##    Ref12_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
    area_file = "ActiveScreenAutomove" #same cut area than before
    ref_file = "automove12" #new ref img
    Ref12_val = compare(window_title, area_file, ref_file)

    #area 2 inactive screen (idle or inactive character)
    x_percent = 0.46
    y_percent = 0.8
    width_percent = 0.537
    height_percent = 0.84
    area_file = "BlackScreenAutomove"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #autmove Ref2
##    Ref2_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
    area_file = "BlackScreenAutomove"
    ref_file = "automove2"
    Ref2_val = compare(window_title, area_file, ref_file)


    #keep highest value of confidence
    Best_Val = max(Ref1_val,Ref12_val,Ref2_val)

    # Click at the matched region if confidence is above the threshold
    threshold= 0.95
    if Best_Val>= threshold:
##        print(f"match found with confidence {Ref1_val}")
##        print("automove_onNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        # Transform search area to smaller clickable area, to avoid edge click and missmatch
        """
        smaller_xs = x_percent / 0.98 
        smaller_ys = y_percent / 0.98
        smaller_xe = width_percent * 0.98
        smaller_ye = height_percent * 0.98
        duration = 0.000001
        get_window_click_space_randomizer(smaller_xs,smaller_ys,smaller_xe,smaller_ye,window_title,duration)
        """
        return "automove_on"
    else:
##        print(f"No match found with confidence. Best: {Ref1_val}")
##        print("automove_ofFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFf")
        return "automove_off"




##from ReturnCompareSSnRef import cut_and_compare
#def cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
##from ClickAtMir import get_window_click_space_randomizer

##cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file):
##compare(window_title, area_file, ref_file):
def openingchest_check(window_title):
    #example use
##    window_title = "Mir4G[1]"
    #area 1 active screen
    x_percent = 0.41
    y_percent = 0.655
    width_percent = 0.595
    height_percent = 0.735
    area_file = "ActiveScreenOpening"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #openingchest ref1
    ref_file = "openingchest1"
    SSnRef1_val=compare(window_title, area_file, ref_file)
    
    #area 2 inactive screen
    x_percent = 0.44
    y_percent = 0.8
    width_percent = 0.56
    height_percent = 0.84
    area_file = "BlackScreenOpening"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #openingchest ref2
    ref_file = "openingchest2"
    SSnRef2_val=compare(window_title, area_file, ref_file)

    #keep highest value of confidence
    Best_Val = max(SSnRef1_val,SSnRef2_val)

    # Click at the matched region if confidence is above the threshold
    threshold= 0.95
    if Best_Val>= threshold:
##        print(f"match found with confidence {SSnRef1_val}")
##        print("openingchest_on")
        # Transform search area to smaller clickable area, to avoid edge click and missmatch
        """
        smaller_xs = x_percent / 0.98 
        smaller_ys = y_percent / 0.98
        smaller_xe = width_percent * 0.98
        smaller_ye = height_percent * 0.98
        duration = 0.000001
        get_window_click_space_randomizer(smaller_xs,smaller_ys,smaller_xe,smaller_ye,window_title,duration)
        """
        return "openingchest_on"
    else:
##        print(f"No match found with confidence. Best: {SSnRef1_val}")
##        print("openingchest_off")
        return "openingchest_off"

def autocollecting_check(window_title):
    #example use
##    window_title = "Mir4G[1]"
    #area 1 active screen
    x_percent = 0.41
    y_percent = 0.655
    width_percent = 0.595
    height_percent = 0.735
    area_file = "ActiveScreenCollectingSpace"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #openingchest ref1
    ref_file = "openingchest1"
    chestRef1_val=compare(window_title, area_file, ref_file)
    #collectingvoidorb ref1
    ref_file = "collectingvoidorb1"
    voidRef1_val=compare(window_title, area_file, ref_file)
    
    #area 2 inactive screen
    x_percent = 0.41
    y_percent = 0.79
    width_percent = 0.59
    height_percent = 0.85
    area_file = "BlackScreenCollectingSpace"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #openingchest ref2
    ref_file = "openingchest2"
    chestRef2_val=compare(window_title, area_file, ref_file)
    #collectingvoidorb ref2
    ref_file = "collectingvoidorb2"
    voidRef2_val=compare(window_title, area_file, ref_file)    

    #keep highest value of confidence
    Best_Val = max(chestRef1_val,chestRef2_val,voidRef1_val,voidRef2_val)

    # Click at the matched region if confidence is above the threshold
    threshold= 0.95
    if Best_Val>= threshold:
##        print(f"match found with confidence {SSnRef1_val}")
##        print("openingchest_on")
        # Transform search area to smaller clickable area, to avoid edge click and missmatch
        """
        smaller_xs = x_percent / 0.98 
        smaller_ys = y_percent / 0.98
        smaller_xe = width_percent * 0.98
        smaller_ye = height_percent * 0.98
        duration = 0.000001
        get_window_click_space_randomizer(smaller_xs,smaller_ys,smaller_xe,smaller_ye,window_title,duration)
        """
        return "autocollecting_on"
    else:
##        print(f"No match found with confidence. Best: {SSnRef1_val}")
##        print("openingchest_off")
        return "autocollecting_off"


def collectingvoidorb_check(window_title):
    #example use
##    window_title = "Mir4G[1]"
    #area 1 active screen
    x_percent = 0.41
    y_percent = 0.655
    width_percent = 0.595
    height_percent = 0.735
    area_file = "ActiveScreenCollectingVoidOrb"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #openingchest ref1
    ref_file = "collectingvoidorb1"
    SSnRef1_val=compare(window_title, area_file, ref_file)
    
    #area 2 inactive screen
    x_percent = 0.44
    y_percent = 0.8
    width_percent = 0.56
    height_percent = 0.84
    area_file = "BlackScreenCollectingVoidOrb"
    cut(window_title,x_percent, y_percent, width_percent, height_percent, area_file)
    #openingchest ref2
    ref_file = "collectingvoidorb2"
    SSnRef2_val=compare(window_title, area_file, ref_file)

    #keep highest value of confidence
    Best_Val = max(SSnRef1_val,SSnRef2_val)

    # Click at the matched region if confidence is above the threshold
    threshold= 0.95
    if Best_Val>= threshold:
##        print(f"match found with confidence {SSnRef1_val}")
##        print("openingchest_on")
        # Transform search area to smaller clickable area, to avoid edge click and missmatch
        """
        smaller_xs = x_percent / 0.98 
        smaller_ys = y_percent / 0.98
        smaller_xe = width_percent * 0.98
        smaller_ye = height_percent * 0.98
        duration = 0.000001
        get_window_click_space_randomizer(smaller_xs,smaller_ys,smaller_xe,smaller_ye,window_title,duration)
        """
        return "collectingvoidorb_on"
    else:
##        print(f"No match found with confidence. Best: {SSnRef1_val}")
##        print("openingchest_off")
        return "collectingvoidorb_off"











