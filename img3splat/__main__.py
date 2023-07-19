#import libraries
from cmath import nan
import sys    #for quitting the program
import os     #for checking macro size
from PIL import Image
import numpy as np

import printpost
import macropreview
import repairpost

#future CLI argument stuff
img_input = 'test/bmcm.png'
rpr_input = 'test/screenshot.jpg'
delay_input = '0.05'
delay = 0.1
verbose_en = True         #print lines after macro generation/preview generation (doesn't affect error output)
show_instructions = False    #show print instructions on completion (maybe via very verbose flag?)
repair = False    #repair mode for screenshot to file comparison
cautious = False    #cautious mode, always prints whole columns

#output vars
nrm_macro_name = 'nrm_macro.txt'
inv_macro_name = 'inv_macro.txt'
rpr_macro_name = 'rpr_macro.txt'
nrm_preview_name = 'nrm_preview.png'
inv_preview_name = 'inv_preview.png'
rpr_preview_name = 'rpr_preview.png'

#-----------------------------
#validate delay input
try:
    if delay_input != '':
        delay = float(delay_input)
except:
    print('Error: Invalid delay input! Not a number.')
    sys.exit()
if delay <= 0:
    print('Error: Invalid delay input! Must be greater than 0.')
    sys.exit()
elif delay >= 0.5:
    print('Delay value is large, print might take a while.')

#open main image, convert to bilevel, test integrity (exit if invalid)
try:
    mainimg = Image.open(img_input).convert('1')
except:
    print("Error: Invalid file! Image isn't recognized or doesn't exist.")
    sys.exit()
if mainimg.size != (320,120):    #check image size (exit if wrong size)
    print('Error: Image is not 320x120!')
    sys.exit()

#open repair image, check size
if repair:
    try:
        rprimg = Image.open(rpr_input)
    except:
        print("Error: Invalid repair file! Image isn't recognized or doesn't exist.")
        sys.exit()
    if ( (rprimg.size == (1280,720)) or (rprimg.size == (320,120)) ) == False:
        print('Error: Repair image is not 1280x720 or 320x120!')
        sys.exit()

#-----------------------------

# generate 320x120 rotated image from repair image
if repair:
    rpr_out = repairpost.procrepair(rprimg)    #returns (rotated array, processed screenshot image)
    rprimg_ar = rpr_out[0]
    scrimg = rpr_out[1]

#-----------------------------

#convert main image to np array, rotate 90 deg to process as columns
mainimg_ar = np.array(mainimg)
mainimg_ar = np.rot90(mainimg_ar, 3)

#generate repair array, generate macro 
if repair:
    proc_ar = repairpost.genrepairarray(mainimg_ar, rprimg_ar)    #creates printable array with repair instructions
    # check if proc_ar is all skip, if so, terminate program
    if np.all(proc_ar == 0):
        print('Error: No pixels to repair!')
        sys.exit()

#-----------------------------

if verbose_en:
    if cautious:
        print('Printing in cautious mode!')
    else:
        print('Printing in fast mode!')

#generate repair macro
if repair:
    printpost.printpost(proc_ar, rpr_macro_name, False, delay, True, cautious)
    if verbose_en:
        print('Generated repair macro!')

#generate normal/inverse macros
else:
    printpost.printpost(mainimg_ar, nrm_macro_name, False, delay, False, cautious)
    if verbose_en:
        print('Generated macro!')
    printpost.printpost(mainimg_ar, inv_macro_name, True, delay, False, cautious)
    if verbose_en:
        print('Generated inverse macro!')

#------------------------------

#run preview script
if repair:
    macropreview.preview(rpr_macro_name, rpr_preview_name, False, True, scrimg)
    if verbose_en:
        print('Generated repair macro preview!')
else:
    macropreview.preview(nrm_macro_name, nrm_preview_name, False, False, None)
    if verbose_en:
        print('Generated macro preview!')
    macropreview.preview(inv_macro_name, inv_preview_name, True, False, None)
    if verbose_en:
        print('Generated inverse macro preview!')

#get smaller macro size
if repair == False:
    nrm_size = os.path.getsize(nrm_macro_name)
    inv_size = os.path.getsize(inv_macro_name)
    if nrm_size < inv_size:
        print('Normal macro likely has shorter print time.')
        print('(' + str(nrm_size) + 'b vs. ' + str(inv_size) + 'b)')
    elif nrm_size > inv_size:
        print('Inverse macro likely has shorter print time.')
        print('(' + str(inv_size) + 'b vs. ' + str(nrm_size) + 'b)')
    else:
        print('Both macros have the exact same size (somehow).')

#print instructions
if show_instructions:
    print('''To print, open a blank plaza post (or all black if inverse),
then press the "sync" button on your controller to disconnect it.
Make sure your Switch is in handheld mode to prevent desyncs.''')
    if repair:
        print('''Then, run this command to start the print:
    sudo nxbt macro -c "rpr_macro.txt" -r''')
    else:
        print('''Then, run one of these commands to start the print:
    sudo nxbt macro -c "nrm_macro.txt" -r
    sudo nxbt macro -c "inv_macro.txt" -r''')
    print('Woomy! くコ:彡')