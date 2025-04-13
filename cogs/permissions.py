from typing import Optional, Union
from discord import app_commands
from discord.ext import commands
# import logging
import discord

class permissions(commands.Cog):
    """Manage permissions of a member."""
    def __init__(self, bot: commands.bot) -> None:
        self.bot = bot

    def get_permissions_embed(self, permissions: discord.Permissions) -> discord.Embed:
        embed = discord.Embed(title='Permissions', colour=discord.Colour.blurple())
        permissions = [
            (name.replace('_', ' ').title(), value)
            for name, value in permissions
        ]

        allowed = [name for name, value in permissions if value]
        denied = [name for name, value in permissions if not value]

        embed.add_field(name='Granted', value='\n'.join(allowed), inline=True)
        embed.add_field(name='Denied', value='\n'.join(denied), inline=True)
        return embed

    @app_commands.command(name='getperms', description='Get permissions of a member or role')
    @app_commands.describe(target='The member or role to get permissions of')
    async def get(self, interaction: discord.Interaction, target: Union[discord.Member, discord.Role]):
        """Get permissions for a member or role"""
        
        if isinstance(target, discord.Member):
            assert target.resolved_permissions is not None
            embed = self.get_permissions_embed(target.resolved_permissions)
            embed.set_author(name=target.display_name, url=target.display_avatar)
        else:
            embed = self.get_permissions_embed(target.permissions)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='getpermschannel', description='Get permissions of a member in a channel')
    @app_commands.describe(channel='The channel to get permissions in')
    @app_commands.describe(member='The member to get permissions of')
    async def _in(
        self, 
        interaction: discord.Interaction, 
        channel: Union[discord.TextChannel, discord.VoiceChannel],
        member: Optional[discord.Member] = None,
    ):
        """Get permissions for you or another member in a specific channel."""
        embed = self.get_permissions_embed(channel.permissions_for(member or interaction.user))
        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(permissions(bot))