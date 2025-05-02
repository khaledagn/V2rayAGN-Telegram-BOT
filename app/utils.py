import os
import json
import random

CONFIGS_FILE = "app/configs/configs.json"

def read_configs(config_type=None, count=5):
    try:
        if not os.path.exists(CONFIGS_FILE):
            print(f"Configuration file not found: {CONFIGS_FILE}")
            return []

        with open(CONFIGS_FILE, "r") as f:
            configs = json.load(f)

        print(f"Loaded configuration keys: {list(configs.keys())}")

        if config_type not in configs or not isinstance(configs[config_type], list):
            print(f"No valid configurations found for type: {config_type}")
            return []

        random.shuffle(configs[config_type])
        selected_configs = configs[config_type][:count]
        print(f"Selected {count} random {config_type} configurations: {selected_configs}")
        return selected_configs

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in {CONFIGS_FILE}: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error reading {CONFIGS_FILE}: {e}")
        return []


def write_configs(data):
    """
    Write configurations to the JSON file.
    Args:
        data (dict): The configuration data to write to the file.
    """
    try:
        os.makedirs(os.path.dirname(CONFIGS_FILE), exist_ok=True)   
        with open(CONFIGS_FILE, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Configurations successfully written to {CONFIGS_FILE}")
    except Exception as e:
        print(f"Unexpected error writing to {CONFIGS_FILE}: {e}")
