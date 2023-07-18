from PIL import Image
import numpy as np

#vars


#funcs

#debug
def rotimgarray(image):
    image = image.convert('1')
    imgar = np.array(image)
    imgar = np.rot90(image, 3)
    return imgar


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
        image = image.convert('1')
        imgar = np.array(image)
    imgar = np.rot90(imgar, 3)    #rotate 90 degrees
    return imgar


def genrepairarray(main_ar, rpr_ar):    #generates repair array (proc_ar)
    # use numpy masks? int array from 0-2, 0 is black (would be False), 1 is white (would be True), 2 is skip
	# then make top left 2x2 (or top right once rotated i guess) pixels Skip (cursor blocks it)

    #create empty processed array (full of skip (2))
    proc_ar = np.full((320, 120), 2, dtype=int)

    #swap top left 2x2 of repair image
    rpr_ar[0][119] = main_ar[0][119]
    rpr_ar[0][118] = main_ar[0][118]
    rpr_ar[1][119] = main_ar[1][119]
    rpr_ar[1][118] = main_ar[1][118]

    # check for differences; True == difference
    mask_ar = np.not_equal(main_ar, rpr_ar)    #mask as like, layer mask not masked np arrays

    #go through mask, if there's a difference, grab value from main array and put in proc array
    for index, x in np.ndenumerate(mask_ar):
        if x:
            if main_ar[index]:
                proc_ar[index] = 1
            else:
                proc_ar[index] = 0

    return proc_ar


# #debug
# img = Image.open('nkos.png')
# rprimg = Image.open('screenshot.jpg')
# main_ar = rotimgarray(img)
# rpr_ar = procrepair(rprimg)
# proc_ar = genrepairarray(main_ar, rpr_ar)
# Image.fromarray(proc_ar).save('proc_img.png')
