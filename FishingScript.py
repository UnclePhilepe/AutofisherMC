import cv2
import numpy as np
import pyautogui
import time
import threading
import os
from dotenv import load_dotenv
from screeninfo import get_monitors
import dxcam  # Using dxcam for smoother screen capture
import logging
import signal
import sys
import keyboard  # Global hotkeys

# Load the .env file manually
dotenv_path = r"C:\\Users\\John\\Desktop\\.env"  # Env table for previous version (unused)
load_dotenv(dotenv_path)

# Define the region of interest (ROI) based on your coordinates
BOBBER_SEARCH_AREA = (
    1164,  # Top-left X1
    572,   # Top-left Y1
    1387,  # Bottom-right X2
    747    # Bottom-right Y2
)

# HSV color range for detecting red
lower_red = np.array([0, 120, 70])  # Lower bound for red
upper_red = np.array([10, 255, 255])  # Upper bound for red

# Timer threshold for reeling in after losing track of red
lost_bobber_threshold = 0.5  # Time (in seconds) to wait before reeling in when the red bobber is lost
vertical_movement_threshold = 25  # Minimum downward movement in pixels to trigger immediate reel-in

# Consecutive downward movements required to trigger reeling in
consecutive_downward_movements_required = 3
downward_movements_counter = 0

# Event to stop the script
stop_event = threading.Event()

# Clear the log file at the start of each run
log_file = "fishing_log.txt"
with open(log_file, "w"):  # Opening in write mode clears the file
    pass

# Set up logging
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

# Get monitor information using screeninfo
monitors = get_monitors()
monitor_index = 1  # Adjust if needed
second_monitor = monitors[monitor_index]
second_monitor_x_offset = second_monitor.x
second_monitor_y_offset = second_monitor.y

# Variable to track last known vertical position of the bobber
last_bobber_position = None

# Initialize dxcam for screen capture
camera = None

def initialize_camera():
    """Initialize the dxcam object."""
    global camera
    try:
        if camera is not None:
            logging.info("Deleting existing dxcam instance.")
            del camera  # Ensure we delete the existing instance
            camera = None
        logging.info("Creating a new dxcam instance.")
        camera = dxcam.create(output_color="BGR")
        return camera
    except Exception as e:
        logging.error(f"Failed to initialize camera: {e}")
        return None

def signal_handler(sig, frame):
    """Handle the signal to stop the script gracefully."""
    print("Stopping script... Please wait for logs to be saved.")
    stop_event.set()

def on_stop_keypress():
    """Function to be called when the stop key combination is pressed."""
    print("Global stop key pressed.")
    stop_event.set()

# Register the global key combination (CTRL+SHIFT+S) to stop the script
keyboard.add_hotkey('ctrl+shift+s', on_stop_keypress)

