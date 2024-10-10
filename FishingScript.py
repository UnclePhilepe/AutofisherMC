import pyaudio
import numpy as np
import pyautogui
import time
import threading

# Configuration
DEVICE_INDEX = 2        # Index of the audio device (Line (7- Astro A50 Game))
CHUNK = 1024            # Number of audio samples per frame
RATE = 48000            # Sampling rate (matches the device's sample rate)
WAIT_TIME = 3           # Seconds to wait before casting the rod
THRESHOLD = 0.0020      # Threshold for detecting a fish bite sound level
MINIMUM_SOUND_LEVEL = 0.0001  # Minimum sound level to consider
COOLDOWN_TIME = 2       # Seconds to ignore sound after casting
CHECK_INTERVAL = 0.05   # Interval in seconds between sound level checks
RECAST_TIMEOUT = 30     # Seconds to wait before recasting if no bite detected

# Initialize PyAudio
p = pyaudio.PyAudio()

# Get the number of input channels for the selected device
device_info = p.get_device_info_by_index(DEVICE_INDEX)
channels = int(device_info['maxInputChannels'])

if channels < 1:
    print("The selected audio device does not support input channels.")
    p.terminate()
    exit(1)

def cast_rod():
    """Simulate casting the rod by pressing RMB once."""
    print("Casting the rod...")
    pyautogui.click(button='right')  # Single click to cast the rod

def reel_in_rod():
    """Simulate reeling in the rod by pressing RMB once."""
    print("Reeling in the rod...")
    pyautogui.click(button='right')  # Single click to reel in the rod

def recast_timer():
    """Timer function to recast the rod if no bite is detected within RECAST_TIMEOUT seconds."""
    global last_cast_time
    while True:
        time.sleep(RECAST_TIMEOUT)
        if time.time() - last_cast_time > RECAST_TIMEOUT:
            print("No bite detected for a while. Recasting...")
            reel_in_rod()
            time.sleep(WAIT_TIME)
            cast_rod()
            last_cast_time = time.time()

# Wait before starting
print(f"Waiting {WAIT_TIME} seconds before casting the rod...")
time.sleep(WAIT_TIME)

# Cast the rod initially
cast_rod()

# Cooldown period after casting
last_cast_time = time.time()

# Start the recast timer thread
recast_thread = threading.Thread(target=recast_timer, daemon=True)
recast_thread.start()

# Open the audio stream
stream = p.open(format=pyaudio.paFloat32,
                channels=channels,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK,
                input_device_index=DEVICE_INDEX)

print("Tracking audio levels... Press Ctrl+C to stop.")

try:
    while True:
        # Read audio data from the stream
        audio_data = np.frombuffer(stream.read(CHUNK, exception_on_overflow=False), dtype=np.float32)

        # Compute the RMS (Root Mean Square) value of the audio signal
        rms = np.sqrt(np.mean(np.square(audio_data)))

        # Ignore values below the minimum sound level
        if rms < MINIMUM_SOUND_LEVEL:
            time.sleep(CHECK_INTERVAL)
            continue

        # Check if the cooldown period after casting has passed
        if time.time() - last_cast_time < COOLDOWN_TIME:
            time.sleep(CHECK_INTERVAL)
            continue

        # Check if the RMS value indicates a fish bite
        if rms > THRESHOLD:
            print(f"Fish bite detected! Sound Level: {rms:.4f}")
            # Reel in the fishing rod
            reel_in_rod()

            # Wait a few seconds before casting again
            print("Waiting before recasting...")
            time.sleep(WAIT_TIME)

            # Cast the rod again
            cast_rod()

            # Update last cast time
            last_cast_time = time.time()

        # Short delay before the next check
        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\nStopped tracking.")

finally:
    # Clean up: close the stream and terminate PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()