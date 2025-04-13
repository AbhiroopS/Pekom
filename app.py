import os
import logging

import discord
from discord import app_commands

from dotenv import load_dotenv

load_dotenv("./.env")

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True


class MyClient(discord.Client):
    async def on_ready(self):
        await tree.sync()
        logging.info(f"Logged on as {self.user}")

client = MyClient(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(
    name="ping",
    description="Ping the bot",
)
async def ping(interaction):
    await interaction.response.send_message("pong!")
    logging.info(f"'ping' Executed by @{interaction.user} in #{interaction.channel} | {interaction.guild}")



client.run(TOKEN, root_logger=True)