def capture_screen():
    """Capture the screen and display the live feed with red bobber detection using dxcam."""
    global camera
    cv2.namedWindow("Minecraft Autofishing Feed", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Minecraft Autofishing Feed", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.moveWindow("Minecraft Autofishing Feed", second_monitor_x_offset, second_monitor_y_offset)

    while not stop_event.is_set():
        try:
            # Capture frame using dxcam
            frame = camera.grab()

            if frame is None:
                logging.warning("No frame captured. Skipping this frame.")
                continue  # Skip if no frame was captured

            # Crop the frame to the search area
            roi_frame = frame[BOBBER_SEARCH_AREA[1]:BOBBER_SEARCH_AREA[3], BOBBER_SEARCH_AREA[0]:BOBBER_SEARCH_AREA[2]]

            # Draw the blue rectangle for the search area (ROI) in the original frame
            cv2.rectangle(frame, (BOBBER_SEARCH_AREA[0], BOBBER_SEARCH_AREA[1]), 
                          (BOBBER_SEARCH_AREA[2], BOBBER_SEARCH_AREA[3]), (255, 0, 0), 2)  # Blue box

            # Convert the cropped frame (ROI) to HSV color space for color-based detection
            hsv_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

            # Create a mask for detecting red
            red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

            # Find contours of the red areas
            contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Find the largest red contour (assumed to be the bobber)
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)
                
                # Draw a green rectangle around the largest red area (the bobber) in the cropped frame
                cv2.rectangle(roi_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the live feed with the blue search box (on the full frame) and red bobber detection
            cv2.imshow("Minecraft Autofishing Feed", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(1/60)  # Control frame rate to ~60fps
        except Exception as e:
            logging.error(f"Error during screen capture: {e}")
            camera = initialize_camera()  # Reinitialize camera if an error occurs

    cv2.destroyAllWindows()

def cast_fishing_rod():
    """Simulate a right-click to cast the fishing rod."""
    logging.info("Casting fishing rod.")
    pyautogui.click(button='right')

def reel_in_fish(reason):
    """Simulate a right-click to reel in the fish and log the reason."""
    logging.info(f"Reeling in the fish. Reason: {reason}")
    pyautogui.click(button='right')

def detect_bobber():
    """Detect the presence and position of the red bobber within the ROI."""
    global camera
    try:
        frame = camera.grab()

        if frame is None:
            logging.warning("No frame captured during bobber detection. Skipping this detection.")
            return (False, None)  # Skip if no frame was captured

        # Crop the frame to the search area (ROI)
        roi_frame = frame[BOBBER_SEARCH_AREA[1]:BOBBER_SEARCH_AREA[3], BOBBER_SEARCH_AREA[0]:BOBBER_SEARCH_AREA[2]]

        # Convert the cropped frame to HSV color space for color-based detection
        hsv_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)

        # Create a mask for detecting red
        red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

        # Find contours of the red areas
        contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Red detected (bobber is visible)
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            return (True, y + h // 2)  # Return True and the vertical position of the bobber
        else:
            # Red not detected (bobber is not visible)
            return (False, None)
    except Exception as e:
        logging.error(f"Error during bobber detection: {e}")
        camera = initialize_camera()  # Reinitialize camera if an error occurs
        return (False, None)

def auto_fish():
    """Main auto-fishing loop with continuous casting."""
    global last_bobber_position
    global downward_movements_counter

    # Initialize the camera before starting the main loop
    initialize_camera()

    # Start showing the live screen capture
    capture_thread = threading.Thread(target=capture_screen)
    capture_thread.daemon = True
    capture_thread.start()

    while not stop_event.is_set():
        # Cast the fishing rod
        cast_fishing_rod()

        # Delay to allow the bobber to settle in the water before starting detection
        time.sleep(3)

        time_of_last_bobber_detection = time.time()

        while not stop_event.is_set():
            # Detect if the bobber is visible and get its vertical position
            bobber_detected, bobber_vertical_position = detect_bobber()

            if bobber_detected:
                # Reset the timer if the bobber is detected
                time_of_last_bobber_detection = time.time()

                # Detect sudden vertical movement down
                if last_bobber_position is not None and bobber_vertical_position is not None:
                    vertical_movement = last_bobber_position - bobber_vertical_position
                    if vertical_movement > vertical_movement_threshold:
                        # Increment counter for consecutive downward movements
                        downward_movements_counter += 1
                        if downward_movements_counter >= consecutive_downward_movements_required:
                            reel_in_fish("Sudden vertical downward movement detected")
                            downward_movements_counter = 0  # Reset the counter
                            break  # Exit the inner loop to immediately recast the rod
                    else:
                        # Reset counter if no significant downward movement
                        downward_movements_counter = 0

                # Update the last known bobber position
                last_bobber_position = bobber_vertical_position
            else:
                # Check how long the bobber has been lost
                time_since_last_detection = time.time() - time_of_last_bobber_detection
                if time_since_last_detection > lost_bobber_threshold:
                    reel_in_fish("Bobber lost for more than 0.5 seconds")
                    break  # Exit the inner loop to immediately recast the rod

            # Wait for a short time before checking again
            time.sleep(0.1)

        # Immediately recast the fishing rod after reeling in
        logging.info("Recasting the rod immediately.")
        cast_fishing_rod()

if __name__ == "__main__":
    # Set up the signal handler to stop the script with CTRL+C
    signal.signal(signal.SIGINT, signal_handler)
    print("Starting auto-fishing with continuous casting and immediate recast after reeling...")
    auto_fish()
