import discord
import json
import datetime


class ErrorMessage():

    async def errordcmessage(interaction, error):

        await interaction.response.send_message(content=f"Ein Error!\n\n```txt\n{error}```\nReporte bitte diesen Error mit `/utility bugreport`", ephemeral=True)


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
                    logchannelid = sjson[str(guildid)]["log"]
                    logchannel = await self.member.guild.fetch_channel(logchannelid)
                    await logchannel.send(embed=log)
                except KeyError:
                    pass

            except discord.Forbidden:
                await interaction.response.send_message(content=f"Warnen Fehlgeschlagen. Der User {self.member.mention} hat `Direktnachrichten von Servermitgliedern` Ausgeschaltet.", ephemeral=True)


class ModButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle, mode, member):
        super().__init__(label=text, style=discordbuttonstyle)
        self.mode = mode
        self.member = member

    async def callback(self, interaction: discord.Interaction):
        member = self.member
        if self.mode == 0:
            with open("serverconfig.json") as file:
                sjson = json.load(file)

            guildid = interaction.guild.id
            channel = interaction.guild.get_channel(
                int(sjson[str(guildid)]["log"]))
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
                    int(sjson[str(guildid)]["log"]))
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
                    int(sjson[str(guildid)]["log"]))

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
            ModButton("Bannen", discord.ButtonStyle.danger, 0, self.member))
        self.add_item(
            ModButton("Kicken", discord.ButtonStyle.blurple, 1, self.member))
        self.add_item(
            ModButton("Muten (3h)", discord.ButtonStyle.secondary, 2, self.member))
        self.add_item(
            ModButton("Warnen", discord.ButtonStyle.danger, 3, self.member))


class EmbedBuilderButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle, mode, channel, embed, timestamp):
        super().__init__(label=text, style=discordbuttonstyle)
        self.mode = mode
        self.channel = channel
        self.embed = embed
        self.timestamp = timestamp

    async def callback(self, interaction: discord.Interaction):
        channel = self.channel
        embed = self.embed
        if self.mode == 0:
            await channel.send(embed=embed)
            await interaction.response.send_message(content="Embed versendet.", ephemeral=True)

        if self.mode == 1:
            await interaction.response.send_modal(EmbedBuilder(channel=channel, timestamp=self.timestamp))


class EmbedBuilderView(discord.ui.View):
    def __init__(self, channel, embed, timestamp):
        self.channel = channel
        self.embed = embed
        self.timestamp = timestamp
        super().__init__(timeout=None)
        self.add_item(EmbedBuilderButton(
            "Passt so", discord.ButtonStyle.success, 0, channel=channel, embed=embed, timestamp=timestamp))
        self.add_item(EmbedBuilderButton(
            "Nein", discord.ButtonStyle.danger, 1, channel=channel, embed=embed, timestamp=timestamp))


class EmbedBuilder(discord.ui.Modal):
    def __init__(self, channel, timestamp) -> None:
        self.channel = channel
        self.timestamp = timestamp
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

        await interaction.response.send_message(embed=embed, view=EmbedBuilderView(channel=self.channel, embed=embed, timestamp=self.timestamp), ephemeral=True)
