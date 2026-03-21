# CODE THAT MAY NOT WORK
import time
import sys
import mss
from pynput import keyboard, mouse
import threading
import random

# ================= CONFIGURATION =================
# The 5x5 Region to monitor (Top-Left X, Top-Left Y, Width, Height)
# You will need to find these coordinates to fit your window
MONITOR_REGION = {"top": 538, "left": 1278, "width": 5, "height": 5}
# Sensitivity: Higher = Less Sensitive (More change required to trigger)
CHANGE_THRESHOLD = 500

# Stability: How many consecutive frames must show change before triggering?
# 1 = Fast but prone to glitches. 3 = Stable but slower.
PERSISTENCE_FRAMES = 2

# Hotkeys
START_STOP_KEY = keyboard.Key.f1  # Press f1 to start/stop monitoring
EXIT_KEY = keyboard.Key.f7     # Press f7 to quit program entirely

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
        self.cooldown = 1.3 # Cooldown before another mouse input is triggered.
        self.monitor_thread = None
        self.sct = None  # Will be created in the monitoring thread

    def get_frame_data(self):
        """Capture the 5x5 region and return raw pixel bytes."""
        # mss instance was created here, now it's moved
        try:
            screenshot = self.sct.grab(MONITOR_REGION)
            return screenshot.raw
        except Exception as e:
            print(f"Capture error: {e}")
            return None

    # Sum of Absolute Difference calculations
    def calculate_difference(self, current, previous):
        if len(current) != len(previous):
            return 0
        return sum(abs(c - p) for c, p in zip(current, previous))

    def trigger_action(self):
        import random
        print("[TRIGGER] Change detected! Pressing 'LMB'")
        delay = random.randint(30,80)
        try:
            ctrl = mouse.Controller()
            ctrl.press(mouse.Button.left)
            time.sleep(delay/1000)
            ctrl.release(mouse.Button.left)
        except Exception as e:
            print(f"Mouse press failed: {e}")

    def monitor_loop(self):
        print("Monitoring started...")
        try:
            self.sct = mss.mss() # mss instance is started in the loop, 
        except Exception as e:
            print(f"Error initializing screen capture: {e}")
            self.monitoring = False
            return

        try:
            # Initialize first frame
            self.previous_frame = self.get_frame_data()
            time.sleep(0.01)

            while self.monitoring:
                current_frame = self.get_frame_data()
                
                if current_frame and self.previous_frame:
                    diff = self.calculate_difference(current_frame, self.previous_frame)
                    
                    if diff > CHANGE_THRESHOLD:
                        self.change_counter += 1
                    else:
                        self.change_counter = 0

                    if self.change_counter >= PERSISTENCE_FRAMES:
                        now = time.time()
                        if now - self.last_trigger_time > self.cooldown:
                            self.trigger_action()
                            self.last_trigger_time = now
                            
                            if STOP_AFTER_TRIGGER:
                                print("Stopping after trigger.")
                                self.monitoring = False
                                break
                            
                            self.change_counter = 0

                self.previous_frame = current_frame
                time.sleep(0.01)
        finally:
            if self.sct:
                self.sct.close()
                self.sct = None
            print("Monitoring stopped")

    def on_press(self, key):
        try:
            if key == EXIT_KEY:
                print("\nExiting program...")
                self.running = False
                self.monitoring = False
                return False
            
            if key == START_STOP_KEY and not self.monitoring:
                print("Monitoring started.")
                self.monitoring = True
                self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
                self.monitor_thread.start()
        except Exception as e:
            print(f"Key handler error: {e}")

    def on_release(self, key):
        try:
            if key == START_STOP_KEY and self.monitoring:
                print("Monitoring stopped.")
                self.monitoring = False
        except Exception as e:
            print(f"Key handler error: {e}")

    def run(self):
        print("=" * 50)
        print("VNC Pixel Monitor")
        print("=" * 50)
        print(f"Region: {MONITOR_REGION}")
        print(f"Threshold: {CHANGE_THRESHOLD}")
        print("Press F1 to Start/Stop Monitoring")
        print("Press F7 to Exit")
        print("=" * 50)

        self.running = True
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