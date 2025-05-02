import requests
import base64
from apscheduler.schedulers.background import BackgroundScheduler
from .utils import write_configs
import os


REMOTE_URLS_JSON = os.getenv("REMOTE_URLS_JSON", "https://www.khaledagn.me/urls.json")  


CONFIG_TYPES = ["vmess", "vless", "trojan", "ss", "ssr", "tuic", "warp"]


FETCH_INTERVAL_MINUTES = 10

def fetch_remote_urls():
    """
    Fetch the list of URLs from the remote JSON file.
    Returns a list of URLs or an empty list if fetching fails.
    """
    try:
        response = requests.get(REMOTE_URLS_JSON, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("urls", [])
    except requests.RequestException as e:
        print(f"Failed to fetch remote URLs: {e}")
    except ValueError as e:
        print(f"Invalid JSON response from remote URLs: {e}")
    return []

def decode_base64(content):
    """
    Decodes Base64 content and returns the decoded text.
    """
    try:
        decoded_bytes = base64.b64decode(content)
        return decoded_bytes.decode("utf-8")
    except (base64.binascii.Error, UnicodeDecodeError) as e:
        print(f"Failed to decode Base64 content: {e}")
        return ""

def fetch_and_update_configs():
    """
    Fetches configuration files from dynamically fetched URLs, decodes Base64 content,
    filters them by type, and replaces the configs.json file with fresh data.
    """
    links = fetch_remote_urls()
    if not links:
        print("No URLs available to fetch configurations.")
        return

    
    filtered_configs = {conf_type: [] for conf_type in CONFIG_TYPES}

    for link in links:
        try:
            print(f"Testing URL: {link}")
            response = requests.get(link, timeout=20)
            response.raise_for_status()

           
            decoded_content = decode_base64(response.text)

             
            for line in decoded_content.splitlines():
                for conf_type in CONFIG_TYPES:
                    if line.startswith(conf_type):
                        filtered_configs[conf_type].append(line)
            print(f"Successfully processed: {link}")

        except requests.RequestException as e:
            print(f"Failed to fetch {link}: {e}")
        except Exception as e:
            print(f"Unexpected error while processing {link}: {e}")

    
    write_configs(filtered_configs)
    print("Configs updated successfully.")


scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_update_configs, "interval", minutes=FETCH_INTERVAL_MINUTES)
scheduler.start()


fetch_and_update_configs()
