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


    def save_data(self):
        with open('birthdays.json', 'w') as file:
            json.dump(self.birthdays, file, indent=4)
        with open('config.json', 'w') as file:
            json.dump(self.config, file, indent=4)


@app_commands.command(name="setup", description="Erstelle ein Birthday System")
@commands.cooldown(1, 20, commands.BucketType.user)
async def bsetup(self, ctx, channel: discord.TextChannel):
    self.config['gratulation_channel'] = channel.id
    self.save_data()
    await ctx.send(f'Geburtstagssystem wurde gestartet. Gratulationen werden im Channel {channel.mention} gesendet.')

@app_commands.command(name="hinzu", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
@commands.cooldown(1, 20, commands.BucketType.user)
async def badd(self, name, geburtstag):
    self.birthdays[name] = geburtstag
    self.save_data()
    await self.bot.interaction.send(f'Geburtstag von {name} wurde gespeichert.')

@app_commands.command(name="show", description="Zeigt den Geburtstag von einem Member")
@commands.cooldown(1, 20, commands.BucketType.user)
async def bshow(self, ctx, name, member: discord.Member = discord.Interaction.user.name):
    if member in self.birthdays:
        await ctx.send(f'{name} hat am {self.birthdays[name]} Geburtstag.')
    else:
        await ctx.send(f'Kein Geburtstag für {name} gefunden.')

@app_commands.command(name="delete", description="Löscht den Geburtstag von einem Member")
@commands.cooldown(1, 20, commands.BucketType.user)
async def bdelete(self, ctx, name,  member: discord.Member = discord.Interaction.user.name):
    if name in self.birthdays:
        del self.birthdays[name]
        self.save_data()
        await ctx.send(f'Geburtstag von {name} wurde gelöscht.')
    else:
        await ctx.send(f'Kein Geburtstag für {name} gefunden.')

@app_commands.command(name="next", description="Zeigt die nächsten Geburtstage an")
@commands.cooldown(1, 20, commands.BucketType.user)
async def bnext(self, ctx):
    if len(self.birthdays) == 0:
        await ctx.send('Keine Geburtstage gespeichert.')
    else:
        result = 'Gespeicherte Geburtstage:\n'
        for name, geburtstag in self.birthdays.items():
            result += f'{name}: {geburtstag}\n'
        await ctx.send(result)

 

    
class BirthdayCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bdcmds = BirthdayCommands(name="birthday", description="Das Geburtstagssystem")
        self.bot.tree.add_command(bdcmds)
        print("Birthdays geladen!")



async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))




