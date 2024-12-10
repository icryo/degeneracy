from discord.ext import commands
import config
from commands import setup_commands
from monitor import monitor_listings
import asyncio
from database import initialize_db

initialize_db()

bot = commands.Bot(command_prefix="!", intents=config.intents)

@bot.event
async def on_ready():
    print(f"Bot is ready. Logged in as {bot.user}")
    asyncio.create_task(monitor_listings(bot))

print("Setting up commands...")
setup_commands(bot)

if __name__ == "__main__":
    bot.run(config.DISCORD_BOT_TOKEN)
