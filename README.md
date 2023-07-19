# img3splat  (insert original name here)
img3splat is a post printer for Splatoon 3 that generates macros for [NXBT](https://github.com/Brikwerk/nxbt), allowing you to print from a Linux machine with a Bluetooth connection rather than a specialized microcontroller. img3splat is heavily inspired by [img2splat](https://github.com/JonathanNye/img2splat), but implements new features to increase reliability.

## How to print
1. Install [JonathanNye's fork of NXBT](https://github.com/JonathanNye/nxbt/tree/experiment/busy-wait) via:

    ```sudo pip install https://github.com/JonathanNye/nxbt/archive/experiment/busy-wait.zip```

    Although img3splat does work with [NXBT's main branch](https://github.com/Brikwerk/nxbt), the fork fixes major timing issues and is highly recommended. If you have errors on NXBT installation, make sure to check the "Troubleshooting" portion of NXBT's README.md.

2. Run NXBT's test function to make sure the virtual controller syncs properly:

     ```sudo nxbt demo```

3. Install img3splat via:

    ```pip install (insert command idk)```

4. Create a 320x120 horizontal image to serve as your plaza post. Images don't necessarily have to be 2-bit grayscale, as they will be automatically converted based on luminance, but dithering *will not* be applied. Processing such images to grayscale beforehand is highly recommended. Any format readable by `Pillow` is supported.

5. Run img3splat:

    ```img3splat [insert arguments here idk]```

    img3splat creates macros for printing on blank canvases (`nrm_macro.txt`) and all-black canvases (`inv_macro.txt`); depending on post contents, one may be significantly faster than the other. img3splat will suggest which macro to use by comparing the file sizes of both.

    Previews of macro prints are generated as `nrm_preview.png` and `inv_preview.png`. Blue pixels represent pixels the cursor passes over but doesn't print, while black/white (depending on macro type) indicates any printed pixels.

7. Open the Splatoon post interface in horizontal mode. If you're using the inverse macro, manually paint the canvas black (touchscreen with largest brush size); otherwise, clear the canvas by pressing on the left joystick. The macro will automatically set the brush to the smallest size and move the cursor to the top left, so size/position doesn't matter. 

8. Undock your Switch, as any change in HDMI input will drop inputs for a short period. If using a longer macro, you may want to remove the USB-C cable from the dock and plug it directly into the Switch.

9. Press the sync button on your controller(s) to enter the "Press L+R on the controller." menu. Then, run the NXBT macro via:

    ```sudo nxbt macro -c "nrm_macro.txt" -r```
    
    or

    ```sudo nxbt macro -c "inv_macro.txt" -r```

    The macro will automatically press - to save the image on completion.
    
10. If you run into any errors with your print, or if you want to make tweaks to the image after the fact, you can run img3splat in *repair mode*, which automatically detects wrong pixels from an in-game screenshot. Running a print macro will automatically save a screenshot to the Switch's album to use with repair mode.

    If you're transferring the screenshot via the Switch's "Send to Smartphone" feature, make sure to **save the image to your phone** rather than copying it to your phone's clipboard. Copying the image to clipboard introduces significant jpg compression, interfering with image recognition (at least on iOS).

    ```img3splat [repair mode command]```

    The "screenshot" input accepts either a 1280x720 (Switch screenshot size) or a 320x120 image (original printed post). The second option is useful for making tweaks to a properly printed post.

    Repair mode generates the repair macro `rpr_macro.txt` and the `rpr_preview.png` macro preview. In the repair mode preview, A/B inputs are represented with lighter and darker shades of red rather than black and white.

    Do note that due to cursor interference, repair mode *will not* repair the top left 2x2 pixels of the post.

11. With the post open, press the sync button on your controller(s) to enter the "Press L+R on the controller." menu. Then, run the repair macro via:

    ```sudo nxbt macro -c "rpr_macro.txt" -r```

    The repair macro will also take a screenshot and press - to save after printing.

## Why img3splat?
img3splat is designed for higher reliability when printing complex posts, minimizing the need for manual touchups.

- If using fast mode (default), img3splat scans the contents of each column to minimize the amount of inputs used when printing. To reduce the effects of dropped inputs, if the last pixel in a column is located at the top or bottom of the canvas, it also sends extra up/down inputs to ensure the cursor is at the proper location.
- If using cautious mode, printing in full columns rather than full rows reduces the area of effect of dropped inputs. Cautious mode still skips empty columns, reduced print times somewhat on unstable connections. (**maybe rephrase this?**)
- img3splat supports taking a screenshot of the Splatoon post interface to check for errors, generating a repair macro that fixes any incorrect pixels. This also allows for tweaks to the original image without restarting the whole printing process.

## Print demo (what to expect)
original image

generated macro and inverse previews, blue indicates cursor travel, black (for macro) or white (for inverse) indicates printed pixels

first pass result

repair macro preview

second pass result

## Arguments/outputs
### Arguments
- image: required, the post you want to print; 320x120 horizontal image (doesn't need to be black and white (auto-converted based on luminance), supports any format supported by `Pillow`)
- repair image: optional, 1280x720 screenshot of the post interface (make sure cursor is smallest and set to top left, ignores top left 2x2 pixels); also accepts a 320x120 image for tweaking purposes
- delay: amount of time between inputs in seconds (0.1 by default), can decrease the value at the risk of higher dropped inputs
- verbose: outputs print mode, when the program generates a macro file or macro preview file
- show instructions: outputs printing instructions after generating a macro (including sudo nxbt)

### Outputs
- `nrm_macro.txt` and `inv_macro.txt`: macro files generated when running the program normally; `nrm_macro.txt` is for a blank canvas, `inv_macro.txt` is for an all-black canvas
- `rpr_macro.txt`: macro file generated when running in repair mode, assumes in-game post is same as screenshot
- `nrm_preview.png`, `inv_preview.png`, and `rpr_preview.png`: preview of cursor movement during macro execution; for nrm, white = untouched by cursor, blue = passed over by cursor, black = ink; for inv, black = untouched by cursor, blue = passed over by cursor, white = erase; for repair, gray = untouched by cursor, blue = passed over by cursor, black = ink, white = erase

## Dependencies
img3splat uses `NumPy` and `Pillow`, both of which should be automatically installed on img3splat installation.

To run the generated macros, you also need [JonathanNye's NXBT fork](https://github.com/JonathanNye/nxbt/tree/experiment/busy-wait) (highly recommended to fix timing issues) or standard [NXBT](https://github.com/Brikwerk/nxbt).

## Issues
this shit is mostly just for personal use I'm only planning on implementing what i need
