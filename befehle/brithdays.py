import asyncio
from typing import Any, Dict, List, Optional, Union
import discord
from discord.app_commands.commands import Group
from discord.app_commands.translator import locale_str
from discord.ext import commands, tasks
from discord import app_commands
import datetime
import json

from discord.permissions import Permissions
from discord.utils import MISSING


class Birthdays(discord.app_commands.Group):


    def __init__(self):
        super().__init__()
# Lade bereits gespeicherte Geburtstage aus einer JSON-Datei
try:
    with open('birthdays.json', 'r') as file:
        birthdays = json.load(file)
except FileNotFoundError:
    birthdays = {}

# ID des Channels, in dem Geburtstagsnachrichten gesendet werden sollen
        

    @tasks.loop(hours=12)  # Überprüfe alle 12 Stunden die Geburtstage
    async def birthday_check(self, member, guild):
        channel = 1086608126985375785
        today = datetime.datetime.now().strftime('%d/%m')
        
        for user_id, date in birthdays.items():
            if date == today:
                member = guild.get_user(int(user_id))
                if member:
                    await channel.send(f'Herzliche Glückwünsche zum Geburtstag, {member.mention}! 🎉🎂')

    @app_commands.command(name="set", description="Lege einen Geburtstag fest.")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def set_birthday(ctx, date: str):
        """Setze deinen Geburtstag im Format TT/MM."""
        birthdays[str(ctx.author.id)] = date
        with open('birthdays.json', 'w') as file:
            json.dump(birthdays, file)
        await ctx.send(f'Dein Geburtstag wurde auf den {date} gesetzt.')

    @app_commands.command(name="get", description="Gucke wann ein Nutzer geburtstag hat.")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def get_birthday(ctx, member: discord.Member = None):
        """Zeige den Geburtstag eines Mitglieds oder deinen eigenen Geburtstag an."""
        if not member:
            member = ctx.author

        if str(member.id) in birthdays:
            await ctx.send(f'{member.name}\'s Geburtstag ist am {birthdays[str(member.id)]}.')
        else:
            await ctx.send(f'Ich habe keinen Geburtstag für {member.name} gefunden.')

    @app_commands.command(name="remove", description="Lass mich dein geburtstag vergessen.")
    async def remove_birthday(ctx):
        """Entferne deinen gespeicherten Geburtstag."""
        if str(ctx.author.id) in birthdays:
            del birthdays[str(ctx.author.id)]
            with open('birthdays.json', 'w') as file:
                json.dump(birthdays, file)
            await ctx.send('Dein gespeicherter Geburtstag wurde entfernt.')
        else:
            await ctx.send('Ich habe keinen gespeicherten Geburtstag für dich gefunden.')



    @app_commands.command(name="next", description="Zeigt die nächsten geburtstage")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def next_birthday( ctx):
        """Zeige die nächsten 10 Geburtstage an."""
        sorted_birthdays = sorted(birthdays.items(), key=lambda x: datetime.datetime.strptime(x[1], '%d/%m'))
        message = "Nächste Geburtstage:\n"
        
        for i, (user_id, date) in enumerate(sorted_birthdays[:10], start=1):
            member = ctx.get_user(int(user_id))
            message += f"{i}. {member.name if member else 'Nutzer'} am {date}\n"

        await ctx.send(message)



class BirthdayCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        bdcmds = Birthdays(name="birthday", description="Befehle des Birthday Systemes")
        self.bot.tree.add_command(bdcmds)
        birthday_check.start()
        print("Birthdyas geladen!")


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))

