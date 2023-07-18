import numpy as np

def printpost(array, inputfile, inverse, prtmin, prtmax, delay, inplace, skiplines, repair):
    #initialize vars
    crsr_is_top = True #T = cursor is moving from top to bottom, F = cursor is moving from bottom to top
    delaystr = str(delay) + 's'
    adjprtmax = prtmax - prtmin #used when comparing array index to terminate print
    arypos = 0 #current array y pos, this needs to be tracked manually (since extracting line by line)
    dirstr = '\nDPAD_DOWN ' + delaystr + '\n' + delaystr #direction string, either "DPAD_DOWN [delay]s" or "DPAD_UP [delay]s" + delay
    inptrpt = 3 #input repeat, number of extra inputs to send at the end of a line
    lineskip = False #whether the current line has been skipped

    #set up initial delay and A press on connect screen
    inputfile.write('3.0s')
    inputfile.write('\nA ' + delaystr)
    inputfile.write('\n5.0s')

    #remove skipped columns, go to min column (if print in place is disabled)
    for i in range(prtmin):
        if inplace == False:
            inputfile.write('\nDPAD_RIGHT ' + delaystr + '\n' + delaystr)
        array = np.delete(array, 0, 0)

    for crtrow in array: #this iterates for every row in the 2d array

        if skiplines: #skip empty lines (all white or all black w/ inverse)
            lineskip = False #reset on new line
            if inverse:
                if np.any(crtrow) == False: #check if any white pixels exist
                    lineskip = True
            else:
                if np.all(crtrow): #check if all white pixels
                    lineskip = True
            if lineskip:
                inputfile.write('\nDPAD_RIGHT ' + delaystr + '\n' + delaystr) #move to next column

        if lineskip == False: #skip extra processing if skipping line
            if crsr_is_top: #if moving top to bottom, need to flip the row
                procrow = crtrow[::-1] #flip current row, set as processed row variable
            else:
                procrow = crtrow #if flipping isn't needed, set current row to processed row variable
            for x in procrow: #iterate the row
                if inverse: #if inverse, erase when True (white)
                    if x:
                        if repair:
                            inputfile.write('\nA ' + delaystr + '\n' + delaystr)
                        inputfile.write('\nB ' + delaystr + '\n' + delaystr)
                else: #ink when False (black)
                    if x == False:
                        if repair:
                            inputfile.write('\nB ' + delaystr + '\n' + delaystr)
                        inputfile.write('\nA ' + delaystr + '\n' + delaystr)
                inputfile.write(dirstr)


        #once at the end of the line
        if arypos == adjprtmax: #terminate loop if at last pixel of max line
            break
        elif lineskip == False: #if at end of current row, but it isn't the final row
            for i in range(inptrpt): #send extra directional inputs to make sure cursor is at the edge
                inputfile.write(dirstr)
            inputfile.write('\nDPAD_RIGHT ' + delaystr + '\n' + delaystr) #move to next column
            arypos += 1
            if crsr_is_top: #reverse input direction
                crsr_is_top = False
                dirstr = '\nDPAD_UP ' + delaystr + '\n' + delaystr
            else:
                crsr_is_top = True
                dirstr = '\nDPAD_DOWN ' + delaystr + '\n' + delaystr


    #save image and close file
    inputfile.write('\nMINUS ' + delaystr + '\n' + delaystr + '\n5.0s')
    inputfile.close()
    return