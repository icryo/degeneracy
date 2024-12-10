from urllib.parse import quote
from datetime import datetime
import requests
import config

def normalize_isoformat(iso_string):
    """Normalize an ISO 8601 string to ensure compatibility with fromisoformat."""
    if 'Z' in iso_string:
        iso_string = iso_string.replace("Z", "+00:00")
    if '.' in iso_string:
        parts = iso_string.split('.')
        parts[1] = (parts[1] + "000000")[:6]  # Pad fractional seconds to six digits
        iso_string = '.'.join(parts)
    return iso_string

def send_discord_notification(content):
    """Send a notification to Discord."""
    try:
        webhook_url = config.DISCORD_WEBHOOK_URL
        response = requests.post(webhook_url, json={"content": content})
        if response.status_code != 200:
            print(f"Failed to send Discord notification: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error sending Discord notification: {e}")
