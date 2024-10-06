
# Minecraft Bedrock Edition Auto-Fishing Script

This script automates the process of fishing in Minecraft Bedrock Edition. It detects the bobber based on color and reels in the fish automatically when it detects specific conditions, such as the bobber moving or disappearing. The script also provides a graceful way to stop and log events during fishing sessions.

## Features
- Detects the bobber using screen capture and HSV color filtering.
- Reels in the fish when the bobber moves downward or disappears.
- Automatically re-casts the fishing rod after reeling in.
- Logs events such as reeling in and re-casting, including reasons for these actions.
- Can be stopped gracefully without killing the process, ensuring all actions are logged.

## Requirements
- Python 3.8+
- Libraries:
  - OpenCV (`cv2`)
  - NumPy (`numpy`)
  - pyautogui
  - MSS (`mss`)
  - dotenv
  - screeninfo

To install the required libraries, run:

```bash
pip install opencv-python numpy pyautogui mss python-dotenv screeninfo
```

## How to Use
1. Clone or download this repository.
2. Set up your `.env` file as needed (currently not used in this version, but you can configure it for future use).
3. Adjust the `BOBBER_SEARCH_AREA` in the script to match the coordinates of your Minecraft window’s bobber location on your monitor.
4. Run the script:

```bash
python auto_fishing.py
```

5. The fishing process will start automatically, showing a live feed for detection. You can stop the script gracefully by pressing `CTRL+C` in the terminal, which will save a log file (`fishing_log.txt`) containing the reasons for each reeling in and recasting event.

## Logging
The script logs the following events:
- **Casting Fishing Rod** – When the rod is cast out.
- **Reeling in the Fish** – When the rod is reeled in, along with the reason (e.g., bobber movement, disappearance).
- **Recasting** – When the rod is re-cast after reeling in.

The logs are saved to `fishing_log.txt` in the same directory as the script.

## Graceful Shutdown
To stop the script gracefully, press `CTRL+C` in the terminal. The script will stop capturing, save the log file, and exit cleanly.
