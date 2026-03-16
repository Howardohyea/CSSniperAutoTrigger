# Counter Strike Auto Trigger
This python script reads the change of a region of 5x5 pixels centered around your crosshair. If the Sum of Absolute Differnece (SAD) of the current frame is larger than a certain threshold, Left Click is automatically triggered. 

# Features
1. SAD instead of fixed colors. This ensures the trigger will not shoot at ambient effects (dust, clouds), or slight crosshair movements.
2. Configurable trigger point and timings. Customize for different maps, playstyle, or even add realistic artificial delay.
3. Push-to-activate instead of toggle ensures maximum flexibility.

# Known bugs and limitations
`Capture error: gdi32.GetDIBits() failed.` is thrown after approximately 50 seconds of cumulative use, requiring a restart of the script. `mss` buffers may need to be flushed or threading to be smarter.

Screen Capture and Keyboard/Mouse Manipulation *may* not work under Linux Wayland. This is untested however. Testers welcome.
