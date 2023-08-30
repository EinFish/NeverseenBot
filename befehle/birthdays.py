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


with open("serverconfig.json") as file:
    sjson = json.load(file)

with open("users.json") as file:
    bjson = json.load(file)

with open('reactions.json') as file:
    rjson = json.load(file)


class BirthdayCommands(discord.app_commands.Group):

    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def badd(self, interaction, tag: app_commands.Range[int, 1, 31], monat: app_commands.Range[int, 1, 12], jahr: app_commands.Range[int, 1960, 2020] = 1600):
        await interaction.response.defer()
        userid = interaction.user.id
        try:

            daten = ""
            if not jahr == None:
                today = datetime.date.today()
                date = datetime.date(jahr, monat, tag)
                date2 = str(date)
                daten = date2.split("-")
                bday = date.strftime("%d/%m/%Y")
                bjson[str(userid)] = {"bday": bday}

            else:
                today = datetime.date.today()
                date = datetime.date(jahr, monat, tag)
                date2 = str(date)
                daten = date2.split("-")
                bday = date.strftime("%d/%m/Y")
                bjson[str(userid)] = {"bday": bday}

            with open("users.json", 'w') as json_file:
                json.dump(bjson, json_file, indent=4)

            if jahr == 1600:
                embed = discord.Embed(title="Geburtstag eingetragen!",
                                      description=f"Dein geburtstag wurde erfolgreich auf den `{daten[2]}.{daten[1]}.` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)
            else:
                embed = discord.Embed(title="Geburtstag eingetragen!",
                                      description=f"Dein geburtstag wurde erfolgreich auf den `{daten[2]}.{daten[1]}.{daten[0]}` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)

            await interaction.followup.send(embed=embed)
        except ValueError:
            await interaction.followup.send(content="Bitte gebe ein richtiges Datum ein.")
        except:
            raise

    @app_commands.command(name="show", description="Zeigt den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bshow(self, interaction, member: discord.Member = None):
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
                        title=f"Geburtstag von {user1.display_name}", description=f"Der User {user1.mention} hat am `{bdaylist[0]}.{bdaylist[1]}` geburtstag.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"Geburtstag von {user1.display_name}", description=f"Der User {user1.mention} hat am `{bdaylist[0]}.{bdaylist[1]}` geburtstag und ist im Jahr `{bdaylist[2]}` geboren.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)

            else:
                if bdaylist[2] == "1600":
                    embed = discord.Embed(
                        title=f"Geburtstag von {user1.display_name}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` geburtstag ", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title=f"Geburtstag von {user1.display_name}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` geburtstag und bist im Jahr `{bdaylist[2]}` geboren.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)
        except KeyError:
            if member == None:
                embed = discord.Embed(
                    title=f"Fehler", description=f"Es gab einen Fehler beim Anzeigen des Geburtstages von {interaction.user.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(
                    name="Grund:", value=f"{interaction.user.mention} hat keinen Geburtstag eingetragen")

            if member != None:
                embed = discord.Embed(
                    title=f"Fehler", description=f"Es gab einen Fehler beim Anzeigen des Geburtstages von {member.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(
                    name="Grund:", value=f"{member.mention} hat keinen Geburtstag eingetragen")

            await interaction.followup.send(embed=embed)

    @app_commands.command(name="delete", description="Löscht den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bdelete(self, interaction, member: discord.Member = None):

        try:
            await interaction.response.defer()
            id = interaction.user.id
            id2 = str(id)

            if member != None:
                userid = str(member.id)
                if interaction.user.guild_permissions.kick_members:
                    id3 = str(userid)
                    del bjson[id3]
                    embed = discord.Embed(title=f"Geburtstag von {member.display_name} gelöscht",
                                          description=f"Der Geburtstag von {member.display_name} wurde gelöscht.", timestamp=datetime.datetime.now(), color=0x0094ff)
                    await interaction.followup.send(embed=embed)

                else:
                    await interaction.followup.send(content=f"{rjson['catnewspaper']} {rjson['catnewspaper']} {rjson['catnewspaper']}", ephemeral=True)
            else:
                del bjson[id2]
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
        await ctx.response.defer()

        def divideListInChunks(list, chunkSize):
            for i in range(0, len(list), chunkSize):
                yield list[i:i + chunkSize]

        # mit 'members = [member.id for member in ctx.guild.members]' austauschen
        memberlist = [member.id for member in ctx.guild.members]

        jsonData = bjson  # Daten aus JSON laden

        users = list(jsonData)  # Ein Array mit UserIDs aus der JSON machen

        maxBDaysPerPage = 10  # Die Maximalen Geburtstage die pro Seite angezeigt werden sollen

        currentPage = 0  # Die Aktuelle Seite

        daytoday = datetime.datetime.now().strftime("%d")  # Heutiger Tag
        monthtoday = datetime.datetime.now().strftime("%m")  # Heutiger Monat
        yeartoday = datetime.datetime.now().strftime("%Y")  # Heutiges Jahr

        parsedBirthdays = []  # Geburtstage als ein bestimmtes Format

        for user in users:
            if int(user) in memberlist:  # ids sind strings, deshalb in int umwandeln
                mention = f"<@{user}>"
                birthday = jsonData[user]["bday"]
                # print(birthday)
                day = birthday.split("/")[0]
                month = birthday.split("/")[1]
                rawYear = birthday.split("/")[2]
                if int(month) > int(monthtoday):  # Monat war noch nicht -> Geburtstag war noch nicht
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

        sortedBirthdays = sorted(parsedBirthdays, key=lambda x: x['inDays'])

        chunkedBirthdays = [_ for _ in divideListInChunks(
            sortedBirthdays, maxBDaysPerPage)]

        # print(chunkedBirthdays)

        def generatePageContent():
            text = ""
            for birthday in chunkedBirthdays[currentPage]:
                if birthday['showAge']:
                    text += f"<@{birthday['user']}> ({birthday['newAge']}. Geburtstag) - <t:{birthday['timestamp']}:D> <t:{birthday['timestamp']}:R>\n"
                else:
                    text += f"<@{birthday['user']}> - <t:{birthday['timestamp']}:D> <t:{birthday['timestamp']}:R>\n"
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
            embed = discord.Embed(title="Die nächsten Geburtstage", description=generatePageContent(
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
        self.birthdayloop.start()
        self.bot.tree.add_command(birthdaycmds)
        print("Birthdays Geladen!")

    @tasks.loop(hours=1)
    async def birthdayloop(self):
        currenttime = datetime.datetime.fromtimestamp(
            int(time.time())).strftime('%H')
        if currenttime == "16":  # Es ist 3 Uhr morgends
            try:
                config = sjson  # config laden
                for server in config:
                    try:

                        roleid = int(config[server]["bdayrole"])
                        channelid = int(config[server]["bday"])

                        # <- Wenn es einen Ping geben soll
                        pingid = int(config[server]["bdayrole"])
                        guild = self.bot.get_guild(int(server))

                        birthdayconfig = bjson  # Birthdayconfig von den Server laden

                        birthdayMembers = []
                        daytoday = datetime.datetime.now().strftime("%d")  # Heutiger Tag
                        monthtoday = datetime.datetime.now().strftime("%m")  # Heutiger Monat
                        for member in guild.members:
                            try:
                                bday = birthdayconfig[str(member.id)]["bday"]
                                if str(daytoday) == bday.split("/")[0] and str(monthtoday) == bday.split("/")[1]:
                                    birthdayMembers.append(member)
                            except:
                                pass  # Mitglied hat den geburtstag nicht eingetragen
                        if len(birthdayMembers) == 0:
                            continue  # Es hat heute niemand auf den Server geburtstag

                        try:
                            role = guild.get_role(roleid)
                            for member in birthdayMembers:
                                try:
                                    await member.add_roles(role)
                                except:
                                    pass  # Der Bot darf den Member nicht bearbeiten
                        except:
                            pass  # Die Rolle existiert nicht

                        try:

                            # <- Wenn ping gewünscht
                            content = guild.get_role(int(pingid)).mention
                            pass
                        except:
                            content = None

                        channel = guild.get_channel(channelid)
                        birthdayPings = ""
                        for member in birthdayMembers:
                            birthdayPings += f"{member.mention} "
                        await channel.send(embed=discord.Embed(title="Herzlichen Glückwunsch!", description=f"{birthdayPings} {'Hat' if len(birthdayMembers) == 1 else 'Haben'} heute Geburtstag!!!", color=0xCB33F5), content=content)
                    except:
                        pass
            except:
                pass


async def setup(bot):
    await bot.add_cog(BirthdayCog(bot))
