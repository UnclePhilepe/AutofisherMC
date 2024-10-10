# Minecraft Bedrock Edition Auto-Fishing Script

This script automates the process of fishing in Minecraft Bedrock Edition. It uses audio detection to identify when a fish bites and automatically reels it in. This is a personal project and is not set up for wide use. Feel free to customize it to your own specific setup.

## Features
- Detects fish bites using audio input analysis.
- Automatically reels in the fish when a bite is detected.
- Automatically re-casts the fishing rod after reeling in.
- Implements a recast timer to ensure the rod is always in the water.
- Configurable parameters for fine-tuning to your specific setup.
- Can be stopped safely using keyboard interrupt (Ctrl+C).

## Requirements
- Python 3.8+
- Libraries:
  - PyAudio
  - NumPy
  - PyAutoGUI
  - Time
  - Threading

To install the required libraries, run:

```bash
pip install pyaudio numpy pyautogui
```

## How to Use

1. Adjust the script parameters in the configuration section:
   - `DEVICE_INDEX`: Set this to the index of your audio input device.
   - `THRESHOLD`: Adjust this value to fine-tune fish bite detection sensitivity.
   - Other parameters like `WAIT_TIME`, `COOLDOWN_TIME`, and `RECAST_TIMEOUT` can also be modified as needed.

2. Run the script:
   ```
   python minecraft_auto_fishing.py
   ```

3. The script will start automatically. Ensure your Minecraft character is in position to fish before starting.

4. To stop the script, press `Ctrl+C` in the terminal where it's running.

## Script Operation

1. The script starts by casting the rod.
2. It then continuously monitors the audio input for sounds above the set threshold.
3. When a fish bite is detected (audio level exceeds the threshold):
   - The rod is reeled in.
   - After a short wait, the rod is re-cast.
4. If no bite is detected for a set period (default 30 seconds), the rod is automatically recast.
5. This process repeats until the script is manually stopped.

## Logging
The script provides real-time console output, including:
- Current sound levels
- Fish bite detections
- Rod casting and reeling actions

## Shutdown
To stop the script, press `Ctrl+C` in the terminal. The script will close the audio stream and terminate cleanly.

## Customization
You can adjust various parameters in the script to optimize for your specific setup:
- `THRESHOLD`: Adjust this to change the sensitivity of fish bite detection.
- `WAIT_TIME`: Change the delay between reeling in and recasting.
- `COOLDOWN_TIME`: Modify the period after casting during which bite detection is ignored.
- `RECAST_TIMEOUT`: Alter the time after which the rod is recast if no bite is detected.

## Known Issues and Troubleshooting
- **False Positives**: If the script is triggering too often, try increasing the `THRESHOLD` value.
- **Missed Bites**: If the script is missing fish bites, try decreasing the `THRESHOLD` value.
- **Audio Device Issues**: Ensure the correct `DEVICE_INDEX` is set for your audio input device.

## Future Improvements
- Implement more sophisticated audio analysis for improved bite detection.
- Add a graphical user interface for easier configuration and monitoring.
- Incorporate error handling and logging to a file for debugging long sessions.

Remember to use this script responsibly and in accordance with the rules of the server you're playing on. Happy fishing!
