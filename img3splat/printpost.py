import numpy as np

def printpost(array, inputfname, inverse, prtmin, prtmax, delay, inplace, skiplines, repair):
    #open input file
    inputfile = open(inputfname, 'w')
    #initialize vars
    crsr_is_top = True    #T = cursor is moving from top to bottom, F = cursor is moving from bottom to top
    delaystr = str(delay) + 's'
    adjprtmax = prtmax - prtmin    #used when comparing array index to terminate print
    arypos = 0    #current array y pos, this needs to be tracked manually (since extracting line by line)
    dirstr = '\nDPAD_DOWN ' + delaystr + '\n' + delaystr    #direction string, either "DPAD_DOWN [delay]s" or "DPAD_UP [delay]s" + delay
    inptrpt = 3    #input repeat, number of extra inputs to send at the end of a line
    lineskip = False    #whether the current line has been skipped

    #set up initial delay and A press on connect screen
    inputfile.write('3.0s')
    inputfile.write('\nA ' + delaystr)
    inputfile.write('\n5.0s')

    #move to top left, switch to smallest brush
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL ' + delaystr + '\n' + delaystr)
    inputfile.write('\nL_STICK@-100+100 5s' + '\n' + delaystr)


    #remove skipped columns, go to min column (if print in place is disabled)
    for i in range(prtmin):
        if inplace == False:
            inputfile.write('\nDPAD_RIGHT ' + delaystr + '\n' + delaystr)
        array = np.delete(array, 0, 0)

    #process the image array
    for crtrow in array: #this iterates for every row in the 2d array
        #skip empty lines (all white or all black w/ inverse)
        if skiplines: 
            lineskip = False    #reset on new line; lineskip is a bit confusing but eh
            if repair:
                if np.all(crtrow == 2):    #check if 2 (skip)
                    lineskip = True
            elif inverse:
                if np.any(crtrow) == False:    #check if any white pixels exist
                    lineskip = True
            else:
                if np.all(crtrow):    #check if all white pixels
                    lineskip = True
            if lineskip:
                inputfile.write('\nDPAD_RIGHT ' + delaystr + '\n' + delaystr)    #skip, move to next column
        #print the column
        if lineskip == False:    #skip extra processing if skipping line
            if crsr_is_top:    #if moving top to bottom, need to flip the row
                procrow = crtrow[::-1]    #flip current row, save as processed row
            else:
                procrow = crtrow    #if flipping isn't needed, make intact row the processed row
            for x in procrow:    #iterate over the row
                if repair:
                    if x == 0:
                        inputfile.write('\nB ' + delaystr + '\n' + delaystr)
                    elif x == 1:
                        inputfile.write('\nA ' + delaystr + '\n' + delaystr)
                elif inverse:    #if inverse, erase when True (white)
                    if x:
                        inputfile.write('\nB ' + delaystr + '\n' + delaystr)
                else:    #normal mode, ink when False (black)
                    if x == False:
                        inputfile.write('\nA ' + delaystr + '\n' + delaystr)
                inputfile.write(dirstr)
        #runs at the end of the line
        if arypos == adjprtmax:   #terminate printing if at last pixel of max line; for obsolete column input
            break
        elif lineskip == False:    #at end of current row, but not final row
            for i in range(inptrpt):    #send extra directional inputs to make sure cursor is at the edge
                inputfile.write(dirstr)
            inputfile.write('\nDPAD_RIGHT ' + delaystr + '\n' + delaystr)    #move to next column
            arypos += 1
            if crsr_is_top:    #reverse input direction
                crsr_is_top = False
                dirstr = '\nDPAD_UP ' + delaystr + '\n' + delaystr
            else:
                crsr_is_top = True
                dirstr = '\nDPAD_DOWN ' + delaystr + '\n' + delaystr

    #move cursor to top, capture
    inputfile.write('\nL_STICK@-100+100 5s' + '\n' + delaystr)
    inputfile.write('\nCAPTURE' + delaystr + '\n' + delaystr)

    #save image and close file
    inputfile.write('\nMINUS ' + delaystr + '\n' + delaystr + '\n5.0s')
    inputfile.close()
    return