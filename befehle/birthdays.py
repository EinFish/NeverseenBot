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
            with open("serverconfig.json", 'w') as json_file:
                json.dump(bjson, json_file, indent=4)

            await interaction.followup.send(f"Birthday Channel gesetzt auf {birthdaychannel.mention}")

    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def badd(self, interaction, tag: int, monat: int, jahr: int = 1600):
        await interaction.response.defer()
        userid = interaction.user.id
        with open("birthdays.json") as file:
            bjson = json.load(file)
            if not jahr == None:
                today = datetime.date.today()
                date = datetime.date(jahr, monat, tag)
                print(date)
                print(today)
                bday = date.strftime("%d/%m/%Y")
                bjson[str(userid)] = {"bday": bday}
            else:
                today = datetime.date.today()
                date = datetime.date(jahr, monat, tag)
                date2 = date.split("-")
                print(date)
                print(today)
                bday = date.strftime("%d/%m/Y")
                bjson[str(userid)] = {"bday": bday}

            with open("birthdays.json", 'w') as json_file:
                json.dump(bjson, json_file, indent=4)

        if jahr == 1600:
            embed = discord.Embed(title="Geburtstag eingetragen!", description=f"Dein geburtstag wurde erfolgreich auf den `{tag}.{monat}.` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)
        else:
            embed = discord.Embed(title="Geburtstag eingetragen!", description=f"Dein geburtstag wurde erfolgreich auf den `{tag}.{monat}.{jahr}` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)

        await interaction.followup.send(embed=embed)


    @app_commands.command(name="show", description="Zeigt den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bshow(self, interaction, member: discord.Member = None):
        await interaction.response.defer()
        id = interaction.user.id
        if member == None:
            userid = str(id)
            user1 = interaction.user
        else:
            userid = str(member.id)
            user1 = member
        with open("birthdays.json") as file:
            bjson = json.load(file)


        bdaystr = bjson[userid]['bday']
        bdaylist = bdaystr.split("/")
        print(bdaylist[0])

        # checking the user and birthday, to display the data.
        if member != None:
            if bdaylist[2] == "1600":
                embed = discord.Embed(title=f"Geburtstag von {user1.display_name}", description=f"Der User {user1.mention} hat am `{bdaylist[0]}.{bdaylist[1]}` geburtstag.", timestamp=datetime.datetime.now(), color=0x0094ff)
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(title=f"Geburtstag von {user1.display_name}", description=f"Der User {user1.mention} hat am `{bdaylist[0]}.{bdaylist[1]}` geburtstag und ist im Jahr `{bdaylist[2]}` geboren.", timestamp=datetime.datetime.now(), color=0x0094ff)
                await interaction.followup.send(embed=embed)

        else:
            if bdaylist[2] == "1600":
                embed = discord.Embed(title=f"Geburtstag von {user1}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` geburtstag ", timestamp=datetime.datetime.now(), color=0x0094ff)
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(title=f"Geburtstag von {user1.display_name}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` geburtstag und bist im Jahr `{bdaylist[2]}` geboren.", timestamp=datetime.datetime.now(), color=0x0094ff)
                await interaction.followup.send(embed=embed)


        

        

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
