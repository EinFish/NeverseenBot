import discord
import json
import datetime
from typing import Any, Literal
import requests
from discord import ui

def createAllJsons():
    requiredFiles = ["config.json", "serverconfig.json", "users.json", "languages.json", "reactions.json", "twitchconfig.json"]
    for fileName in requiredFiles:
        try:
            with open(fileName, 'x') as file:
                # If successful, the file is created with {} as content
                file.write("{}")
                print(f"File {fileName} was created")
        except FileExistsError:
            # The File already exists
            pass
        except Exception as e:
            print(f"An error occurred in {fileName} creation: {e}")

createAllJsons()

def checkIfConfigIsComplete():
    with open("config.json", "r") as file:
        configuration = json.load(file)
        configModified = False
        if not "APP_ID" in configuration:
            configModified = True
            appID = input("Please enter your App ID (the ID of your Bot): ")
            configuration["APP_ID"] = appID
        if not "TOKEN" in configuration:
            configModified = True
            token = input("Please enter your Bot token: ")
            configuration["TOKEN"] = token
        if not "TWITCH_URL" in configuration:
            configModified = True
            twitchurl = input("Please enter your Twitch URL (if you dont want one, ender 'skip'): ")
            configuration["TWITCH_URL"] = twitchurl
        if configModified:
            with open("config.json", "w") as file:
                json.dump(configuration, file, indent=4)

checkIfConfigIsComplete()

with open("config.json") as file:
    config = json.load(file)


async def errordcmessage(interaction, error):
    try:
        await interaction.response.send_message(content=f"Ein Error!\n\n```txt\n{error}```\nReporte bitte diesen Error mit `/utility bugreport`", ephemeral=True, view=Bugreportview())
    except discord.errors.InteractionResponded:
        await interaction.followup.send(content=f"Ein Error!\n\n```txt\n{error}```\nReporte bitte diesen Error mit `/utility bugreport`", ephemeral=True, view=Bugreportview())
    raise error


class bugReportModal(ui.Modal, title="Bugreport"):
    command = ui.TextInput(label="In welchem Befehl tritt der Bug auf?",
                           style=discord.TextStyle.short, placeholder="/fun twitch", required=True, max_length=255)
    excepted = ui.TextInput(label="Was hast du von dem Befehl erwartet?", style=discord.TextStyle.long,
                            placeholder="Informationen über einen Twitch Streamer", required=True, max_length=255)
    actual = ui.TextInput(label="Was hat dir der Befehl zurückgegeben?", style=discord.TextStyle.long,
                          placeholder="Nichts. Es lädt nur für immer", required=True, max_length=1024)
    reproduce = ui.TextInput(label="Was hast du gemacht, dass der Bug auftritt?",
                             style=discord.TextStyle.long, placeholder="Den Befehl ausgeführt", required=True, max_length=1024)
    extra = ui.TextInput(label="Sonst noch etwas, das wichtig ist?",
                         style=discord.TextStyle.long, placeholder="", required=False, max_length=1024)

    async def on_submit(self, interaction) -> None:
        recivers = config["OWNER_ID"]
        for reciver in recivers:
            reciv = interaction.client.get_user(reciver)
            await reciv.send(embed=discord.Embed(title="Bugreport", description=f"Bug reportet von {interaction.user} ({interaction.user.id})\n```\nBefehl: {self.command}\n\nerwartet: {self.excepted}\n\ntatsächlich: {self.actual}\n\nreproduce: {self.reproduce}\n\nExtra: {self.extra}\n```", color=0x7A50BE))
        embed = discord.Embed(
            title="Danke", description="Der Bug wurde reportet. Vielen Dank!", color=0x7A50BE)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class BugreportButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle):
        super().__init__(label=text, style=discordbuttonstyle)

    async def callback(self, ctx):
        with open("users.json") as file:
            ujson = json.load(file)
        if ujson[str(ctx.user.id)] != {"blacklist": True}:
            await ctx.response.send_modal(bugReportModal())
        else:
            await ctx.response.send_message("Du bist auf der Blacklist.", ephemeral=True)


