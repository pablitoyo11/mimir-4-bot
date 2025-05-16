from ReturnCompareSSnRef import cut_and_compare
#def cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
from ClickAtMir import get_window_click_space_randomizer

def openingchest_check():
    #example use
    window_title = "Mir4G[1]"
    output_file = "openingchest"

    #openingchest ref1
    x_percent = 0.41
    y_percent = 0.655
    width_percent = 0.595
    height_percent = 0.735
    output_file = "openingchest1"
    SSnRef1_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)
    
    #openingchest ref2
    x_percent = 0.44
    y_percent = 0.8
    width_percent = 0.56
    height_percent = 0.84
    output_file = "openingchest2"
    SSnRef2_val=cut_and_compare(window_title,x_percent, y_percent, width_percent, height_percent, output_file)

    #keep highest value of confidence
    Best_Val = max(SSnRef1_val,SSnRef2_val)

    # Click at the matched region if confidence is above the threshold
    threshold= 0.95
    if Best_Val>= threshold:
        print(f"match found with confidence {SSnRef1_val}")
        print("openingchest_on")
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
        print(f"No match found with confidence. Best: {SSnRef1_val}")
        print("openingchest_off")
        return "openingchest_off"







