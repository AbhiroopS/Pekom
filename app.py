import os
import logging

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv("./.env")

TOKEN = os.getenv("TOKEN")
TEST_GUILD_ID = os.getenv("TEST_GUILD_ID")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="p!", intents=intents)

@bot.event
async def on_ready():
    """Event that runs when the bot is ready."""
    try:
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                logging.info(f"Loaded {filename[:-3]} cog")
        logging.info("All cogs loaded successfully.")
        
        synced = await bot.tree.sync(guild=discord.Object(id=TEST_GUILD_ID))
        logging.info(f"Synced {len(synced)} commands to Test Guild.")
        # synced = await bot.tree.sync()
        # logging.info(f"Synced {len(synced)} commands globally.")
        
    except Exception as e:
        logging.error(f"Failed to sync commands: {e}")
    logging.info(f"Logged in as {bot.user}")
    logging.info(f"User ID: {bot.user.id}")
    logging.info("Bot is ready.")
    

bot.run(TOKEN, root_logger=True)