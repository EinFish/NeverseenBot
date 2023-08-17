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
import utils

birthdayjson = utils.birthdayinit()
class BirthdayCommands(discord.app_commands.Group):
    
    @app_commands.command(name="setup", description="Erstelle ein Birthday System")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bsetup(self, channel: discord.TextChannel):
        print("dsf")
    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def badd(self, interaction, tag: int, monat: int, jahr: int = None):
        geburtstag = ""
        birthdayjson.bdjson.birthdays[interaction.user.name] = geburtstag
        birthdayjson.save_data()


    @app_commands.command(name="show", description="Zeigt den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bshow(self, member: discord.Member):
        print("dsf")
    @app_commands.command(name="delete", description="Löscht den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bdelete(self, member: discord.Member):
        print("dsf")
    @app_commands.command(name="next", description="Zeigt die nächsten Geburtstage an")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bnext(self, interaction):
        print("dsf")
        
class BirthdayCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        birthdaycmds = BirthdayCommands(name="birthday", description="Befehle des Birthday Systemes")
        self.bot.tree.add_command(birthdaycmds)        
        print("Birthdays Geladen!")


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))