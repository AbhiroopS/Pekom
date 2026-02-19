from discord import app_commands
from discord.ext import commands
import discord

import logging
import os
import aiohttp
from datetime import datetime

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
    
    async def _call_openrouter(self, messages_text: str) -> str:
        """Call OpenRouter API to generate a comedic summary."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        
        if not api_key or api_key == "sk-yourkeyhere":
            raise ValueError("OpenRouter API key not configured")
        
        prompt = f"""You are a hilariously unhinged Discord bot tasked with summarizing channel conversations. 
Read the following messages and create a comedic recap with your own slightly chaotic commentary in the format of a news report.

Your summary should include:
- A dramatic/funny intro
- Key statistics about the conversation (message count, most active users, etc.)
- Unhinged observations about conversation patterns
- Random out-of-context highlights
- A sarcastic closing thought

Be witty, sarcastic, and entertaining. Use emojis. Don't hold back on the comedy.

Messages to summarize:
{messages_text}

Generate the comedic summary now:"""

        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://github.com/AbhiroopS/Pekom",
                    "X-Title": "Pekom Discord Bot"
                },
                json={
                    "model": "anthropic/claude-3.5-sonnet",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.9
                }
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise Exception(f"OpenRouter API error: {response.status} - {error_text}")
                
                data = await response.json()
                return data["choices"][0]["message"]["content"]
    
    @app_commands.command(name='summarize', description='Get an AI-generated comedic recap of recent messages')
    @app_commands.describe(count='Number of messages to analyze (default: 200, max: 500)')
    async def summarize(self, interaction: discord.Interaction, count: int = 200):
        """Generate an AI-powered comedic summary of recent channel messages."""
        
        # Check if user is allowed to use this command
        allowed_users = os.getenv("ALLOWED_SUMMARIZE_USERS", "").split(",")
        if str(interaction.user.id) not in allowed_users:
            await interaction.response.send_message(
                "❌ You don't have permission to use this command. This is an exclusive club. 💅",
                ephemeral=True
            )
            logging.warning(f"'summarize' Denied for @{interaction.user} (ID: {interaction.user.id})")
            return
        
        # Validate count
        if count < 10:
            await interaction.response.send_message("❌ Please analyze at least 10 messages.", ephemeral=True)
            return
        if count > 500:
            await interaction.response.send_message("❌ Maximum 500 messages allowed.", ephemeral=True)
            return
        
        await interaction.response.defer()  # This might take a while
        
        try:
            # Fetch the messages
            messages = []
            async for message in interaction.channel.history(limit=count):
                if not message.author.bot:  # Skip bot messages
                    messages.append(message)
            
            if len(messages) == 0:
                await interaction.followup.send("There's literally nothing to summarize. This channel is a ghost town. 👻")
                logging.info(f"'summarize' Executed by @{interaction.user} in #{interaction.channel} | {interaction.guild} | No messages found")
                return
            
            # Format messages for the LLM
            messages_text = "\n\n".join([
                f"[{msg.created_at.strftime('%Y-%m-%d %H:%M')}] {msg.author.name}: {msg.content[:500]}"
                for msg in reversed(messages[-100:])  # Send last 100 messages to avoid token limits
            ])
            
            # Call OpenRouter API
            try:
                summary = await self._call_openrouter(messages_text)
            except ValueError as e:
                await interaction.followup.send(
                    "⚠️ OpenRouter API key not configured. Please set OPENROUTER_API_KEY in .env file."
                )
                logging.error(f"'summarize' Failed - {e}")
                return
            except Exception as e:
                await interaction.followup.send(
                    f"❌ Failed to generate summary from OpenRouter API. Error: {str(e)[:100]}"
                )
                logging.error(f"'summarize' OpenRouter API Error: {e}")
                return
            
            # Add metadata footer
            summary += f"\n\n*📊 Analyzed {len(messages)} messages from the last {count} in the channel*"
            
            # Send the summary (split if too long)
            if len(summary) > 2000:
                # Split into chunks
                chunks = [summary[i:i+2000] for i in range(0, len(summary), 2000)]
                for chunk in chunks:
                    await interaction.followup.send(chunk)
            else:
                await interaction.followup.send(summary)
            
            logging.info(f"'summarize' Executed by @{interaction.user} in #{interaction.channel} | {interaction.guild} | Analyzed {len(messages)} messages")
            
        except discord.Forbidden:
            await interaction.followup.send("I don't have permission to read message history. Literally 1984. 😔")
            logging.error(f"'summarize' Failed - Missing permissions in #{interaction.channel}")
        except Exception as e:
            await interaction.followup.send(f"Something went horribly wrong. The chaos was too much even for me. 💥")
            logging.error(f"'summarize' Error: {e}")
        
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(utility(bot))
