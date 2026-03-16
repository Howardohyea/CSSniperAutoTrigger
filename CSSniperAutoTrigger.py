# CODE THAT MAY NOT WORK

import time
import os
import sys
import mss
import mss.tools
from pynput import keyboard
from pynput import mouse
import threading

# ================= CONFIGURATION =================
# The 5x5 Region to monitor (Top-Left X, Top-Left Y, Width, Height)
# You will need to find these coordinates to fit your window
MONITOR_REGION = {"top": 538, "left": 1278, "width": 5, "height": 5}
# Sensitivity: Higher = Less Sensitive (More change required to trigger)
CHANGE_THRESHOLD = 400

# Stability: How many consecutive frames must show change before triggering?
# 1 = Fast but prone to glitches. 3 = Stable but slower.
PERSISTENCE_FRAMES = 2

# Hotkeys
START_STOP_KEY = keyboard.Key.f1  # Press f1 to start/stop monitoring
EXIT_KEY = keyboard.Key.f7     # Press ESC to quit program entirely

# Stop after one trigger? (False = Keep monitoring)
STOP_AFTER_TRIGGER = False
# ===================================================

class ScreenMonitor:
    def __init__(self):
        self.running = False
        self.monitoring = False
        self.previous_frame = None
        self.change_counter = 0
        self.last_trigger_time = 0
        self.cooldown = 1.2  # Seconds to wait before allowing another trigger
        
        # Initialize screen capture
        try:
            self.sct = mss.mss()
        except Exception as e:
            print(f"Error initializing screen capture: {e}")
            sys.exit(1)

    def get_frame_data(self):        
        self.sct=mss.mss()
        """Capture the 5x5 region and return raw pixel bytes."""
        try:
            # Capture the region
            screenshot = self.sct.grab(MONITOR_REGION)
            # Return raw bytes (BGRA format usually)
            return screenshot.raw
        except Exception as e:
            print(f"Capture error: {e}")
            return None

    def calculate_difference(self, current, previous):
        """
        Calculate Sum of Absolute Differences (SAD) between two frames.
        Returns an integer representing total change.
        """
        if len(current) != len(previous):
            return 0
        
        total_diff = 0
        # Iterate through every byte (R, G, B, A for each pixel)
        for c, p in zip(current, previous):
            total_diff += abs(c - p)
        
        return total_diff

    def trigger_action(self):
        """Emulate the key press."""
        print(f"[TRIGGER] Change detected! Pressing 'LMB'")
        try:
            from pynput.keyboard import Controller
            from pynput.mouse import Button, Controller
            kb = Controller()
            mouse = Controller()
            mouse.press(Button.left)
            mouse.release(Button.left)
        except Exception as e:
            print(f"Key press failed: {e}")

    def monitor_loop(self):
        """Main monitoring logic."""
        print("Monitoring started...")
        
        # Initialize first frame
        self.previous_frame = self.get_frame_data()
        time.sleep(0.01)
        
        while self.monitoring:
            current_frame = self.get_frame_data()
            
            if current_frame and self.previous_frame:
                diff = self.calculate_difference(current_frame, self.previous_frame)
                
                # Debug: Uncomment to see live difference values
                # print(f"Frame Diff: {diff}") 
                
                if diff > CHANGE_THRESHOLD:
                    self.change_counter += 1
                else:
                    self.change_counter = 0
                
                # Check if change is persistent enough
                if self.change_counter >= PERSISTENCE_FRAMES:
                    # Check cooldown
                    now = time.time()
                    if now - self.last_trigger_time > self.cooldown:
                        self.trigger_action()
                        self.last_trigger_time = now
                        
                        if STOP_AFTER_TRIGGER:
                            print("Stopping after trigger.")
                            self.monitoring = False
                            break
                        
                        # Reset counter after trigger to avoid double-triggering
                        self.change_counter = 0
            
            # Update frame for next loop
            self.previous_frame = current_frame
            
            # Sleep to control CPU usage 
            time.sleep(0.01)

    def on_press(self, key):
        """Handle global hotkeys."""
        try:
            if key == EXIT_KEY:
                print("\nExiting program...")
                self.running = False
                self.monitoring = False
                return False  # Stop listener
            
            if key == START_STOP_KEY:
                if not self.monitoring:
                    print("Monitoring started.")
                    self.monitoring = True
                    self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
                    self.monitor_thread.start()
                    # Start monitor loop in separate thread
                    t = threading.Thread(target=self.monitor_loop, daemon=True)
                    t.start()
        except Exception as e:
            print(f"Key handler error: {e}")

    def on_release(self,key):
        try:
            if key == START_STOP_KEY:
                print("Monitoring stopped")
                self.monitoring=False
                
                    
        except Exception as e:
            print(f"Key handler error: {e}")

    def run(self):
        """Start the program."""
        print("=" * 50)
        print("VNC Pixel Monitor")
        print("=" * 50)
        print(f"Region: {MONITOR_REGION}")
        print(f"Threshold: {CHANGE_THRESHOLD}")
        print(f"Press F1 to Start/Stop Monitoring")
        print(f"Press F7 to Exit")
        print("=" * 50)
        
        self.running = True
        
        # Start keyboard listener
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            while self.running:
                time.sleep(0.1)
            listener.stop()

if __name__ == "__main__":
    try:
        monitor = ScreenMonitor()
        monitor.run()
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Critical error: {e}")