import asyncio
import json
from typing import Any, Dict, List, Optional, Union
import discord
from discord.app_commands.commands import Group
from discord.app_commands.translator import locale_str
from discord.ext import commands
from discord import app_commands
from discord.permissions import Permissions
from discord.utils import MISSING


class BirthdayCommands(discord.app_commands.Group):
    def __init__(self):
        try:
            with open('birthdays.json', 'r') as file:
                birthdays = json.load(file)
        except FileNotFoundError:
            birthdays = {}

        try:
            with open('config.json', 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {'gratulation_channel': None}

    @app_commands.command(name="setup", description="Erstelle ein Birthday System")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def start(self, ctx, channel: discord.TextChannel):
        self.config['gratulation_channel'] = channel.id
        save_data()
        await ctx.send(f'Geburtstagssystem wurde gestartet. Gratulationen werden im Channel {channel.mention} gesendet.')

    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def add(context, name, geburtstag):
        birthdays[name] = geburtstag
        save_data()
        await context.send(f'Geburtstag von {name} wurde gespeichert.')


    


class Birthday(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bdcmds = BirthdayCommands(name="birthday", description="Das Geburtstagssystem")
        self.bot.tree.add_command(bdcmds)
        print("Birthdays geladen!")



async def setup(bot):
    await bot.add_cog(Birthday(bot))




