import os
from dotenv import load_dotenv
#######----------------////This is NOT NEEDED on the current version of auto fishing\\\\ -----------------#################
# Manually specify the path to the .env file (try the script folder or Desktop)
dotenv_path = r"C:\Users\John\Desktop\Minecraft Autofishins script\.env"

# Check if the .env file exists at the specified location
if not os.path.exists(dotenv_path):
    print(f"Error: .env file not found at {dotenv_path}")
    print(f"Files in directory: {os.listdir(r'C:\Users\John\Desktop\Minecraft Autofishins script')}")
else:
    print(f".env file found at {dotenv_path}")

# Load the .env file
load_dotenv(dotenv_path)

# Debugging: Print the loaded environment variables
print("Loaded BOBBER_BOX_X1:", os.getenv('BOBBER_BOX_X1'))
print("Loaded BOBBER_BOX_Y1:", os.getenv('BOBBER_BOX_Y1'))
print("Loaded BOBBER_BOX_X2:", os.getenv('BOBBER_BOX_X2'))
print("Loaded BOBBER_BOX_Y2:", os.getenv('BOBBER_BOX_Y2'))