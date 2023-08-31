import asyncio
import discord
from typing import Any
from discord.ext import commands
from discord import app_commands
import json
import datetime
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

        try:
            if sjson[str(id)]["bewechannel"] != 0:
                channelid = sjson[str(id)]["bewechannel"]
            else:
                channelid = sjson[str(id)]["log"]
        except KeyError:
            print("ned geklappt")
            channelid = sjson[str(id)]["log"]
        print(channelid)

        frage0 = TicketModal.frage0
        print(frage0)

        channel = await interaction.guild.fetch_channel(channelid)

        embed = discord.Embed(title="Neue Bewerbung",
                              color=0x0094ff, timestamp=datetime.datetime.now(), description=f"Bewerbung von {interaction.user.mention}")
        embed.add_field(
            name="Kurze Selbstvorstellung & Deine Motivation", value=self.frage0, inline=False)
        embed.add_field(
            name="Hast du Erfahrung im Umgang mit Twitch?", value=self.frage1, inline=False)
        embed.add_field(
            name="Hast du gute Kommunikationsfähigkeiten?", value=self.frage2, inline=False)
        embed.add_field(
            name="Verantfortungsbewusst und Zeitlich Flexibel?", value=self.frage3, inline=False)
        embed.add_field(
            name="Kannst du in einem Team arbeiten?", value=self.frage4, inline=False)

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

        if interaction.user.guild_permissions.administrator:
            bdchannelcheck = False
            await interaction.response.defer()
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
                sjson[str(guildid)]["welcome"] = {"channel": welcomechannel.id}
                bdchannelcheck = True
            else:
                sjson[str(guildid)]["welcome"] = {"channel": welcomechannel}
            if birthdayrole2 != "":
                sjson[str(guildid)]["bdayrole"] = birthdayrole2
            with open("serverconfig.json", "w") as json_file:
                json.dump(sjson, json_file, indent=4)
            if bdchannelcheck == False:
                await interaction.followup.send(content="👌")
                return
            if bdchannelcheck == True:
                await interaction.followup.send(content=f"👌\nBitte beachte `/admin welcome-embed` auszuführen. Auch wen du dies vorher schon getan hast!")
        else:
            await interaction.response.send_message(content=f"{rjson['catnewspaper']}", ephemeral=True)

    @app_commands.command(name="welcome-embed", description="Legt die willkommensnachricht fest.")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def wmessage(self, interaction, titel: str, beschreibung: str, membercount: bool = False, timestamp: bool = False, profilepicture: bool = False, usermention: bool = False):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = interaction.guild.id
        if interaction.user.guild_permissions.administrator:
            if sjson[str(guildid)]["welcome"] != "None":
                sjson[str(guildid)]["welcome"]["title"] = titel
                sjson[str(guildid)]["welcome"]["description"] = beschreibung
                sjson[str(guildid)]["welcome"]["membercount"] = membercount
                sjson[str(guildid)]["welcome"]["timestamp"] = timestamp
                sjson[str(guildid)]["welcome"]["usermention"] = usermention
                sjson[str(guildid)]["welcome"]["profilepicture"] = profilepicture

                with open("serverconfig.json", "w") as json_file:
                    json.dump(sjson, json_file, indent=4)

                logchannelid = sjson[str(guildid)]["log"]
                logchannel = await interaction.guild.fetch_channel(logchannelid)

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

                await logchannel.send(content="Die Willkommensnachricht wurde geändert!", embed=welcome_embed)
                await interaction.response.send_message(content="Willkommensembed gesetzt!", ephemeral=True)

            else:
                await interaction.response.send_message(content="Bitte lege erst den welcome channel fest mit `/admin setup`", ephemeral=True)
                print("dfj")
            print("dfj")

        else:
            await interaction.response.send_message(content=f"{rjson['catnewspaper']}", ephemeral=True)

    @app_commands.command(name="bewerben-phase", description="öffne oder schließe die phase zum bewerben")
    @commands.cooldown(1, 10, commands.BucketType.user,)
    async def bwp(self, interaction, phase: bool, channel: discord.TextChannel = None):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = interaction.guild.id
        if interaction.user.guild_permissions.administrator:
            sjson[str(guildid)]["bwp"] = phase
            print("dfj")
            embed = discord.Embed(
                title="Bewerben", description="Klicke hier um dich zu bewerben", color=0x0094ff)

            with open("serverconfig.json", "w") as file:
                json.dump(sjson, file, indent=4)

            if phase == True:
                try:
                    await channel.send(embed=embed, view=TicketView())
                except AttributeError:
                    await interaction.response.send_message(content=f"ERROR: Bitte lege einen Kanal fest.", ephemeral=True)
                    return
                await interaction.response.send_message(content=f"Bewerbungsphase auf {phase} gesetzt.", ephemeral=True)
                return
            await interaction.response.send_message(content=f"Bewerbungsphase auf {phase} gesetzt.", ephemeral=True)
        else:
            await interaction.response.send_message(content="Du hast keine Berechtigungen dafür.", ephemeral=True)
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
        # id2 = int(id)
        if ctx.author.id not in id:
            await ctx.send("Das solltest du besser lassen :)")
            return
        print("started sync")
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} Befehle wurden gesynced.")
        print("finished sync")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
