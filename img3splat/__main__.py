#import libraries
import sys    #for quitting the program
from PIL import Image
import numpy as np

import printpost
import macropreview

#future CLI argument stuff
img_input = 'nkos.png'
rpr_input = 'screenshot.jpg'
clm_input = ''
clm_min = 0
clm_max = 319
delay_input = ''
delay = 0.1
startinplace = False    #this is to put the cursor in place at (an) empty column(s)and it'll just print the column(s)
skipemptylines = True
verbose_en = True         #print lines after macro generation/preview generation (doesn't affect error output)
show_instructions = False    #show print instructions on completion (maybe via very verbose flag?)
repair = False    #repair mode for screenshot to file comparison

#output vars
nrm_macro_name = 'nrm_macro.txt'
inv_macro_name = 'inv_macro.txt'
rpr_macro_name = 'rpr_macro.txt'
nrm_preview_name = 'nrm_preview.png'
inv_preview_name = 'inv_preview.png'
rpr_preview_name = 'rpr_preview.png'

#-----------------------------
#validate inputs

#parse column input
try:
    if clm_input != '':
        try:    #if column input is one value
            clm_min = int(clm_input)
            clm_max = clm_min
        except:     #if column input is two values
            clm_list = clm_input.split("-", 1)
            print(clm_list[0], clm_list[1])
            clm_min = int(clm_list[0])
            clm_max = int(clm_list[1])
except:
    print('Error: Invalid column input!')
    print('Make sure values are 0-319, either [single column] or [starting column]-[ending column].') 
    sys.exit()
if clm_min > clm_max or clm_min < 0 or clm_max > 319:    #make sure values are in bounds
    print('Error: Invalid column input!')
    print('Make sure values are 0-319, either "[single column]" or "[starting column]-[ending column]".') 
    sys.exit()
if clm_input == '' and startinplace == True:
    print('Error: "Start in place" must specify min/max column values.')
    sys.exit()

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

#generate 320x120 rotated image from repair image #(WIP, commented out for now)
# if repair:
#     rprimg_ar = repairpost.procrepair(rprimg) #this returns a rotated array

#-----------------------------

#convert main image to np array, rotate 90 deg to process as columns
mainimg_ar = np.array(mainimg)
mainimg_ar = np.rot90(mainimg_ar, 3)

#generate repair array, generate macro 
if repair:
    print("sorry this isn't finished yet") #(WIP)
    # proc_ar = repairpost.genrepairarray(mainimg_ar, rprimg_ar)    #creates printable array with repair instructions
    # check if proc_ar is all skip, if so, terminate program

#-----------------------------

#generate repair macro
if repair:
    print("sorry this isn't finished yet") #(WIP)
#     printpost.printpost(proc_ar, rpr_macro_name, False, clm_min, clm_max, delay, startinplace, skipemptylines, True)

#generate normal/inverse macros
else:
    printpost.printpost(mainimg_ar, nrm_macro_name, False, clm_min, clm_max, delay, startinplace, skipemptylines, False)
    if verbose_en:
        print('Generated macro!')
    printpost.printpost(mainimg_ar, inv_macro_name, True, clm_min, clm_max, delay, startinplace, skipemptylines, False)
    if verbose_en:
        print('Generated inverse macro!')

#------------------------------

#run preview script
if repair:
    macropreview.preview(rpr_macro_name, rpr_preview_name, False, True)
    if verbose_en:
        print('Generated repair macro preview!')
else:
    macropreview.preview(nrm_macro_name, nrm_preview_name, False, False)
    if verbose_en:
        print('Generated macro preview!')
    macropreview.preview(inv_macro_name, nrm_preview_name, False, False)
    if verbose_en:
        print('Generated inverse macro preview!')

#closing message
if show_instructions:
    print('''To print, open a blank plaza post (or all black if inverse), set brush to smallest, and set the
cursor to the top left corner of the post (or at the top of the column if "print in place" is enabled).
Then, hit the "sync" button on your controller to disconnect it.
Make sure your Switch is in handheld mode to prevent desyncs.
Run "sudo nxbt macro -c "splat_macro.txt" -r" or "sudo nxbt macro -c "inv_macro.txt" -r" to start the print.
Woomy! くコ:彡''')