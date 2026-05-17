import requests
import time
import json
import os

SETTINGS_FILE = "settings.json"

def load_settings():
    """Load settings from file if it exists"""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return None

def save_settings(token, channel_id, message, interval):
    """Save settings to JSON file"""
    settings = {
        "token": token,
        "channel_id": channel_id,
        "message": message,
        "interval": interval
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)
    print(f"Settings saved to {SETTINGS_FILE}")

def get_input(prompt, current_value=None):
    """Get user input with optional current value shown"""
    if current_value:
        user_input = input(f"{prompt} [{current_value}]: ").strip()
        return user_input if user_input else current_value
    return input(f"{prompt}: ").strip()

# Load existing settings if available
existing_settings = load_settings()

print("=== Discord Auto Messenger Setup ===\n")

# Get settings from user
if existing_settings:
    print("Existing settings found!")
    use_existing = input("Use existing settings? (y/n): ").strip().lower()
    if use_existing == 'y':
        TOKEN = existing_settings['token']
        CHANNEL_ID = existing_settings['channel_id']
        MESSAGE = existing_settings['message']
        INTERVAL = existing_settings['interval']
        print("Using saved settings.")
    else:
        TOKEN = get_input("Enter your token", existing_settings.get('token'))
        CHANNEL_ID = get_input("Enter channel ID", existing_settings.get('channel_id'))
        MESSAGE = get_input("Enter message", existing_settings.get('message'))
        INTERVAL = int(get_input("Enter interval in seconds", existing_settings.get('interval')))
        save_settings(TOKEN, CHANNEL_ID, MESSAGE, INTERVAL)
else:
    TOKEN = get_input("Enter your token")
    CHANNEL_ID = get_input("Enter channel ID")
    MESSAGE = get_input("Enter message")
    INTERVAL = int(get_input("Enter interval in seconds"))
    save_settings(TOKEN, CHANNEL_ID, MESSAGE, INTERVAL)

headers = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

def send_message():
    url = f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages"
    payload = {"content": MESSAGE}
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200 or response.status_code == 201:
        print(f"Sent: {MESSAGE} at {time.strftime('%H:%M:%S')}")
    else:
        print(f"Error {response.status_code}: {response.text}")

print(f"\nStarting Discord Auto Messenger...")
print(f"Channel: {CHANNEL_ID}")
print(f"Message: {MESSAGE}")
print(f"Interval: {INTERVAL} seconds")
print("Press Ctrl+C to stop\n")

try:
    while True:
        send_message()
        time.sleep(INTERVAL)
except KeyboardInterrupt:
    print("\nStopped.")