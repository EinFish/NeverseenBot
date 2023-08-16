import asyncio
import json
import discord
from discord.ext import commands
from discord import app_commands


class BirthdayCommands(discord.app_commands.Group):

    try:
        with open('birthdays.json', 'r') as file:
            birthdays = json.load(file)
    except FileNotFoundError:
        birthdays = {}

    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        config = {'gratulation_channel': None}

    @app_commands.command(name="setup", description="Erstelle ein Birthday System")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def start(ctx, channel: discord.TextChannel):
        config['gratulation_channel'] = channel.id
        save_data()
        await ctx.send(f'Geburtstagssystem wurde gestartet. Gratulationen werden im Channel {channel.mention} gesendet.')

    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def add(ctx, name, geburtstag):
        birthdays[name] = geburtstag
        save_data()
        await ctx.send(f'Geburtstag von {name} wurde gespeichert.')


    


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




