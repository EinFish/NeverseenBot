import discord
from discord.ext import commands
from discord import app_commands, ui
import json
from typing import Literal
import datetime
import utils

errormessage = utils.ErrorMessage.errordcmessage


sspauswahl = ""
sspuser = "test"
ssptitle = ""
sspdescription = ""
sspwinner = None


with open('config.json') as file:
    config = json.load(file)

with open("users.json") as file:
    ujson = json.load(file)


class Fun(discord.app_commands.Group):
    try:
        @app_commands.command(name="twitch", description="Bekomme den Twitch Link!")
        @commands.cooldown(1, 20, commands.BucketType.user)
        async def twich(self, ctx):
            await ctx.response.defer()
            embed = discord.Embed(
                title="Twitch Link", description=config["TWITCH_URL"], color=0x0094ff, timestamp=datetime.datetime.now())
            await ctx.followup.send(embed=embed)

        @app_commands.command(name="ping", description="Gibt den Ping vom Client Zurück.")
        @commands.cooldown(1, 60, commands.BucketType.user)
        async def lul(self, ctx):
            embed = discord.Embed(title="Ping", color=0x0094ff,
                                  description=f"`Pong 🏓` `{int(ctx.client.latency * 100)} ms`", timestamp=datetime.datetime.now())
            """ embed.add_field(
                name="Ping:", value=f"`{int(ctx.client.latency * 100)}` ms") """

            await ctx.response.send_message(embed=embed)

        @app_commands.command(name="crashmsg", description="Testet die Error Message")
        async def crashtest(self, interaction):
            if interaction.user.id in config["OWNER_ID"]:
                try:
                    lol = "sdfh"
                    lolint = int(lol)
                    print(lolint)
                except Exception as error:
                    await errormessage(interaction=interaction, error=error)
            else:
                await interaction.response.send_message(content=f"Dir fehlen Berechtigungen.", ephemeral=True)

        @app_commands.command(name="ssp", description="spiele Schere-Stein-Papier gegen einen anderen User")
        @app_commands.checks.cooldown(1, 5)
        async def SSP(self, interaction, symbol: Literal['Schere', 'Stein', 'Papier'], user: discord.Member):

            class Dropdown(discord.ui.Select):
                def __init__(self):
                    options = [
                        discord.SelectOption(
                            label='Schere', description='Wähle Schere.', emoji='✂'),
                        discord.SelectOption(
                            label='Stein', description='Wähle Stein.', emoji='\U0001faa8'),
                        discord.SelectOption(
                            label='Papier', description='Wähle Papier.', emoji='📄')
                    ]

                    super().__init__(placeholder='Suche dir dein Symbol aus...',
                                     min_values=1, max_values=1, options=options)

                async def callback(self, interaction: discord.Interaction):
                    if interaction.user.id == user.id:
                        global sspauswahl
                        sspauswahl = self.values[0]
                        await msg_edit()
                    else:
                        await interaction.response.send_message("wurdest du gefragt?", ephemeral=True)

            class DropdownView(discord.ui.View):
                def __init__(self):
                    super().__init__()
                    self.add_item(Dropdown())

            view = DropdownView()
            embed = discord.Embed(title=f"{user.display_name} wurde von {interaction.user.display_name} herrausgefordert!",
                                  description=f"Nimm die Herausvorderung an indem du unten ein Symbol auswählst.", color=0x0094ff)

            await interaction.response.send_message(embed=embed, view=view)

            async def msg_edit():
                global sspwinner

                if symbol == sspauswahl:
                    ssptitle = "Unentschieden!"
                    sspdescription = f"Ihr hattet beide {sspauswahl}"

                elif symbol == "Schere" and sspauswahl == "Stein":
                    sspwinner = user.display_name
                    ssplooser = interaction.user
                    str(sspwinner)

                elif symbol == "Stein" and sspauswahl == "Papier":
                    sspwinner = user.display_name
                    ssplooser = interaction.user
                    str(sspwinner)

                elif symbol == "Papier" and sspauswahl == "Schere":
                    sspwinner = user.display_name
                    ssplooser = interaction.user
                    str(sspwinner)

                elif symbol == "Stein" and sspauswahl == "Schere":
                    ssplooser = user
                    sspwinner = interaction.user.display_name
                    str(sspwinner)

                elif symbol == "Papier" and sspauswahl == "Stein":
                    ssplooser = user
                    sspwinner = interaction.user.display_name
                    str(sspwinner)

                elif symbol == "Schere" and sspauswahl == "Papier":
                    ssplooser = user
                    sspwinner = interaction.user.display_name
                    str(sspwinner)

                if sspwinner != None:
                    ssptitle = f"{sspwinner} hat gewonnen!"
                    sspdescription = f"{ssplooser.mention} spiel doch noch eine Runde. Vielleicht gewinnst du dann ja."
                embed2 = discord.Embed(
                    title=ssptitle, description=sspdescription, color=0x0094ff)
                await interaction.edit_original_response(embed=embed2, view=None)
    except Exception as error:
        errormessage()


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        funcmds = Fun(
            name="fun", description="spiele")
        self.bot.tree.add_command(funcmds)
        print("FunCommands Geladen!")


async def setup(bot):
    await bot.add_cog(FunCog(bot))
