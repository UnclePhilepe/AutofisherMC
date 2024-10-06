import pyautogui
import time

print("Move your mouse to the top-left corner of the desired area.")
time.sleep(5)  # Give you some time to position the mouse
top_left = pyautogui.position()
print(f"Top-left corner: {top_left}")

print("Move your mouse to the bottom-right corner of the desired area.")
time.sleep(5)  # Give you some time to position the mouse
bottom_right = pyautogui.position()
print(f"Bottom-right corner: {bottom_right}")

print(f"Coordinates to use:\nTop-left (X1, Y1): {top_left}\nBottom-right (X2, Y2): {bottom_right}")
