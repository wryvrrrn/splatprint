# img3splat  (insert original name here)
img3splat is a post printer for Splatoon 3 that generates macros for [NXBT](https://github.com/Brikwerk/nxbt), allowing you to print from a Linux machine with a Bluetooth connection rather than a specialized microcontroller. img3splat is heavily inspired by [img2splat](https://github.com/JonathanNye/img2splat), but implements new features to (hopefully) increase reliability.

## TL;DR: How to print
- Install [NXBT](https://github.com/Brikwerk/nxbt). Due to alleged timing issues with longer macros, img3splat has only been tested with [JonathanNye's fork of NXBT](https://github.com/JonathanNye/nxbt), but it may work with the main branch. If you have errors on installation, make sure to check the "Troubleshooting" portion of NXBT's README.md.
- Run NXBT's test function to ensure connectivity and make sure controller pairs properly
- Install img3splat (insert pip command here)
- Create your plaza post (320x120 image, will be auto-converted to 2-bit greyscale (no dithering))
- run img3splat (command)
- canvas horizontal on empty canvas (unless using "inverse", then all black), minimum brush size on top left, press sync button on controllers
- run NXBT macro (command); will automatically press minus to save on completion
- once finished, if there's any printing errors, take a screenshot of the post editor with the cursor minimum size top left
- run img3splat in repair mode (command)
- run NXBT with repair macro (command)
- repeat if needed

## Why img3splat?
img3splat is designed for higher reliability when printing complex posts, minimizing the need for manual touchups due to dropped inputs. This sacrifices some speed, but the program has some optimizations in place to reduce print time for simpler posts.

- printing in full columns reduces the area of effect of dropped inputs (as cursor is aligned at the edge more frequently), reducing print time for repair operations
- skips empty columns rather than taking a naive approach, reducing print time
- supports taking a screenshot of the Splatoon post interface to check for errors, generates a repair macro that only targets the affected columns
- repair macro also easily allows for small tweaks to the original image without reprinting the whole thing

## Print demo (what to expect)
original image

generated macro and inverse previews, blue indicates cursor travel, black (for macro) or white (for inverse) indicates printed pixels

first pass result

repair macro preview

second pass result

## Arguments/outputs
### Arguments
- image: required, the post you want to print; 320x120 horizontal image (doesn't need to be black and white (auto-converted based on luminance), supports any format supported by `Pillow`)
- repair image: optional, 1280x720 screenshot of the post interface (make sure cursor is smallest and set to top left (or maybe you don't get the cursor if you don't use the dpad? idk)); also accepts a 320x120 image if you already processed it for some reason
- override last row detection (repair): useful if the program isn't detecting the last row of the screenshot image properly (as it's one line of pixels with color bleed due to jpg compression); reprints the bottom pixel of any column that otherwise requires repair, ignores them otherwise regardless of what color they're detected as 
- delay: amount of time between inputs in seconds (0.1 by default), can decrease to increase speed at the risk of higher dropped inputs
- columns: single column or min-max, will only print those columns (assumes columns are empty); likely unneeded with repair function
- start in place: requires column input, will print assuming your cursor is at the top of the leftmost column you're printing at rather than starting at
- verbose: outputs when the program generates a macro file or macro preview file
- show instructions: outputs printing instructions after generating a macro (including sudo nxbt)

### Outputs
- `nrm_macro.txt` and `inv_macro.txt`: macro files generated when running the program normally; `nrm_macro.txt` is for a blank canvas, `inv_macro.txt` is for an all-black canvas
- `rpr_macro.txt`: macro file generated when running in repair mode, assumes in-game post is same as screenshot
- `nrm_preview.png`, `inv_preview.png`, and `rpr_preview.png`: preview of cursor movement during macro execution; for nrm, white = untouched by cursor, blue = passed over by cursor, black = ink; for inv, black = untouched by cursor, blue = passed over by cursor, white = erase; for repair, gray = untouched by cursor, blue = passed over by cursor, black = ink, white = erase

## Dependencies
img3splat uses `NumPy` and `Pillow`, both of which should be automatically installed on img3splat installation.

To run the generated macros, you also need [NXBT](https://github.com/Brikwerk/nxbt) or [JonathanNye's NXBT fork](https://github.com/JonathanNye/nxbt) (which supposedly fixes some timing issues with longer macros).

## Issues
this shit is mostly just for personal use I'm only planning on implementing what i need
