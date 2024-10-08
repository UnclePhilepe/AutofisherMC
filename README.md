
# Minecraft Bedrock Edition Auto-Fishing Script

This script automates the process of fishing in Minecraft Bedrock Edition. It detects the bobber based on color and reels in the fish automatically when it detects specific conditions, such as the bobber moving or disappearing. This is a personal project and is not set up for wide use. Feel free to customize it to your own specific setup.

## Features
- Detects the bobber using screen capture and HSV color filtering.
- Reels in the fish when the bobber moves downward or disappears.
- Automatically re-casts the fishing rod after reeling in.
- Logs events such as reeling in and re-casting, including reasons for these actions.
- Can be stopped without killing the process, ensuring all actions (the script does) are logged.
- Now uses `dxcam` for smoother screen capture performance with higher frame rates.

## Requirements
- Python 3.8+
- Libraries:
  - OpenCV (`cv2`)
  - NumPy (`numpy`)
  - pyautogui
  - dxcam (`dxcam`)
  - dotenv
  - screeninfo

To install the required libraries, run:

```bash
pip install opencv-python numpy pyautogui dxcam python-dotenv screeninfo
```

## How to Use

### 1. **Mouse Calibration Script** (Optional but Recommended)
If you need to find the coordinates for your Minecraft window’s fishing bobber area, use the provided mouse calibration script. It helps you find the top-left (X1, Y1) and bottom-right (X2, Y2) coordinates for the region of interest (ROI).
1. Run the script and move your mouse to the top-left and bottom-right corners of the area you want to capture in the Minecraft window.
2. The script will display the coordinates, which you can plug into the `BOBBER_SEARCH_AREA` in the auto-fishing script.

### 2. **Auto-Fishing Script**
1. Adjust the `BOBBER_SEARCH_AREA` in the script using the coordinates you obtained from the calibration script.
2. Run the script.
3. The fishing process will start automatically, showing a live feed for detection. You can stop the script by pressing `CTRL+C` in the terminal or `CTRL+SHIFT+S` in-game, which will save a log file (`fishing_log.txt`) containing the reasons for each reeling in and recasting event.

### Changes in This Version:
- The script now uses `dxcam` instead of `mss` for improved screen capture performance, enabling smoother real-time detection with higher frame rates.
- Optimized for smoother operation without flicker, especially on setups with multiple monitors.

## Logging
The script logs the following events:
- **Casting Fishing Rod** – When the rod is cast out.
- **Reeling in the Fish** – When the rod is reeled in, along with the reason (e.g., bobber movement, disappearance).
- **Recasting** – When the rod is re-cast after reeling in.

The logs are saved to `fishing_log.txt` in the same directory as the script.

## Shutdown
To stop the script, press `CTRL+C` in the terminal or `CTRL+SHIFT+S` in-game. The script will stop capturing, save the log file, and exit cleanly.

## Known Issues
- **Bobber Detection Fails**: If the bobber is not detected consistently, you may need to adjust the `BOBBER_SEARCH_AREA` or the HSV color range.
- **Single Monitor Setup**: The script is optimized for a two-monitor setup, displaying the feed on the secondary monitor. You may need to adjust the monitor index for a single monitor setup.
- **Screen Flicker**: Flickering may occur in some setups when displaying the live detection feed.
- **Cast Loop**: Sometimes when catching a salmon the script will loop in a casting and reel state, the current fix is to manually cast.

