from PIL import Image
import numpy as np

#vars


#funcs

def procrepair(image):    #takes in 320x120 or screenshot, outputs 320x120 rotated np array
    if image.size == (1280,720):
        img119 = image.crop((160,188,1120,545))    #crop top 320x119 image from screenshot
        img1 = image.crop((160,545,1120,546))      #crop bottom row of pixels
        img119 = img119.convert('1')    #convert 320x119 to 2-bit greyscale
        img1 = img1.point(lambda i: i > 127 and 255).convert('1')    #same but for bottom row (I have no clue how this works tbh)
        img119 = img119.resize((320,119))    #scale down 3x
        img1 = img1.resize((320,1))    #scale down 3x horizontally only
        imgar = np.concatenate((np.array(img119), np.array(img1)), axis=0)    #concat 119+1 to get 320x120
    else:    #for non-screenshot
        imgar = np.array(image)
    imgar = np.rot90(imgar, 3)    #rotate 90 degrees
    return imgar


def genrepairarray(main_ar, rpr_ar):    #generates repair array (proc_ar)
    # use numpy masks? int array from 0-2, 0 is black (would be False), 1 is white (would be True), 2 is skip
	# then make top left 2x2 (or top right once rotated i guess) pixels Skip (cursor blocks it)
    return proc_ar

rprimg = Image.open('screenshot.jpg')
output_image = Image.fromarray(procrepair(rprimg))
output_image.save('120.png')