import discord
import asyncio
from typing import Any
from discord.ext import commands
from discord import app_commands
import json
import datetime
from utils import BewerbenView


class SetupCommands(discord.app_commands.Group):

    @app_commands.command(name="rollen", description="sdfgrver an")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def roles(self, interaction, modrole: discord.Role = None, birthdayrole: discord.Role = None):
        if interaction.user.guild_permissions.administrator:

            guildid = interaction.guild.id
            with open("serverconfig.json") as file:
                sjson = json.load(file)
            if birthdayrole != None:
                birthdayrole2 = birthdayrole.id
            else:
                birthdayrole2 = ""
            if modrole != None:
                modrole2 = modrole.mention
            else:
                modrole2 = ""
            sjson[str(guildid)]["bdayrole"] = birthdayrole2
            sjson[str(guildid)]["modrole"] = modrole2

            with open("serverconfig.json", "w") as json_file:
                json.dump(sjson, json_file, indent=4)

            await interaction.response.send_message(content="Erfolg!", ephemeral=True)

        else:
            await interaction.response.send_message(content=f"Du hast keine Berechtigungen für diesen Command.", ephemeral=True)

    @app_commands.command(name="log", description="Passe die Einstellusdf Server an")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def logchannel(self, interaction, logchannel: discord.TextChannel):
        if interaction.user.guild_permissions.administrator:
            with open("serverconfig.json") as file:
                sjson = json.load(file)
            guildid = interaction.guild.id
            sjson[str(guildid)]["logchannel"] = logchannel.id
            with open("serverconfig.json", "w") as json_file:
                json.dump(sjson, json_file, indent=4)
            await interaction.response.send_message(content="Erfolg!", ephemeral=True)
        else:
            await interaction.response.send_message(content=f"Du hast keine Berechtigungen für diesen Command.", ephemeral=True)

    @app_commands.command(name="welcome-channel", description="Passsdfn des Bots an deinen Server an")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def welcomechannel(self, interaction, welcomechannel: discord.TextChannel):
        if interaction.user.guild_permissions.administrator:
            with open("serverconfig.json") as file:
                sjson = json.load(file)
            guildid = interaction.guild.id
            sjson[str(guildid)]["welcome"] = {"channel": welcomechannel.id}

            with open("serverconfig.json", "w") as json_file:
                json.dump(sjson, json_file, indent=4)

            await interaction.response.send_message(content="Erfolg!\nBitte bedenke, dass die Willkommensnachricht zurückgesetzt wurde.", ephemeral=True)

        else:
            await interaction.response.send_message(content=f"Du hast keine Berechtigungen für diesen Command.", ephemeral=True)

    @app_commands.command(name="bewerben", description="Passe die Esdfngen des Bots an deinen Server an")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def bwp(self, interaction, phase: bool, channel: discord.TextChannel = None):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = interaction.guild.id
        if interaction.user.guild_permissions.administrator:
            sjson[str(guildid)]["bwp"] = phase
            embed = discord.Embed(
                title="Bewerben", description="Klicke hier um dich zu bewerben", color=0x0094ff)

            with open("serverconfig.json", "w") as file:
                json.dump(sjson, file, indent=4)

            if phase == True:
                try:
                    await channel.send(embed=embed, view=BewerbenView())
                except AttributeError:
                    await interaction.response.send_message(content=f"ERROR: Bitte lege einen Kanal fest.", ephemeral=True)
                    return
                await interaction.response.send_message(content=f"Bewerbungsphase auf {phase} gesetzt.", ephemeral=True)
                return
            await interaction.response.send_message(content=f"Bewerbungsphase auf {phase} gesetzt.", ephemeral=True)
        else:
            await interaction.response.send_message(content="Du hast keine Berechtigungen dafür.", ephemeral=True)

    async def on_guild_remove(ctx):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = ctx.guild.id
        del sjson[str(guildid)]

    @app_commands.command(name="welcome-embed", description="Legt die willkommensnachricht fest.")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def wmessage(self, interaction, titel: str, beschreibung: str, membercount: bool = False, timestamp: bool = False, profilepicture: bool = False, usermention: bool = False):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = interaction.guild.id
        if interaction.user.guild_permissions.administrator:
            try:
                sjson[str(guildid)]["welcome"]["title"] = titel
                sjson[str(guildid)]["welcome"]["description"] = beschreibung
                sjson[str(guildid)]["welcome"]["membercount"] = membercount
                sjson[str(guildid)]["welcome"]["timestamp"] = timestamp
                sjson[str(guildid)]["welcome"]["usermention"] = usermention
                sjson[str(guildid)]["welcome"]["profilepicture"] = profilepicture

            except KeyError:
                await interaction.response.send_message(content="Bitte lege erst den Willkommenskanal Fest.", ephemeral=True)

            with open("serverconfig.json", "w") as json_file:
                json.dump(sjson, json_file, indent=4)
            try:
                logchannelid = sjson[str(guildid)]["logchannel"]
                logchannel = await interaction.guild.fetch_channel(logchannelid)
            except KeyError:
                pass

            if usermention == True:
                welcome_embed = discord.Embed(title=f"Herzlich Willkommen {interaction.user.display_name}",
                                              description=f"Willkommen in der Neverseen Community {interaction.user.mention}", color=0x0094ff)
                if timestamp == True:
                    welcome_embed = discord.Embed(
                        title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                        members = interaction.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)
                if membercount == True:
                    welcome_embed = discord.Embed(
                        title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", color=0x0094ff)
                    members = interaction.guild.member_count
                    welcome_embed.add_field(
                        name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = interaction.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                if profilepicture == True:
                    welcome_embed = discord.Embed(
                        title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", color=0x0094ff)
                    welcome_embed.set_thumbnail(
                        url=interaction.user.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", timestamp=datetime.datetime.now(), color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {interaction.user.display_name}", description=f"Willkommen in der Neverseen Community {interaction.user.mention}", timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = interaction.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)

            else:
                welcome_embed = discord.Embed(
                    title=titel, description=beschreibung, color=0x0094ff)
                if timestamp == True:
                    welcome_embed = discord.Embed(
                        title=titel, description=beschreibung, color=0x0094ff, timestamp=datetime.datetime.now())
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, color=0x0094ff, timestamp=datetime.datetime.now())
                        members = interaction.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)
                if membercount == True:
                    welcome_embed = discord.Embed(
                        title=titel, description=beschreibung, color=0x0094ff)
                    members = interaction.guild.member_count
                    welcome_embed.add_field(
                        name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = interaction.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                if profilepicture == True:
                    welcome_embed = discord.Embed(
                        title=titel, description=beschreibung, color=0x0094ff)
                    welcome_embed.set_thumbnail(
                        url=interaction.user.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, timestamp=datetime.datetime.now(), color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = interaction.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                        welcome_embed.set_thumbnail(
                            url=interaction.user.avatar)
            try:
                await logchannel.send(content="Die Willkommensnachricht wurde geändert!", embed=welcome_embed)
                await interaction.response.send_message(content="Willkommensembed gesetzt!", ephemeral=True)
            except UnboundLocalError:
                await interaction.response.send_message(content="Willkommensembed gesetzt!", ephemeral=True)

        else:
            await interaction.response.send_message(content=f"Du hast keine Berechtigung dafür.", ephemeral=True)


class SetupCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        setupcmds = SetupCommands(
            name="setup", description="Befehle zum aufsetzen des Servers")
        self.bot.tree.add_command(setupcmds)
        print("SetupCommands Geladen!")


async def setup(bot):
    await bot.add_cog(SetupCog(bot))
