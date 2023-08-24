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
import time

birthdayjson = utils.birthdayinit()

with open("serverconfig.json") as file:
    sjson = json.load(file)

with open("birthdays.json") as file:
    bjson = json.load(file)

with open('reactions.json') as file:
    rjson = json.load(file)





class BirthdayCommands(discord.app_commands.Group):

    


    @app_commands.command(name="setup", description="Erstelle ein Birthday System")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bsetup(self, interaction, birthdaychannel: discord.TextChannel):
        await interaction.response.defer()
        guildid = interaction.guild.id
        guildname = interaction.guild.name
        channelid = birthdaychannel.id
       
        sjson[str(guildid)] = {"name": guildname, "bday": channelid}
        with open("serverconfig.json", 'w') as json_file:
            json.dump(sjson, json_file, indent=4)

        await interaction.followup.send(f"Birthday Channel gesetzt auf {birthdaychannel.mention}")

    @app_commands.command(name="add", description="Füge deinen Geburtstag ins Geburtstagssystem ein")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def badd(self, interaction, tag: app_commands.Range[int, 1, 31], monat: app_commands.Range[int, 1, 12], jahr: app_commands.Range[int, 1960, 2020] = 1600):
        await interaction.response.defer()
        userid = interaction.user.id
        
        daten = ""
        if not jahr == None:
            today = datetime.date.today()
            date = datetime.date(jahr, monat, tag)
            date2 = str(date)
            daten = date2.split("-")
            print(date)
            print(today)
            bday = date.strftime("%d/%m/%Y")
            bjson[str(userid)] = {"bday": bday}

        else:
            today = datetime.date.today()
            date = datetime.date(jahr, monat, tag)
            date2 = str(date)
            daten = date2.split("-")
            print(date)
            print(today)
            bday = date.strftime("%d/%m/Y")
            bjson[str(userid)] = {"bday": bday}

        with open("birthdays.json", 'w') as json_file:
            json.dump(bjson, json_file, indent=4)

        if jahr == 1600:
            embed = discord.Embed(title="Geburtstag eingetragen!", description=f"Dein geburtstag wurde erfolgreich auf den `{daten[2]}.{daten[1]}.` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)
        else:
            embed = discord.Embed(title="Geburtstag eingetragen!", description=f"Dein geburtstag wurde erfolgreich auf den `{daten[2]}.{daten[1]}.{daten[0]}` gesetzt.", timestamp=datetime.datetime.now(), color=0x0094ff)

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
                embed = discord.Embed(title=f"Geburtstag von {user1.display_name}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` geburtstag ", timestamp=datetime.datetime.now(), color=0x0094ff)
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(title=f"Geburtstag von {user1.display_name}", description=f"Du hast am `{bdaylist[0]}.{bdaylist[1]}` geburtstag und bist im Jahr `{bdaylist[2]}` geboren.", timestamp=datetime.datetime.now(), color=0x0094ff)
                await interaction.followup.send(embed=embed)
        

    @app_commands.command(name="delete", description="Löscht den Geburtstag von einem Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def bdelete(self, interaction, member: discord.Member = None):
        await interaction.response.defer()
        id = interaction.user.id
        id2 = str(id)
        
        
        if member != None:
            userid = str(member.id)
            if interaction.user.guild_permissions.kick_members:
                id3 = str(userid)
                print(id3)
                del bjson[id3]
                embed = discord.Embed(title=f"Geburtstag von {member.display_name} gelöscht", description=f"Der Geburtstag von {member.display_name} wurde gelöscht.", timestamp=datetime.datetime.now(), color=0x0094ff)

                
            else:
                await interaction.followup.send(content=f"{rjson['catnewspaper']} {rjson['catnewspaper']} {rjson['catnewspaper']}", ephemeral=True)
        else:
            del bjson[id2]
            embed = discord.Embed(title=f"Geburtstag gelöscht", description=f"Du hast deinen Geburtstag gelöscht.", timestamp=datetime.datetime.now(), color=0x0094ff)

        await interaction.followup.send(embed=embed)

        with open("birthdays.json", 'w') as json_file:
            json.dump(bjson, json_file, indent=4)




    @app_commands.command(name="next", description="Zeigt die nächsten Geburtstage an")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def birthday(self, ctx):
        await ctx.response.defer()
        def divideListInChunks(list, chunkSize):
            for i in range(0, len(list), chunkSize): 
                yield list[i:i + chunkSize]

        memberlist = [member.id for member in ctx.guild.members] # mit 'members = [member.id for member in ctx.guild.members]' austauschen

        jsonData = bjson # Daten aus JSON laden

        users = list(jsonData) # Ein Array mit UserIDs aus der JSON machen

        maxBDaysPerPage = 10 # Die Maximalen Geburtstage die pro Seite angezeigt werden sollen

        currentPage = 0 # Die Aktuelle Seite

        daytoday = datetime.datetime.now().strftime("%d") # Heutiger Tag
        monthtoday = datetime.datetime.now().strftime("%m") # Heutiger Monat
        yeartoday = datetime.datetime.now().strftime("%Y") # Heutiges Jahr

        parsedBirthdays = [] # Geburtstage als ein bestimmtes Format 

        for user in users:
            if int(user) in memberlist: #ids sind strings, deshalb in int umwandeln
                mention = f"<@{user}>"
                birthday = jsonData[user]["bday"]
                print(birthday)
                day = birthday.split("/")[0]
                month = birthday.split("/")[1]
                rawYear = birthday.split("/")[2]
                if int(month) > int(monthtoday): # Monat war noch nicht -> Geburtstag war noch nicht
                    year = int(yeartoday)
                elif int(month) == int(monthtoday) and int(day) >= int(daytoday): # Monat ist heute aber Tag war noch nicht -> Geburtstag war noch nicht
                    year = int(yeartoday)
                else: # Geburtstag war schon
                    year = int(yeartoday) + 1
                
                date_obj = datetime.datetime.strptime(f"{month}-{day}-{year}", "%m-%d-%Y")

                birthdayParsed = {}
                birthdayParsed["inDays"] = (date_obj - datetime.datetime.now()).days
                birthdayParsed["showAge"] = rawYear != "1600"
                birthdayParsed["newAge"] = year - int(rawYear)
                birthdayParsed["user"] = user
                birthdayParsed["timestamp"] = int(time.time()) + birthdayParsed["inDays"] * 86400 +86400 # Für discord time formating
                parsedBirthdays.append(birthdayParsed)

        sortedBirthdays = sorted(parsedBirthdays, key=lambda x: x['inDays'])

        chunkedBirthdays = [_ for _ in divideListInChunks(sortedBirthdays, maxBDaysPerPage)]

        print(chunkedBirthdays)

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
            embed = discord.Embed(title = "Die nächsten Geburtstage", description = generatePageContent(), color=0x0094ff, timestamp=datetime.datetime.now())
            return embed

        async def updateEmbed(interaction):
            embed = getEmbed()
            await interaction.response.edit_message(embed = embed)

        embed = getEmbed()
        view = discord.ui.View()
        if len(chunkedBirthdays) > 1:
            prevpagebtn = discord.ui.Button(label = "⏪")
            prevpagebtn.callback = beforePage
            nextpagebtn = discord.ui.Button(label = "⏩")
            nextpagebtn.callback = nextPage
            view.add_item(prevpagebtn)
            view.add_item(nextpagebtn)

        await ctx.followup.send(embed = embed, view = view)


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