class Bugreportview(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BugreportButton("Bug reporten",
                                      discord.ButtonStyle.success))


class WarnModal(discord.ui.Modal):
    def __init__(self, member):
        self.member = member
        super().__init__(title="Warnen:")
    grund = discord.ui.TextInput(label="Grund", placeholder="Gebe bitte einen Grund für das Warnen an",
                                 required=True, style=discord.TextStyle.short, max_length=100, min_length=5)

    async def on_submit(self, interaction) -> None:
        with open("users.json") as file:
            ujson = json.load(file)

        with open("serverconfig.json") as file:
            sjson = json.load(file)

        if interaction.user.guild_permissions.kick_members:
            try:
                warns = ujson[str(self.member.id)]["warns"]
            except:
                warns = 0
            ujson[str(self.member.id)] = {"warns": warns + 1}

            with open("users.json", "w") as json_file:
                json.dump(ujson, json_file, indent=4)

            try:
                guildid = interaction.guild.id
                dm = discord.Embed(
                    title="Du wurdest gewarnt!", timestamp=datetime.datetime.now(), color=0x0094ff)
                dm.add_field(name="Grund:", value=self.grund)
                dm.add_field(name="Server:", value=interaction.guild.name)
                await self.member.send(embed=dm)

                embed = discord.Embed(
                    title=f"{self.member.display_name} wurde Gewarnt.", timestamp=datetime.datetime.now(), color=0x0094ff)
                embed.add_field(name="Aktuelle Warnungen:",
                                value=warns + 1)
                embed.set_thumbnail(url=self.member.avatar)
                if self.grund != None:
                    embed.add_field(name="Grund:", value=self.grund)
                await interaction.response.send_message(embed=embed, ephemeral=True)

                log = discord.Embed(
                    title="User Gewarnt", description=f"Der User {self.member.mention} wurde von {interaction.user.mention} gewarnt.", timestamp=datetime.datetime.now(), color=0x0094ff)
                log.add_field(name="Grund", value=self.grund)
                try:
                    logchannelid = sjson[str(guildid)]["logchannel"]
                    logchannel = await self.member.guild.fetch_channel(logchannelid)
                    await logchannel.send(embed=log)
                except KeyError:
                    pass

            except discord.Forbidden:
                await interaction.response.send_message(content=f"Warnen Fehlgeschlagen. Der User {self.member.mention} hat `Direktnachrichten von Servermitgliedern` Ausgeschaltet.", ephemeral=True)


class ModButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle, mode, member, custom_id):
        super().__init__(label=text, style=discordbuttonstyle, custom_id=custom_id)
        self.mode = mode
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        member = self.member
        if self.mode == 0:
            with open("serverconfig.json") as file:
                sjson = json.load(file)

            guildid = interaction.guild.id
            channel = interaction.guild.get_channel(
                int(sjson[str(guildid)]["logchannel"]))
            if interaction.user.guild_permissions.ban_members:
                await interaction.response.send_message(content=f"Du hast {member.mention} erfolgreich gebannt", ephemeral=True)
                await member.ban()

                embed = discord.Embed(title="User gebannt", description="Ein User wurde von " +
                                      interaction.user.mention + " gebannt.", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(name="Gebannt:",
                                value=member.mention, inline=True)
                embed.add_field(
                    name="Von:", value=interaction.user.mention, inline=True)
                await channel.send(embed=embed)
            else:
                await interaction.response.send_message(content=f"Du hast keine Berechtigung dafür.", ephemeral=True)
        if self.mode == 1:
            with open("serverconfig.json") as file:
                sjson = json.load(file)

            if interaction.user.guild_permissions.kick_members:
                guildid = interaction.guild.id
                channel = interaction.guild.get_channel(
                    int(sjson[str(guildid)]["logchannel"]))
                await member.kick()
                await interaction.response.send_message(content=f"Du hast {member.mention} erfolgreich gekickt", ephemeral=True)

                embed = discord.Embed(title="User gekickt", description="Ein User wurde von " +
                                      interaction.user.mention + " gekickt.", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(name="Gekickt:",
                                value=member.mention, inline=True)
                embed.add_field(
                    name="Von:", value=interaction.user.mention, inline=True)
                await channel.send(embed=embed)

            else:
                await interaction.response.send_message(content="Du hast keine Berechtigung dafür.", ephemeral=True)
        if self.mode == 2:
            if interaction.user.guild_permissions.moderate_members:
                with open("serverconfig.json") as file:
                    sjson = json.load(file)

                guildid = interaction.guild.id
                channel = interaction.guild.get_channel(
                    int(sjson[str(guildid)]["logchannel"]))

                duration = datetime.timedelta(
                    seconds=0, minutes=0, hours=3, days=0)
                await interaction.response.send_message(content="Der User " + member.mention + f" wurde in ein Timeout geschickt für: {duration}", ephemeral=True)
                await member.timeout(duration)

                embed = discord.Embed(
                    title="User im Timeout", description=f"Ein User wurde von {interaction.user.mention} ins Timeout versetzt.", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(name="Im Timeout:",
                                value=member.mention, inline=True)
                embed.add_field(
                    name="Von:", value=interaction.user.mention, inline=True)
                embed.add_field(name="Für:", value=duration, inline=True)
                await channel.send(embed=embed)
            else:
                await interaction.response.send_message(content=f"Du hast keine Berechtigung dafür.", ephemeral=True)

        if self.mode == 3:
            if interaction.user.guild_permissions.moderate_members:
                await interaction.response.send_modal(WarnModal(member=member))
                print("3")
            else:
                await interaction.send_message(content="Dir fehlen Berechtigungen.")


class ModViewView(discord.ui.View):
    def __init__(self, member):
        self.member = member
        super().__init__(timeout=None)
        self.add_item(
            ModButton("Bannen", discord.ButtonStyle.danger, 0, self.member, custom_id="vb1"))
        self.add_item(
            ModButton("Kicken", discord.ButtonStyle.blurple, 1, self.member, custom_id="vb2"))
        self.add_item(
            ModButton("Muten (3h)", discord.ButtonStyle.secondary, 2, self.member, custom_id="vb3"))
        self.add_item(
            ModButton("Warnen", discord.ButtonStyle.danger, 3, self.member, custom_id="vb4"))


class EmbedBuilderButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle, mode, channel, embed, timestamp, custom_id, i):
        super().__init__(label=text, style=discordbuttonstyle, custom_id=custom_id)
        self.mode = mode
        self.channel = channel
        self.embed = embed
        self.timestamp = timestamp
        self.i = i

    async def callback(self, interaction: discord.Interaction):
        channel = self.channel
        embed = self.embed
        if self.mode == 0:
            await channel.send(embed=embed)
            self.disabled = True

            await interaction.response.send_message(content="Embed versendet.", ephemeral=True)

        if self.mode == 1:
            await interaction.response.send_modal(EmbedBuilder(channel=channel, timestamp=self.timestamp))


class EmbedBuilderView(discord.ui.View):
    def __init__(self, channel, embed, timestamp, i):
        self.channel = channel
        self.embed = embed
        self.timestamp = timestamp
        self.interaction = i
        super().__init__(timeout=None)
        self.add_item(EmbedBuilderButton(
            "Passt so", discord.ButtonStyle.success, 0, channel=channel, embed=embed, timestamp=timestamp, custom_id="eb1", i=i))
        self.add_item(EmbedBuilderButton(
            "Nein", discord.ButtonStyle.danger, 1, channel=channel, embed=embed, timestamp=timestamp, custom_id="eb2", i=i))


class EmbedBuilder(discord.ui.Modal):
    def __init__(self, channel, timestamp, i, thumb) -> None:
        self.channel = channel
        self.timestamp = timestamp
        self.i = i
        self.thumb = thumb
        super().__init__(title="Embed Builder")
    titel = discord.ui.TextInput(
        label="Titel:", placeholder="Setzte einen Titel", style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Beschreibung", placeholder="Füge eine Beschreibung hinzu",
                                       style=discord.TextStyle.long, max_length=1500, required=False)

    field1_name = discord.ui.TextInput(label="Feld 1", placeholder="Feld 1 name",
                                       style=discord.TextStyle.short, max_length=1500, required=False)

    field1_value = discord.ui.TextInput(label="Feld 1", placeholder="Feld 1 value",
                                        style=discord.TextStyle.long, max_length=1500, required=False)

    async def on_submit(self, interaction) -> None:
        if self.timestamp == True:
            embed = discord.Embed(
                title=self.titel, description=self.description, color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name=self.field1_name, value=self.field1_value)
        elif self.timestamp == False:
            embed = discord.Embed(
                title=self.titel, description=self.description, color=0x0094ff)
            embed.add_field(name=self.field1_name, value=self.field1_value)

        if self.thumb != None:
            embed.set_thumbnail(url=self.thumb)

        await interaction.response.send_message(embed=embed, view=EmbedBuilderView(channel=self.channel, embed=embed, timestamp=self.timestamp, i=self.i), ephemeral=True)


class BewerbenModal(discord.ui.Modal):
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

        try:
            if sjson[str(id)]["bewechannel"] != 0:
                channelid = sjson[str(id)]["bewechannel"]
            else:
                channelid = sjson[str(id)]["logchannel"]
        except KeyError:

            channelid = sjson[str(id)]["logchannel"]

        frage0 = BewerbenModal.frage0

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


class BewerbenView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(BewerbenButton("Bewerben",
                      discord.ButtonStyle.success, custom_id="bb1"))


class BewerbenButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle, custom_id):
        super().__init__(label=text, style=discordbuttonstyle, custom_id=custom_id)

    async def callback(self, interaction: discord.Interaction) -> Any:
        with open("serverconfig.json") as file:
            sjson = json.load(file)
        guildid = interaction.guild.id
        try:
            bwp = sjson[str(guildid)]["bwp"]
            if bwp == True:
                await interaction.response.send_modal(BewerbenModal())
            else:
                await interaction.response.send_message(content="Bewerbungsphase geschlossen.", ephemeral=True)
        except KeyError:
            await interaction.response.send_message(content="Bewerbungsphase geschlossen.", ephemeral=True)


def twitchconfig():
    with open("twitchconfig.json") as file:
        tconfig = json.load(file)
    return tconfig


def config():
    with open("config.json") as file:
        config = json.load(file)
    return config


def serverjson():
    with open("serverconfig.json") as file:
        wjson = json.load(file)
    return wjson


def get_app_access_token():
    tconfig = twitchconfig()
    params = {
        "client_id": tconfig["client_id"],
        "client_secret": tconfig["client_secret"],
        "grant_type": "client_credentials"
    }

    response = requests.post(
        "https://id.twitch.tv/oauth2/token", params=params)
    access_token = response.json()["access_token"]
    return access_token


def savejson(file: dict, json_name: Literal["serverconfig","users","languages","reactions", "twitch"]):
    try:
        if type(file) != dict:
            print("Please Devide a Dictionary.")
            return
        if json_name == "serverconfig":
            with open("serverconfig.json", "w") as json_file:
                json.dump(file, json_file, indent=4)
            return
        if json_name == "users":
            with open("users.json", "w") as json_file:
                json.dump(file, json_file, indent=4)
            return
        if json_name == "languages":
            with open("languages.json", "w") as json_file:
                json.dump(file, json_file, indent=4)
            return
        if json_name == "reactions":
            with open("reactions.json", "w") as json_file:
                json.dump(file, json_file, indent=4)
            return
        if json_name == "twitch":
            with open("twitchconfig.json", "w") as json_file:
                json.dump(file, json_file, indent=4)
            return

    except Exception as Error:
        print(Error)
