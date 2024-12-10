from discord import Intents
API_URL = os.getenv("API_URL", "https://csfloat.com/api/v1/listings")
API_TOKEN = os.getenv("API_TOKEN", "")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", "")

# Search parameters
search_parameters = {
    "market_hash_name": "",
    "rarity_name": "",
    "type": "buy_now",
    "min_float": "",
    "max_float": "",
    "rarity": "",
    "paint_seed": "",
    "paint_index": "",
    "user_id": "",
    "collection": "",
    "min_price": "",
    "max_price": "",
}

# Bot intents
intents = Intents.default()
intents.messages = True
intents.message_content = True

# Monitoring frequency
MONITOR_INTERVAL = 3600  # in seconds
