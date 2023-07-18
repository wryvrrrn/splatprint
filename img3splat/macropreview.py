from PIL import Image
import numpy as np

#set up vars
def preview(macroname, output):
    macro = open(macroname, 'r')
    curx = 0 #cursor x value
    cury = 0 #cursor y value
    img = Image.new(mode="RGB", size=(320, 120), color=(255,255,255))
    img_array = np.array(img)

    #iterate across image
    with open(macroname, 'r') as f:
        for x in range(3):
            next(f)
        for l_no, line in enumerate(f):
            if line.startswith("B") or line.startswith("A"):
                img_array[cury][curx] = (0,0,0)
            if 'LEFT' or 'RIGHT' or 'UP' or 'DOWN' in line:
                if np.all(img_array[cury][curx]) != 0:
                    img_array[cury][curx] = (200,200,255)
            if 'LEFT' in line:
                curx = max(curx - 1, 0)
            if 'RIGHT' in line:
                curx = min(curx + 1, 319)
            if 'UP' in line:
                cury = max(cury - 1, 0)
            if 'DOWN' in line:
                cury = min(cury + 1, 119)
            if 'MINUS' in line:
                break

    #cleanup + output
    macro.close()
    output_image = Image.fromarray(img_array)
    output_image.save(output)