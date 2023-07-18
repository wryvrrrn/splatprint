from PIL import Image
import numpy as np

#vars


#funcs

def procrepair(image):    #takes in 320x120 or screenshot, outputs 320x120 rotated np array
    # detect image size; if 320x120, convert to threshold, convert to np array, rotate 90 degrees
    # for screenshot, get top 319x120 from image, scale down to 319x120, threshold (maybe threshold before? idk)
    # for bottom row, threshold then squish to 1x120? need different settings though
    # then, append to bottom of 319x120 np array, and rotate
    # if that doesn't work gotta go with more complex options
    return


def genrepairarray(main_ar, rpr_ar):    #generates repair array (proc_ar)
    # use numpy masks? int array from 0-2, 0 is black (would be False), 1 is white (would be True), 2 is skip
	# then make top left 2x2 (or top right once rotated i guess) pixels Skip (cursor blocks it)
    return proc_ar