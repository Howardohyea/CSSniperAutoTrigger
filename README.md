# Pixel Monitor Auto Trigger
This python script reads the change of a region of 5x5 pixels centered around your crosshair. If the Sum of Absolute Differnece (SAD) of the current frame is larger than a certain threshold, Left Click is automatically triggered. 

# Features
1. SAD instead of fixed colors. This ensures the trigger will not shoot at ambient effects (dust, clouds), or slight crosshair movements.
2. Configurable trigger point and timings. Customize for different maps, playstyle, or even add artificial delay.
3. Push-to-activate instead of toggle ensures maximum flexibility.

# Setup
1. Install [python](https://www.python.org/downloads/) and pip. Only the latest version of Python is tested, I do not guarantee support for older versions. 
2. Install the dependencies `mss` and `pynput`. 
   - `pip install mss`
   - `pip install pynput`
3. Configure the `MONITOR_REGION` on Line 15 to fit your own monitor size. On the most common 1920x1080 resolution, the config is `"top": 538, "left": 1278`. Adapt this number to fit your own screen.
   - To get this region for any resolution, divide your screen width and height (in pixels) by 2, then subtract 2 to the result.
   - Formula: `(pixels/2)-2`

# Known bugs and limitations
`Capture error: gdi32.GetDIBits() failed.` is thrown after approximately 30 seconds of cumulative use, requiring a restart of the script. This ***may*** be a Resource leak on Windows related to the mss library. Flushing `mss` buffers or smarter threading may fix this. Code submissions is welcome. 

**[Update]** A recent commit fe1f4c6 has vastly improved the situation, bringing the use time up to approximately 5 minutes. However, the issue isn't fundamentally fixed and a GDI error is still thrown, requiring a restart of the script.

Screen Capture and Keyboard/Mouse Manipulation *may* not work under Linux Wayland. This is untested however. Testers welcome.