import requests
import config
from database import is_listing_seen, mark_listing_as_seen
from utils import normalize_isoformat, send_discord_notification
from datetime import datetime
import asyncio


async def monitor_listings(bot):
    """Periodically checks for new listings."""
    print("Debug: Entered monitor_listings loop.")
    while True:
        try:
            # Check if market_hash_name is defined
            market_hash_name = config.search_parameters.get("market_hash_name")
            if not market_hash_name:
                print("Debug: Waiting for 'market_hash_name' to be defined...")
                await asyncio.sleep(config.MONITOR_INTERVAL)
                continue

            # Prepare API request
            headers = {"Authorization": config.API_TOKEN}
            params = {k: v for k, v in config.search_parameters.items() if v}
            print(f"Debug: Checking listings with parameters: {params}")
            response = requests.get(config.API_URL, headers=headers, params=params)

            # Handle API errors
            if response.status_code != 200:
                print(f"Debug: API Error: {response.status_code} - {response.text}")
                await asyncio.sleep(config.MONITOR_INTERVAL)
                continue

            # Process listings
            listings = response.json().get("data", [])
            print(f"Debug: Received {len(listings)} listings from API.")

            for listing in listings:
                listing_id = listing.get("id")
                created_at = listing.get("created_at", "")

                if not listing_id or is_listing_seen(listing_id):
                    print(f"Debug: Skipping already seen or invalid listing: {listing_id}")
                    continue

                # Normalize and store listing
                normalized_created_at = normalize_isoformat(created_at.replace("Z", "+00:00"))
                mark_listing_as_seen(listing_id, normalized_created_at)

                # Prepare notification
                item_name = listing.get("item", {}).get("market_hash_name", "Unknown Item")
                price = listing.get("price", 0) / 100.0
                inspect_link = listing.get("item", {}).get("inspect_link", "No link available")
                item_id = listing.get("id", "Unknown ID")  # Fetch the item ID
                csfloat_link = f"https://csfloat.com/item/{item_id}"  # Construct the link

                message = (
                    f"**New Listing Found:**\n"
                    f"**Item Name:** {item_name}\n"
                    f"**Price:** ${price:.2f}\n"
                    f"**Created At:** {normalized_created_at}\n"
                    f"**Inspect Link:** {inspect_link}\n"
                    f"**CSFloat Link:** [View Item]({csfloat_link})"
                )

                # Send Discord notification
                print(f"New listing detected: {message}")
                send_discord_notification(message)

        except Exception as e:
            print(f"Debug: Error in monitor_listings: {e}")

        # Wait for the next check
        print(f"Debug: Sleeping for {config.MONITOR_INTERVAL} seconds...")
        await asyncio.sleep(config.MONITOR_INTERVAL)
