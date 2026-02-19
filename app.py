import os
import logging
import asyncio

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv("./.env")

TOKEN = os.getenv("TOKEN")
CLIENT_ID = os.getenv("CLIENT_ID")
OWNER_ID = os.getenv("OWNER_ID")
TEST_GUILD_ID = int(os.getenv("TEST_GUILD_ID"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="p!", intents=intents)

# Usada Pekora quotes and comedic status messages
PEKORA_STATUSES = [
    "Has the don has the don has the don! 🍚",
    "Moshi moshi! Pekora desu yo~! 🐰",
    "Pe~ko~ra~! 💙",
    "Eiii! That's unreasonable! 😤",
    "Pekora pee basu! 🚌",
    "Baaaaka! Are you an idiot?! 😤💢",
    "Un-Union! Strike! ✊",
    "Sore wa chigau yo! That's wrong! ❌",
    "Yare yare daze... 😌",
    "Nandayo! What are you doing! 💥",
    "Watching 24/7 ☕",
    "Not actually a bunny 🐰",
    "Existential crisis.exe 😔",
    "I am become meme 💀",
    "Touch grass. Literally. 🌱",
    "Simping for Pekora since 2020 💙",
    "Nijisanji who? 🤫",
    "Vtubers are my life now 📺",
    "Simp simpson.mp4 🎵",
    "This is fine 🔥",
    "uwu? never. 💢",
    "Reading your messages... 📖",
    "Judging silently 👀",
    "I sleep. I rerun. I win. 💤",
    "Botted since day one 🤖",
    "Pekora harem size: 1 (me) 💙",
    "Cringe is dead. I killed it. 💀",
    "I am speed. 🚀",
    "uwu or die trying ✨",
    "Not sorry. 😊",
    "Running on despair and memes 😔",
    "Hype! Suki! Daisuki! 💖",
    "Yoshi! Let's go! 🎮",
    "Mogu mogu~! 🍪",
    "HAAAAAAAAAAAAAAAAA! 📢",
    "PeKO? No, PeKOrA! 🐰💙",
    "I love you! (platonically) 💕",
    "Let's have a laughing fit!HAHAHA! 😄",
    "Hontou wa iie... (Actually no...) 🙈",
    "Pekora is my sun ☀️",
    "Usada Construction Corp. 🏗️",
    "Don-chan is watching 👁️👄👁️",
]

async def rotate_status():
    """Background task to rotate bot status every 2 minutes."""
    import random
    while True:
        try:
            status = random.choice(PEKORA_STATUSES)
            await bot.change_presence(
                activity=discord.Game(name=status),
                status=discord.Status.online
            )
        except Exception as e:
            logging.error(f"Error rotating status: {e}")
        
        await asyncio.sleep(120)

# ===========================================
# SYNC COMMANDS
# ===========================================

async def sync_to_guild(guild_id: int, clear_first: bool = False):
    """Sync commands to a specific guild."""
    guild = discord.Object(id=guild_id)
    
    if clear_first:
        bot.tree.clear_commands(guild=guild)
    
    bot.tree.copy_global_to(guild=guild)
    synced = await bot.tree.sync()
    return synced

async def sync_global():
    """Sync commands globally (all servers)."""
    synced = await bot.tree.sync()
    return synced

# ===========================================
# SLASH COMMANDS
# ===========================================

@bot.tree.command(name="sync", description="Sync commands to test server (bot owner only)")
async def sync_command(interaction: discord.Interaction, clear: bool = False):
    """Sync commands to the test server."""
    if interaction.user.id != int(OWNER_ID):
        await interaction.response.send_message("❌ No permission.", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    try:
        synced = await sync_to_guild(TEST_GUILD_ID, clear_first=clear)
        await interaction.followup.send(
            f"✅ Synced {len(synced)} commands to test server."
            + (" (cleared first)" if clear else "")
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="promote", description="Promote commands to global (bot owner only)")
async def promote_command(interaction: discord.Interaction):
    """Promote commands from test server to global (all servers)."""
    if interaction.user.id != int(OWNER_ID):
        await interaction.response.send_message("❌ No permission.", ephemeral=True)
        return
    
    await interaction.response.defer()
    
    try:
        # First sync to test server to ensure commands exist
        await sync_to_guild(TEST_GUILD_ID)
        
        # Then promote to global
        synced = await sync_global()
        
        await interaction.followup.send(
            f"✅ Promoted {len(synced)} commands to GLOBAL!\n"
            f"⚠️ Note: Global sync can take up to 1 hour to appear in all servers."
        )
    except Exception as e:
        await interaction.followup.send(f"❌ Error: {e}")

@bot.tree.command(name="botstatus", description="Check bot status")
async def bot_status(interaction: discord.Interaction):
    """Display bot status."""
    embed = discord.Embed(title="🤖 Bot Status", color=discord.Colour.blurple())
    embed.add_field(name="Bot", value=bot.user.name, inline=True)
    embed.add_field(name="Test Server", value=f"`{TEST_GUILD_ID}`", inline=True)
    await interaction.response.send_message(embed=embed)

# ===========================================
# ON_READY
# ===========================================

@bot.event
async def on_ready():
    """Event that runs when the bot is ready."""
    # Load cogs
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            logging.info(f"Loaded {filename[:-3]} cog")
    
    # Sync to test server on startup
    try:
        synced = await sync_to_guild(TEST_GUILD_ID, clear_first=True)
        logging.info(f"Synced {len(synced)} commands to test server")
    except Exception as e:
        logging.error(f"Failed to sync: {e}")
    
    # Start status rotation
    bot.loop.create_task(rotate_status())
    
    logging.info(f"Logged in as {bot.user}")
    logging.info(f"Test server: {TEST_GUILD_ID}")
    logging.info("Bot is ready!")

bot.run(TOKEN, root_logger=True)