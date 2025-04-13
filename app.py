import os
import logging

import discord
from dotenv import load_dotenv

load_dotenv("./.env")

TOKEN = os.getenv("TOKEN")


class MyClient(discord.Client):
    async def on_ready(self):
        logging.info(f"Logged on as {self.user}")

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == "ping":
            logging.info(f"{message.author} said ping")
            await message.channel.send("pong")


intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)
client.run(TOKEN, root_logger=True)
