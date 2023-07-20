# img3splat  (insert original name here)
img3splat is a post printer for Splatoon 3 that generates macros for [NXBT](https://github.com/Brikwerk/nxbt), allowing you to print from a Linux machine with a Bluetooth connection rather than a specialized microcontroller. img3splat is heavily inspired by [img2splat](https://github.com/JonathanNye/img2splat), but fixes syncing issues and implements new features to increase reliability.
## How to print
1. Install [JonathanNye's fork of NXBT](https://github.com/JonathanNye/nxbt/tree/experiment/busy-wait) via:

        sudo pip install https://github.com/JonathanNye/nxbt/archive/experiment/busy-wait.zip

    Although img3splat does work with [NXBT's main branch](https://github.com/Brikwerk/nxbt), the fork is very highly recommended as it fixes major timing issues. If you have errors on NXBT installation, make sure to check the "Troubleshooting" portion of NXBT's README.md.

2. Run NXBT's test function to make sure the virtual controller connects and syncs properly:

        sudo nxbt demo

3. Install img3splat via:

        pip install (insert command idk)

4. Create a 320x120 horizontal image to serve as your plaza post. Images don't necessarily have to be 2-bit grayscale, as they will be automatically converted based on luminance, but dithering *will not* be applied. Processing such images to grayscale beforehand is highly recommended. Any format readable by `Pillow` is supported.

5. Run img3splat:

        img3splat -i "image.png"

    Additional flags are listed under "Usage" below.

    img3splat creates macros for printing on blank canvases (`nrm_macro.txt`) and all-black canvases (`inv_macro.txt`). Depending on post contents, one may be significantly faster than the other; img3splat will suggest which macro to use by comparing the file sizes of both.

    Previews of macro prints are generated as `nrm_preview.png` and `inv_preview.png`. Blue pixels represent pixels the cursor passes over but doesn't print, while black/white (depending on macro type) indicates any printed pixels.

6. Open the Splatoon post interface in horizontal mode. If you're using the inverse macro, manually paint the canvas black (touchscreen with largest brush size); otherwise, clear the canvas by pressing on the left joystick. The macro will automatically set the brush to the smallest size and move the cursor to the top left, so size/position doesn't matter. 

7. Undock your Switch, as any change in HDMI input will drop inputs for a short period. If using a longer macro, you may want to remove the USB-C cable from the dock and plug it directly into the Switch.

8. Press the sync button on your controller(s) and wait until the screen shows the "Press L+R on the controller." menu. Then, run the NXBT macro via:

        sudo nxbt macro -c "nrm_macro.txt" -r
    
    or

        sudo nxbt macro -c "inv_macro.txt" -r

    The macro will automatically press - to save the image on completion.
    
9. If you run into any errors with your print, or if you want to make tweaks to the image after the fact, you can run img3splat in *repair mode*, which automatically detects wrong pixels from an in-game screenshot. Running a print macro will automatically save a screenshot to the Switch's album to use with repair mode.

    If you're transferring the screenshot via the Switch's "Send to Smartphone" feature, make sure to **save the image to your phone** rather than copying it to your phone's clipboard. Copying the image to clipboard introduces significant JPG compression, interfering with image recognition (at least on iOS).

        img3splat -i "image.png" -r "screenshot.jpg"

    The "screenshot" input accepts either a 1280x720 (Switch screenshot size) or a 320x120 image (original printed post). The second option is useful for making tweaks to a properly printed post.

    Repair mode generates the repair macro `rpr_macro.txt` and the `rpr_preview.png` macro preview. In the repair mode preview, A/B inputs are represented with lighter and darker shades of red rather than black and white.

    Do note that due to cursor interference, repair mode *will not* repair the top left 2x2 pixels of the post.

10. Like before, disconnect your controllers with the post open. Then, run the repair macro via:

        sudo nxbt macro -c "rpr_macro.txt" -r

    The repair macro will also take a screenshot and press - to save after printing.

## Why img3splat?
img3splat is designed for higher reliability when printing complex posts, minimizing the need for manual touchups.

- In fast mode (default), img3splat scans the contents of each column to minimize the amount of inputs used when printing. To reduce the effects of dropped inputs, if the last pixel in a column is located at the top or bottom of the canvas, it also sends extra up/down inputs to ensure the cursor is at the proper location.
- img3splat can also print in cautious mode, which prints in full columns to minimize the effects of dropped inputs. Printing in columns (rather than rows) allows the cursor to be aligned more frequently, reducing the area of effect of dropped inputs. 
- In case of errors, img3splat supports taking a screenshot of the Splatoon post interface to generate a repair macro that fixes any incorrect pixels. This feature can also be used to tweak the original image without printing the image from scratch.
    
- img3splat can also save the post contents of a screenshot to a 320x120 image, allowing you to rough out a post on the touchscreen and polish it in an image editor (useful if you don't have a drawing tablet).

## Demonstration
original image

generated macro and inverse previews, blue indicates cursor travel, black (for macro) or white (for inverse) indicates printed pixels

first pass result

repair macro preview

second pass result

## Usage
### Arguments

You can view the help message by running `img3splat` without any arguments.

Standard usage of img3splat is as follows:

    `img3splat -i "input.png"`

- `-i "input.png"`: Input image, with `"input.png"` being a 320x120 image of the post you want to print. img3splat will convert the image to black and white automatically (based on luminance), but will not apply dithering for any RGB/grayscale images. This can be in any format supported by `Pillow`, but a lossless format (like `.png`) is recommended.

- `-d [#]` (optional): Delay, in seconds. Indicates the amount of time a button is pressed, as well as the amount of time the macro waits before inputting another button press. If not specified, will use the default value of 0.1.

    Lowering this value will increase the speed of macro execution at the risk of more dropped inputs. If you're printing longer macros and have a stable connection, it may be useful to start with a smaller delay to print the bulk of the post and do a second pass in repair mode with the default value (this hasn't been tested, though).

- `-c` (optional): Cautious. If enabled, img3splat will pass the cursor through the entire column of any columns that contain printable pixels rather than moving to the next column after reaching the last printable pixel. This reduces the effects of any dropped inputs, as img3splat sends extra inputs at the end of a column to ensure the cursor is aligned with the top/bottom of the image, but usually significantly increases print time. However, enabling this does significantly reduce macro generation time.

- `-v` (optional): Verbose. If enabled, img3splat will print messages when the program generates a macro file or macro preview file. img3splat will still recommend a macro to use with this flag disabled.

- `-p` (optional): Print instructions. If enabled, img3splat will print instructions on how to print the generated macros, including post setup and the commands for running the macro file with NXBT.

Repair mode usage is as follows:

    `img3splat -i "input.png" -r "screenshot.jpg"`

- `-i "input.png"`: Input image, with `"input.png"` being the 320x120 image that img3splat will correct the post to. Usually the original image used to generate macro in normal operation, but you can also use a revised version of the original to make tweaks to the post. Supported formats and color space are identical to standard operation.

- `-r "screenshot.jpg"`: Runs img3splat in repair mode. This generates a macro file that targets any pixels that were inputted incorrectly in-game. `screenshot.jpg` is the image of the in-game post that needs to be corrected. Must either be a 1280x720 screenshot of the post interface, taken with the Switch's capture button, or a 320x120 image of the post. The images saved to the Switch's album after publishing a post are not supported.

    Screenshots should be taken with the canvas set horizontally, the brush size set to smallest, and the cursor placed in the top left. However, manual screenshots usually aren't needed; macros generated by img3splat will automatically save an appropriate screenshot at the end of execution. See "How to print" above for some details on how to best transfer the screenshot to your computer while minimizing compression.

- `-c`, `-v`, and `-p` (optional): Function identically to standard operation.

    If the initial macro suffered from several dropped inputs due to an unstable connection, cautious mode (`-c`) is recommended.

Save mode usage is as follows:

    `img3splat -s "screenshot.jpg"`

- `-s "screenshot.jpg"`: Save screenshot, with `"screenshot.jpg"` being a 1280x720 screenshot of the post interface, taken with the Switch's capture button. Saves the detected 320x120 post from the 1280x720 screenshot of the post interface as `proc_screenshot.png`. Useful if you want to edit a post made in-game on the computer.

    Unfortunately, pixels around the in-game cursor will not be detected properly. To minimize the cursor's interference with detection operations, it's recommended to set the cursor to the smallest brush size and place it in the corner of the canvas. Improper usage of the Switch's "Sent to Smartphone" feature may also introduce extra JPG compression that interferes with detection; see "How to print" above for details.

- `-v` (optional): Functions identically to standard operation.

Save mode cannot be used in conjunction with the macro generation modes.

### Outputs
- `nrm_macro.txt` and `inv_macro.txt`: Macro files generated when running the program normally. `nrm_macro.txt` is intended for printing on a blank canvas, and `inv_macro.txt` is intended for an all-black canvas.
- `rpr_macro.txt`: Macro file generated when running in repair mode.
- `nrm_preview.png`, `inv_preview.png`, and `rpr_preview.png`: Previews of macro execution. Blue pixels represent pixels the cursor will pass over but not print. For `nrm_preview.png`, pixels to be printed are marked in black, while untouched pixels are marked in white; for `inv_preview.png`, pixels are marked the opposite color. For `rpr_preview.png`, untouched pixels are marked by their color in the original post while printed pixels are marked in lighter and darker shades of red.

## Dependencies
img3splat uses `NumPy` and `Pillow`, both of which should be automatically installed on img3splat installation.

Additionally, to run the generated macros, you also need [JonathanNye's NXBT fork](https://github.com/JonathanNye/nxbt/tree/experiment/busy-wait) (highly recommended to fix timing issues) or the standard version of [NXBT](https://github.com/Brikwerk/nxbt). As img3splat doesn't need NXBT to run (and installation of it requires root privileges), it is not included as a dependency.
