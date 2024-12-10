import config
from discord.ext import commands
import requests
from database import is_listing_seen
from utils import normalize_isoformat
import asyncio 
from monitor import monitor_listings

monitor_task = None


def setup_commands(bot):
    """Attach commands to the bot."""
    print("Debug: Setting up commands...")
    print(f"Existing commands before setup: {[cmd.name for cmd in bot.commands]}")

    # Remove existing commands
    for cmd_name in ["set_var", "set_frequency", "bot_help", "check", "all", "go"]:
        if bot.get_command(cmd_name):
            print(f"Removing command: {cmd_name}")
            bot.remove_command(cmd_name)

    # Define commands
    @bot.command()
    async def set_var(ctx, parameter: str, *, value: str):
        """Update any search parameter dynamically."""
        if parameter in config.search_parameters:
            config.search_parameters[parameter] = value
            print(f"Updated `search_parameters`: {config.search_parameters}")
            await ctx.send(f"{ctx.author.mention} Parameter `{parameter}` updated to: `{value}`")
        else:
            await ctx.send(f"{ctx.author.mention} Invalid parameter: `{parameter}`")

    @bot.command()
    async def go(ctx):
        """Manually start the monitoring process."""
        print("Debug: !go command triggered.")
        
        # Ensure market_hash_name is defined
        if not config.search_parameters.get("market_hash_name"):
            await ctx.send(f"{ctx.author.mention} Please define `market_hash_name` with `!set_var` before starting monitoring.")
            print("Debug: market_hash_name not defined.")
            return

        # Check if monitoring is already running
        if hasattr(bot, "monitoring_task") and bot.monitoring_task:
            if not bot.monitoring_task.done():
                await ctx.send(f"{ctx.author.mention} Monitoring is already running.")
                print("Debug: Monitoring is already running.")
                return
            else:
                # Reset the task if it's completed or cancelled
                bot.monitoring_task = None

        try:
            print("Debug: Starting monitoring task...")
            bot.monitoring_task = asyncio.create_task(monitor_listings(bot))
            await ctx.send(f"{ctx.author.mention} Monitoring started.")
        except Exception as e:
            print(f"Debug: Error starting monitoring: {e}")
            await ctx.send(f"{ctx.author.mention} Failed to start monitoring: {e}")


    @bot.command()
    async def set_frequency(ctx, seconds: int):
        """Update the monitoring frequency dynamically."""
        if seconds < 10:
            await ctx.send(f"{ctx.author.mention} Frequency too low! Minimum is 10 seconds.")
            return
        config.MONITOR_INTERVAL = seconds
        print(f"Debug: Monitoring frequency updated to {seconds} seconds.")
        print(config.MONITOR_INTERVAL)
        await ctx.send(f"{ctx.author.mention} Monitoring frequency updated to {seconds} seconds.")

    @bot.command()
    async def stop(ctx):
        """Stop the monitoring process."""
        if hasattr(bot, "monitoring_task") and bot.monitoring_task:
            if not bot.monitoring_task.done():
                bot.monitoring_task.cancel()
                await ctx.send(f"{ctx.author.mention} Monitoring stopped.")
                print("Debug: Monitoring stopped.")
            else:
                print("Debug: Monitoring task was already completed.")
        else:
            print("Debug: No active monitoring task found.")
        # Clear the task reference
        bot.monitoring_task = None

        
        # Reset search parameters
        config.search_parameters = {
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
        print("Search parameters reset.")
        await ctx.send(f"{ctx.author.mention} Search parameters have been reset.")

    @bot.command()
    async def bot_help(ctx):
        """List all available commands."""
        commands_list = (
            "**Commands:**\n"
            "`!set_var <parameter> <value>` - Update a search parameter.\n"
            "`!set_frequency <seconds>` - Set the frequency for listing checks.\n"
            "`!go` - Start monitoring for listings.\n"
            "`!check` - Manually trigger a listing check.\n"
            "`!all` - Fetch all listings.\n"
            "`!bot_help` - Show this help message.\n"
        )
        await ctx.send(f"{ctx.author.mention} {commands_list}")

    @bot.command()
    async def check(ctx):
        """Manually trigger a listing check."""
        await ctx.send(f"{ctx.author.mention} Sending manual check request...")
        # Insert logic for manual check here.

    @bot.command()
    async def all(ctx):
        """List all items from the API response, regardless of when posted."""
        await ctx.send(f"{ctx.author.mention} Fetching all available listings...")
        # Insert logic for fetching all listings here.

    print(f"Commands after setup: {[cmd.name for cmd in bot.commands]}")
