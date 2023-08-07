import asyncio
from typing import Any, Optional, Union
import discord
from discord.emoji import Emoji
from discord.enums import ButtonStyle
from discord.ext import commands
from discord import app_commands
import datetime
from discord.interactions import Interaction

from discord.utils import MISSING



class EmbedBuilder(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="Embed Builder")
    titel = discord.ui.TextInput(label="Titel:", placeholder="Setzte einen Titel", style=discord.TextStyle.short)
  #  farbe = discord.ui.TextInput(label="Farbe:", placeholder="Bitte einen Hex farbcode ohne #", style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Beschreibung", placeholder="Füge eine Beschreibung hinzu", style=discord.TextStyle.long, max_length=1500, required=False)    
    

    async def on_submit(self, interaction) -> None:
        embed = discord.Embed(title=EmbedBuilder.titel, color=0x0094ff, description=EmbedBuilder.description)
        await interaction.response.defer()
        await interaction.followup.send(embed=embed)

class TicketModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="Problembeschreibung:")
    problem = discord.ui.TextInput(label="Was ist dein Anliegen?", placeholder="Problem", required=True, style=discord.TextStyle.short, max_length=100, min_length=10)
    async def on_submit(self, interaction) -> None:
        mod = "<@&1063569606658248746>"
        Channel = interaction.channel
        person = interaction.user.mention
        id = interaction.user.id
        Thread = await Channel.create_thread(name=interaction.user.display_name)
        await interaction.response.send_message(content="Dein Ticket findest du hier: " + Thread.jump_url , ephemeral=True)
        embed = discord.Embed(color=0x0094ff, timestamp=datetime.datetime.now(), title=self.problem, description=interaction.user.mention + " bitte beschreibe dein Problem näher. Es wird sich bald ein Team Mitglied um dein Problem kümmern.")
        await Thread.send(content=person + mod, embed=embed)
        
class TicketButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle):
        super().__init__(label=text, style=discordbuttonstyle)

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_modal(TicketModal())

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton("Ticket erstellen", discord.ButtonStyle.success))


class FunCommands(discord.app_commands.Group):
    @app_commands.command(name="twitch", description="Bekomme den Twitch Link!")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def twich(self, ctx):
        await ctx.response.defer()
        embed = discord.Embed(title="Twitch Link", description=f"https://www.twitch.tv/neverseen_minecraft", color=0x0094ff, timestamp=datetime.datetime.now())
        await ctx.followup.send(embed=embed)

    @app_commands.command(name="play-music", description="Spielt einen ausgewählten Song.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def playsong(self, interaction):
        await interaction.response.send_message("Nicht eingebaut!", ephemeral=True)


class ModCommands(discord.app_commands.Group):
    
    @app_commands.command(name="delete-messages", description="Lösche Nachrichten von einem Bestimmten User.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def delete(self, ctx, user: discord.Member):
        await ctx.response.defer()
        print(user)


    @app_commands.command(name="ticketchannel", description="Lege den Kanal für die Tickets fest.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def ticket_channel(self, interaction, channel: discord.TextChannel, titel: str, text: str = ""):
        if text == "":
            text = "Klicke auf den unteren Knopf um ein " + titel + " ticket zu erstellen."
        await interaction.response.defer()
        print(channel.id)
        embed = discord.Embed(title=titel, description=text, color=0x0094ff)
        await interaction.followup.send(content="erstellt", ephemeral=True)
        await channel.send(embed=embed, view=TicketView())


    @app_commands.command(name="ban", description="Banne einen Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def on_member_ban(self, member, user: discord.Member, reason: str):
        server = self.get_guild(1063567516737224805)
        channel = server.get_channel(1063958279409115136)
        embed = discord.Embed(title="User gebannt",description="Ein User wurde gebannt",color=0x0094ff, timestamp=datetime.datetime.now())
        embed.add_field(name="Gebannt:", value=user, inline=True)
        embed.add_field(name="Von:", value=user, inline=True)
        await server.ban(user, reason=reason)
        await channel.send(embed=embed)

    @app_commands.command(name="unban", description="Entbanne einen Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def on_member_unban(self, guild, user: discord.User, reason: str):
        print("unban")
        await guild.unban(user, reason=reason)


    @app_commands.command(name="embed-builder", description="Baue ein Embed in einem Formular!")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def embedbuilder(self, interaction):
        await interaction.response.send_modal(EmbedBuilder())

class HelpView(discord.ui.View):
    def __init__(self, client, timeout=3600):
        super().__init__(timeout=timeout)
        options = HelpSelect.generate_options(client)
        self.add_item(HelpSelect(client, options))

class HelpSelect(discord.ui.Select):

    options = []

    def __init__(self, client, options):
        self.client = client
        super().__init__(placeholder="Wofür möchtest du Hilfe erhalten?",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction):
        newtext = ""
        for group in interaction.client.tree.walk_commands():
            if group.name == self.values[0]:
                for command in group.commands:
                    newtext += f"\n`{command.name}"

                    for param in command.parameters:
                        if param.required:
                            newtext += f" {param.name}"
                        else:
                            newtext += f" ({param.name})"

                    newtext += f"`: {command.description}"
        embed = discord.Embed(
            title=self.values[0], description=newtext, color=0x0094ff)
        embed.set_footer(
            text=f"{interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed)

    @classmethod
    def generate_options(self, client):
        options = []
        groups = []
        for cmd in client.tree.walk_commands():
            if cmd.parent is not None:
                if cmd.parent.qualified_name not in groups:
                    groups.append(cmd.parent.qualified_name)
                    options.append(discord.SelectOption(
                        label=cmd.parent.qualified_name,
                        description=cmd.parent.description,
                        value=cmd.parent.qualified_name
                    ))
        return options


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        funcmds = FunCommands(name="fun", description="zum Spaß haben")
        modcmds = ModCommands(name="mod", description="Zum Moderieren")
        self.bot.tree.add_command(funcmds)
        self.bot.tree.add_command(modcmds)
        print("Commands geladen!")

    @app_commands.command(name="help", description="bekomme hilfe")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def help(self, ctx):
        await ctx.response.defer()
        try:
            embed = discord.Embed(
                title="Wofür möchtest du hilfe erhalten?", description=f"Suche eine der unten stehenden Kategorien aus, um Hilfe zu erhalten", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.set_footer(
                text=f"{ctx.user}", icon_url=ctx.user.avatar.url if ctx.user.avatar != None else None)
            await ctx.followup.send(embed=embed, view=HelpView(ctx.client))
        except:
            embed = discord.Embed(
                title="Fehler!", description=f"Nicht einmal ich kann dir dabei helfen :c", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.set_footer(
                text=f"{ctx.user}", icon_url=ctx.user.avatar.url if ctx.user.avatar != None else None)
            await ctx.followup.send(embed=embed)


    @commands.command()
    async def sync(self, ctx) -> None:
        if ctx.author.id != 753863284448428102:
            await ctx.send("Das solltest du besser lassen :)")
            return
        print("started sync")
        fmt = await ctx.bot.tree.sync()
        await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} Befehle wurden gesynced.")
        print("finished sync")



async def setup(bot):
    await bot.add_cog(Commands(bot))