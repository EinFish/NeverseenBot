import asyncio
import json
from typing import Any, Dict, List, Optional, Union
import discord
import datetime

from discord.app_commands.commands import Group
from discord.app_commands.translator import locale_str
from discord.ext import commands, tasks
from discord import app_commands
from discord.permissions import Permissions
from discord.utils import MISSING
import time
import utils

errormessage = utils.errordcmessage


class BirthdayCommands(discord.app_commands.Group):

    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def badd(self, interaction, tag: app_commands.Range[int, 1, 31], monat: app_commands.Range[int, 1, 12], jahr: app_commands.Range[int, 1960, 2020] = 1600):
        with open("users.json") as file:
            bjson = json.load(file)
        await interaction.response.defer()
        userid = interaction.user.id

        try:
            warns = bjson[str(userid)]["warns"]
        except KeyError:
            warns = 0
        try:

            daten = ""
            if not jahr == None:
                today = datetime.date.today()
                date = datetime.date(jahr, monat, tag)
                date2 = str(date)
                daten = date2.split("-")
                bday = date.strftime("%d/%m/%Y")
                bjson[str(userid)] = {"bday": bday, "warns": warns}

            else:
                today = datetime.date.today()
                date = datetime.date(jahr, monat, tag)
                date2 = str(date)
                daten = date2.split("-")
                bday = date.strftime("%d/%m/Y")
                bjson[str(userid)] = {"bday": bday, "warns": warns}

            with open("users.json", 'w') as json_file:
                json.dump(bjson, json_file, indent=4)

            if jahr == 1600:
                embed = discord.Embed(title="Geburtstag eingetragen!",
                                      description=f"Dein Geburtstag wurde erfolgreich auf den `{daten[2]}.{daten[1]}.` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)
            else:
                embed = discord.Embed(title="Geburtstag eingetragen!",
                                      description=f"Dein Geburtstag wurde erfolgreich auf den `{daten[2]}.{daten[1]}.{daten[0]}` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)

            await interaction.followup.send(embed=embed)
        except ValueError:
            await interaction.followup.send(content="Bitte gebe ein richtiges Datum ein.")
        except Exception as error:
            await errormessage(interaction=interaction, error=error)

    @app_commands.command(name="show", description="Zeigt den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bshow(self, interaction, member: discord.Member = None):
        with open("users.json") as file:
            bjson = json.load(file)

        await interaction.response.defer()

        try:
            id = interaction.user.id
            if member == None:
                userid = str(id)
                user1 = interaction.user
            else:
                userid = str(member.id)
                user1 = member
            """ with open("users.json") as file:
                bjson = json.load(file) """

            bdaystr = bjson[userid]['bday']
            bdaylist = bdaystr.split("/")

            # checking the user and birthday, to display the data.
            if member != None:
                if bdaylist[2] == "1600":
                    embed = discord.Embed(
                        title=f"Geburtstag von {user1.display_name}", description=f"Der User {user1.mention} hat am `{bdaylist[0]}.{bdaylist[1]}` Geburtstag.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"Geburtstag von {user1.display_name}", description=f"Der User {user1.mention} hat am `{bdaylist[0]}.{bdaylist[1]}` Geburtstag und ist im Jahr `{bdaylist[2]}` geboren.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)

            else:
                if bdaylist[2] == "1600":
                    embed = discord.Embed(
                        title=f"Geburtstag von {user1.display_name}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` Geburtstag.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"Geburtstag von {user1.display_name}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` Geburtstag und bist im Jahr `{bdaylist[2]}` geboren.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)
        except KeyError:
            if member == None:
                embed = discord.Embed(
                    title=f"Fehler", description=f"Es gab einen Fehler beim Anzeigen des Geburtstages von {interaction.user.mention}.", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(
                    name="Grund:", value=f"{interaction.user.mention} hat keinen Geburtstag eingetragen.")

            if member != None:
                embed = discord.Embed(
                    title=f"Fehler", description=f"Es gab einen Fehler beim Anzeigen des Geburtstages von {member.mention}.", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(
                    name="Grund:", value=f"{member.mention} hat keinen Geburtstag eingetragen.")

            await interaction.followup.send(embed=embed)

    @app_commands.command(name="delete", description="Löscht den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bdelete(self, interaction, member: discord.Member = None):
        with open("users.json") as file:
            bjson = json.load(file)

        try:

            id = interaction.user.id
            id2 = str(id)

            if member != None:
                userid = str(member.id)
                if member.id == interaction.user.id:
                    await interaction.response.defer()
                    del bjson[id2]["bday"]
                    embed = discord.Embed(title=f"Geburtstag gelöscht", description=f"Du hast deinen Geburtstag gelöscht.",
                                          timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)

                elif interaction.user.guild_permissions.kick_members:
                    await interaction.response.defer()
                    id3 = str(userid)
                    del bjson[id3]["bday"]
                    embed = discord.Embed(title=f"Geburtstag von {member.display_name} gelöscht",
                                          description=f"Der Geburtstag von {member.display_name} wurde gelöscht.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)

                else:
                    await interaction.response.send_message(content=f"Du hast keine Berechtigung, andere Geburtsdaten zu löschen.", ephemeral=True)
            else:
                await interaction.response.defer()
                del bjson[id2]["bday"]
                embed = discord.Embed(title=f"Geburtstag gelöscht", description=f"Du hast deinen Geburtstag gelöscht.",
                                      timestamp=datetime.datetime.now(), color=0x0094ff)

                await interaction.followup.send(embed=embed)

            with open("users.json", 'w') as json_file:
                json.dump(bjson, json_file, indent=4)

        except KeyError:
            if member == None:
                embed = discord.Embed(
                    title=f"Fehler", description=f"Es gab einen Fehler beim Löschen des Geburtstages von {interaction.user.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(
                    name="Grund:", value=f"{interaction.user.mention} hat keinen Geburtstag eingetragen")

            elif member != None:
                embed = discord.Embed(
                    title=f"Fehler", description=f"Es gab einen Fehler beim Löschen des Geburtstages von {member.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(
                    name="Grund:", value=f"{member.mention} hat keinen Geburtstag eingetragen")

            await interaction.followup.send(embed=embed)

    @app_commands.command(name="next", description="Zeigt die nächsten Geburtstage an")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def birthday(self, ctx):
        with open("users.json") as file:
            bjson = json.load(file)
        await ctx.response.defer()

        def divideListInChunks(list, chunkSize):
            for i in range(0, len(list), chunkSize):
                yield list[i:i + chunkSize]

        # mit 'members = [member.id for member in ctx.guild.members]' austauschen
        memberlist = [member.id for member in ctx.guild.members]

        jsonData = bjson  # Daten aus JSON laden

        users = list(jsonData)  # Ein Array mit UserIDs aus der JSON machen
        maxBDaysPerPage = 2  # Die Maximalen Geburtstage die pro Seite angezeigt werden sollen

        currentPage = 0  # Die Aktuelle Seite

        daytoday = datetime.datetime.now().strftime("%d")  # Heutiger Tag
        monthtoday = datetime.datetime.now().strftime("%m")  # Heutiger Monat
        yeartoday = datetime.datetime.now().strftime("%Y")  # Heutiges Jahr

        parsedBirthdays = []  # Geburtstage als ein bestimmtes Format

        for user in users:
            try:
                if int(user) in memberlist:  # ids sind strings, deshalb in int umwandeln
                    mention = f"<@{user}>"
                    birthday = jsonData[user]["bday"]
                    day = birthday.split("/")[0]
                    month = birthday.split("/")[1]
                    rawYear = birthday.split("/")[2]
                    # Monat war noch nicht -> Geburtstag war noch nicht
                    if int(month) > int(monthtoday):
                        year = int(yeartoday)
                    # Monat ist heute aber Tag war noch nicht -> Geburtstag war noch nicht
                    elif int(month) == int(monthtoday) and int(day) >= int(daytoday):
                        year = int(yeartoday)
                    else:  # Geburtstag war schon
                        year = int(yeartoday) + 1

                    date_obj = datetime.datetime.strptime(
                        f"{month}-{day}-{year}", "%m-%d-%Y")

                    birthdayParsed = {}
                    birthdayParsed["inDays"] = (
                        date_obj - datetime.datetime.now()).days
                    birthdayParsed["showAge"] = rawYear != "1600"
                    birthdayParsed["newAge"] = year - int(rawYear)
                    birthdayParsed["user"] = user
                    birthdayParsed["timestamp"] = int(time.time(
                    )) + birthdayParsed["inDays"] * 86400 + 86400  # Für discord time formating
                    parsedBirthdays.append(birthdayParsed)

            except KeyError:
                pass

        sortedBirthdays = sorted(parsedBirthdays, key=lambda x: x['inDays'])

        chunkedBirthdays = [_ for _ in divideListInChunks(
            sortedBirthdays, maxBDaysPerPage)]

        def generatePageContent():
            text = ""
            for birthday in chunkedBirthdays[currentPage]:
                if birthday['inDays'] == -1:
                    string = "Heute"
                else:
                    string = f" <t:{birthday['timestamp']}:R>"
                if birthday['showAge']:
                    text += f"<@{birthday['user']}> ({birthday['newAge']}. Geburtstag) - <t:{birthday['timestamp']}:D> {string}\n"
                else:
                    text += f"<@{birthday['user']}> - <t:{birthday['timestamp']}:D> {string}\n"
            return text

        async def nextPage(interaction):
            nonlocal currentPage
            currentPage += 1
            if currentPage == len(chunkedBirthdays):
                currentPage = 0
            await updateEmbed(interaction)

        async def beforePage(interaction):
            nonlocal currentPage
            currentPage -= 1
            if currentPage == -1:
                currentPage = len(chunkedBirthdays) - 1
            await updateEmbed(interaction)

        def getEmbed():
            if currentPage == 0:
                a = 1
            elif currentPage != 0:
                a = currentPage
                a += 1
            embed = discord.Embed(title=f"Die nächsten Geburtstage | Seite {a}", description=generatePageContent(
            ), color=0x0094ff, timestamp=datetime.datetime.now())
            return embed

        async def updateEmbed(interaction):
            embed = getEmbed()
            await interaction.response.edit_message(embed=embed)

        embed = getEmbed()
        view = discord.ui.View()
        if len(chunkedBirthdays) > 1:
            prevpagebtn = discord.ui.Button(label="⏪")
            prevpagebtn.callback = beforePage
            nextpagebtn = discord.ui.Button(label="⏩")
            nextpagebtn.callback = nextPage
            view.add_item(prevpagebtn)
            view.add_item(nextpagebtn)

        await ctx.followup.send(embed=embed, view=view)


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
