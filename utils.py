import discord
import json
import datetime


class ErrorMessage():

    async def errordcmessage(interaction, error):

        await interaction.response.send_message(content=f"Ein Error!\n\n```txt\n{error}```\nReporte bitte diesen Error mit `/utility bugreport`", ephemeral=True)


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
            print("3")


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
