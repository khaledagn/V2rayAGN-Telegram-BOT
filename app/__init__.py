import os
import json

# Constants for configuration paths
CONFIGS_DIR = "app/configs"
CONFIGS_FILE = os.path.join(CONFIGS_DIR, "configs.json")

try:
    # Ensure the configs directory exists
    os.makedirs(CONFIGS_DIR, exist_ok=True)

    # Check if the configs.json file exists; create it if not
    if not os.path.exists(CONFIGS_FILE):
        with open(CONFIGS_FILE, "w") as f:
            json.dump({}, f, indent=4)  # Write an empty JSON object
        print(f"Initialized configs.json at {CONFIGS_FILE}")
except Exception as e:
    print(f"Error initializing configurations: {e}")
