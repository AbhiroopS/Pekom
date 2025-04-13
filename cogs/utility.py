import os  # noqa: F401
from discord import app_commands
from discord.ext import commands
import discord

import logging

class utility(commands.Cog):
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    @app_commands.command(name='ping', description='Ping the bot')
    async def get(self, interaction: discord.Interaction):
        """Ping the bot."""
        await interaction.response.send_message(f'Pong! {round(interaction.client.latency * 1000)}ms')
        # Log the interaction
        logging.info(f"'ping' Executed by @{interaction.user} in #{interaction.channel} | {interaction.guild}")
        
    @app_commands.command(name='echo', description='Echo a message')
    @app_commands.describe(message='The message to echo')
    # @app_commands.guilds(discord.Object(id=os.getenv("TEST_GUILD_ID")))
    async def echo(self, interaction: discord.Interaction, message: str):
        """Echo a message."""
        await interaction.response.send_message(message)
        # Log the interaction
        logging.info(f"'echo' Executed by @{interaction.user} in #{interaction.channel} | {interaction.guild} | Message: {message}")
        
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(utility(bot))