import asyncio
import discord
from typing import Any
from discord.ext import commands
from discord import app_commands
import json
""" 
with open("serverconfig.json") as file:
    sjson = json.load(file) """

with open("config.json") as file:
    config = json.load(file)

with open("reactions.json") as file:
    rjson = json.load(file)


class TicketModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Bewerben")
    frage0 = discord.ui.TextInput(label="Kurze Selbstvorstellung & Deine Motivation", placeholder="Required",
                                  required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage1 = discord.ui.TextInput(label="Hast du Erfahrung im Umgang mit Twitch?", placeholder="Required",
                                  required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage2 = discord.ui.TextInput(label="Hast du gute Kommunikationsfähigkeiten?", placeholder="Required",
                                  required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage3 = discord.ui.TextInput(label="Verantfortungsbewusst und Zeitlich Flexibel?", placeholder="Required",
                                  required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage4 = discord.ui.TextInput(label="Kannst du in einem Team arbeiten?", placeholder="Required",
                                  required=True, style=discord.TextStyle.short, max_length=500, min_length=10)

    async def on_submit(self, interaction) -> None:
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        id = interaction.guild.id
        print(id)
        if sjson[str(id)]["bewechannel"] != 0:
            try:
                channelid = sjson[str(id)]["bewechannel"]
            except:
                print("ned geklappt")
                channelid = sjson[str(id)]["log"]
            print(channelid)

        else:
            channelid = sjson[str(id)]["log"]

        frage0 = TicketModal.frage0
        print(frage0)

        channel = await interaction.guild.fetch_channel(channelid)

        embed = discord.Embed(title="Neue Bewerbung")
        embed.add_field(
            name="Kurze Selbstvorstellung & Deine Motivation", value=TicketModal.frage0)
        embed.add_field(
            name="Hast du Erfahrung im Umgang mit Twitch?", value=TicketModal.frage1)
        embed.add_field(
            name="Hast du gute Kommunikationsfähigkeiten?", value=TicketModal.frage2)
        embed.add_field(
            name="Verantfortungsbewusst und Zeitlich Flexibel?", value=TicketModal.frage3)
        embed.add_field(
            name="Kannst du in einem Team arbeiten?", value=TicketModal.frage4)

        await channel.send(embed=embed)

        await interaction.response.send_message(content="Bewerbung eingereicht!", ephemeral=True)


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton("Ticket erstellen",
                      discord.ButtonStyle.success))


class TicketButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle):
        super().__init__(label=text, style=discordbuttonstyle)

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_modal(TicketModal())


class AdminCommands(discord.app_commands.Group):
    @app_commands.command(name="setup", description="Passe die Einstellungen des Bots an deinen Server an")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def setupserver(self, interaction, modrole: discord.Role, logchannel: discord.TextChannel = None, birthdaychannel: discord.TextChannel = None, welcomechannel: discord.TextChannel = None, birthdayrole: discord.Role = None, bewerbungschannel: discord.TextChannel = None):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        await interaction.response.defer()
        if interaction.user.guild_permissions.administrator:
            guildid = interaction.guild.id
            guildname = interaction.guild.name
            birthdayrole2 = ""
            modrole2 = modrole.mention
            if birthdayrole != None:
                birthdayrole2 = birthdayrole.id
            if welcomechannel == None:
                welcomechannel = "None"
            sjson[str(guildid)] = {"name": guildname, "modrole": modrole2}
            if birthdaychannel != None:
                sjson[str(guildid)]["bday"] = birthdaychannel.id
            if bewerbungschannel != None:
                sjson[str(guildid)]["bewerben"] = bewerbungschannel.id
            if logchannel != None:
                sjson[str(guildid)]["log"] = logchannel.id
            if welcomechannel != "None":
                sjson[str(guildid)]["welcome"] = welcomechannel.id
            else:
                sjson[str(guildid)]["welcome"] = welcomechannel
            if birthdayrole2 != "":
                sjson[str(guildid)]["bdayrole"] = birthdayrole2
            with open("serverconfig.json", "w") as json_file:
                json.dump(sjson, json_file, indent=4)

            await interaction.followup.send(content="👌")
        else:
            await interaction.followup.send(content=f"{rjson['catnewspaper']}", ephemeral=True)

    @app_commands.command(name="welcome-embed", description="Legt die willkommensnachricht fest.")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def wmessage(self, interaction, titel: str, beschreibung: str, farbe: str = None, membercount: bool = False):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = interaction.guild.id
        await interaction.response.defer()
        if interaction.user.guild_permissions.administrator:
            if sjson[str(guildid)]["welcome"] != "None":
                if membercount == False:
                    embed = {"title": titel, "description": beschreibung}
                if membercount == False:
                    embed = {"title": titel, "description": beschreibung}
                if membercount == False:
                    embed = {"title": titel, "description": beschreibung}
                if membercount == False:
                    embed = {"title": titel, "description": beschreibung}
                if membercount == False:
                    embed = {"title": titel, "description": beschreibung}
                if membercount == False:
                    embed = {"title": titel, "description": beschreibung}
                if membercount == False:
                    embed = {"title": titel, "description": beschreibung}
                sjson[str(guildid)]["welcomemsg"] = embed
                print("dfj")

                print("dfj")

            else:
                await interaction.followup.send(content="Bitte lege erst den welcome channel fest mit `/admin setup`", ephemeral=True)
                print("dfj")
            print("dfj")

        else:
            await interaction.followup.send(
                content=f"{rjson['catnewspaper']}", ephemeral=True)

    @app_commands.command(name="bewerben-phase", description="öffne oder schließe die phase zum bewerben")
    @commands.cooldown(1, 10, commands.BucketType.user,)
    async def bwp(self, interaction, phase: bool, channel: discord.TextChannel):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        await interaction.response.defer()
        guildid = interaction.guild.id
        if interaction.user.guild_permissions.administrator:
            sjson[str(guildid)]["bwp"] = phase
            print("dfj")
            embed = discord.Embed(
                title="Bewerben", description="Klicke hier um dich zu bewerben", color=0x0094ff)

            await channel.send(embed=embed, view=TicketView())

            with open("serverconfig.json", "w") as file:
                json.dump(sjson, file, indent=4)

        else:
            await interaction.followup.send(content="Du hast keine Berechtigungen dafür.", ephemeral=True)
        print("dfj")

    async def on_guild_remove(ctx):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = ctx.guild.id
        del sjson[str(guildid)]
        print("dfj")


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        admincmds = AdminCommands(
            name="admin", description="Befehle für admins")
        self.bot.tree.add_command(admincmds)
        print("AdminCommands Geladen!")

    @commands.command()
    async def sync(self, ctx) -> None:
        id = config["OWNER_ID"]
        id2 = int(id)
        if ctx.author.id != id2:
            await ctx.send("Das solltest du besser lassen :)")
            return
        print("started sync")
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} Befehle wurden gesynced.")
        print("finished sync")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
