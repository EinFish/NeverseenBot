import asyncio
import json
from typing import Any, Dict, List, Optional, Union
import discord
import datetime
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
    async def bsetup(self, interaction, birthdaychannel: discord.TextChannel):
        await interaction.response.defer()
        guildid = interaction.guild.id
        guildname = interaction.guild.name
        channelid = birthdaychannel.id
        with open("serverconfig.json") as file:
            bjson = json.load(file)
            bjson[str(guildid)] = {"name": guildname, "bday": channelid}

            print(bjson)

            with open("serverconfig.json", 'w') as json_file:
                json.dump(bjson, json_file, indent=4)

            await interaction.followup.send(f"Birthday Channel gesetzt zu {birthdaychannel}")

    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def badd(self, interaction, tag: int, monat: int, jahr: int = None):
        userid = interaction.user.id
        with open("birthdays.json") as file:
            bjson = json.load(file)
            date_format = "%d/%m/%Y"
            date_format2 = "%d/%m"
            if not jahr == None:
                today = datetime.datetime.now()
                bday = datetime.datetime.strptime(
                    f"{monat}/{tag}/{jahr}", date_format)
                diff = bday - today
                diff.days
                print(bday)
                ts = datetime.datetime.timestamp(bday)
                print(type(bday))
                print(diff)
                bjson[str(userid)] = {"bday": ts}
                print(bjson)
            else:
                today = datetime.datetime.now()
                bday = datetime.datetime.strptime(
                    f"{monat}/{tag}", date_format2)
                diff = bday - today
                diff.days
                print(bday)
                ts = datetime.datetime.timestamp(bday)
                print(type(bday))
                print(diff)
                bjson[str(userid)] = {"bday": ts}
                print(bjson)

                with open("serverconfig.json", 'w') as json_file:
                    json.dump(bjson, json_file, indent=4)

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
        birthdaycmds = BirthdayCommands(
            name="birthday", description="Befehle des Birthday Systemes")
        self.bot.tree.add_command(birthdaycmds)
        print("Birthdays Geladen!")


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
