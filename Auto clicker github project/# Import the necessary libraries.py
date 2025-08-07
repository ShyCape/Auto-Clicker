import pyautogui
import time
import random
import threading
from pynput.keyboard import Key, Listener

# --- Configuration ---
# The key to press to toggle the autoclicker
TOGGLE_KEY = '\\'

# Global state variable for the autoclicker
running = False

# --- Get Clicks-per-second from User ---
while True:
    try:
        cps = float(input("Enter the desired clicks per second (e.g., 10): "))
        if cps <= 0:
            print("Please enter a number greater than 0.")
            continue
        
        # Calculate the base delay (1 / cps) and create a small random range around it
        base_delay = 1.0 / cps
        min_delay = base_delay * 0.75  # 25% faster
        max_delay = base_delay * 1.25  # 25% slower
        break
    except ValueError:
        print("Invalid input. Please enter a number.")

# --- The Autoclicker Loop ---
def autoclicker_loop():
    """This function runs in a separate thread and performs the clicks."""
    global running
    
    while True:
        while running:
            # Generate a random delay between min_delay and max_delay
            delay = random.uniform(min_delay, max_delay)
            pyautogui.click()
            time.sleep(delay)
        time.sleep(0.1)

# --- Keyboard Listener Function ---
def on_press(key):
    """This function is called every time a key is pressed."""
    global running
    
    try:
        if key.char == TOGGLE_KEY:
            running = not running
            if running:
                print(f"Autoclicker STARTED at ~{cps:.2f} CPS. Press '\\' again to stop.")
            else:
                print("Autoclicker STOPPED. Press '\\' to start.")
    except AttributeError:
        pass

# --- Main Program ---
if __name__ == "__main__":
    # --- Start-up Warning ---
    print("Made By Shy_cape on Github")
    print("\nPress the '\' key to start the autoclicker.")

    # Create and start the autoclicker loop in a separate thread
    autoclicker_thread = threading.Thread(target=autoclicker_loop)
    autoclicker_thread.daemon = True
    autoclicker_thread.start()

    # Create and start the keyboard listener
    with Listener(on_press=on_press) as listener:
        listener.join()