#TODO:
# -set up command line switches
# -set up paths properly
# -path/git/pip integration
# -separate script for comparing screenshot to file (get 320x120 image from screenshot, then numpy mask?)
# -row mode? it's just changing some values but
#-----------------------------

#import libraries
import sys #this is for quitting the program
from PIL import Image
import numpy as np

import printpost
import macropreview

#future CLI argument stuff
img_input = 'nkos.png'
clm_input = ''
clm_min = 0
clm_max = 319
delay_input = ''
delay = 0.1
startinplace = False #this is to put the cursor in place at (an) empty column(s)and it'll just print the column(s)
skipemptylines = True
show_instructions = True #verbose flag
repair = False #repair mode for eventual screenshot to file comparison

#-----------------------------

#validate inputs

#parse column input
try:
    if clm_input != '':
        try: #if column input is one value
            clm_min = int(clm_input)
            clm_max = clm_min
        except: #if column input is two values
            clm_list = clm_input.split("-", 1)
            print(clm_list[0], clm_list[1])
            clm_min = int(clm_list[0])
            clm_max = int(clm_list[1])
except:
    print('Error: Invalid column input!')
    print('Make sure values are 0-319, either [single column] or [starting column]-[ending column].') 
    sys.exit()
if clm_min > clm_max or clm_min < 0 or clm_max > 319: #make sure values are in bounds
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

#open image, convert to bilevel, test integrity (exit if invalid)
try:
    spimg = Image.open(img_input).convert('1')
except:
    print("Error: Invalid file! Image isn't recognized or doesn't exist.")
    sys.exit()

#check image size (exit if wrong size)
if spimg.size != (320,120):
    print('Error: Image is not 320x120!')
    sys.exit()


#-----------------------------

#convert image to np array
spimg_np = np.array(spimg)
#rotate img 90 deg to process rows as columns
spimg_np = np.rot90(spimg_np, 3)

#call the print function somewhere around here i think, both normal and inverse
nrm_macro_name = 'splat_macro.txt'
inv_macro_name = 'inv_macro.txt'

nrm_macro = open(nrm_macro_name, 'w')
printpost.printpost(spimg_np, nrm_macro, False, clm_min, clm_max, delay, startinplace, skipemptylines, repair)
if show_instructions:
    print('Generated macro!')

inv_macro = open(inv_macro_name, 'w')
printpost.printpost(spimg_np, inv_macro, True, clm_min, clm_max, delay, startinplace, skipemptylines, repair)
if show_instructions:
    print('Generated inverse macro!')

#------------------------------

#run preview script
macropreview.preview(nrm_macro_name, 'macro_preview.png')
if show_instructions:
    print('Generated macro preview!')

macropreview.preview(inv_macro_name, 'inv_preview.png')
if show_instructions:
    print('Generated inverse macro preview!')

#closing message
if show_instructions:
    print('''To print, open a blank plaza post (or all black if inverse), set brush to smallest, and set the
cursor to the top left corner of the post (or at the top of the column if "print in place" is enabled).
Then, hit the "sync" button on your controller to disconnect it.
Make sure your Switch is in handheld mode to prevent desyncs.
Run "sudo nxbt macro -c "splat_macro.txt" -r" or "sudo nxbt macro -c "inv_macro.txt" -r" to start the print.
Woomy! くコ:彡''')