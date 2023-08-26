import asyncio
import discord
from typing import Any
from discord.ext import commands
import json
from discord import app_commands

with open("reactions.json") as file:
    rjson = json.load(file)


with open("serverconfig.json") as file:
    sjson = json.load(file)


""" class TicketButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle):
        super().__init__(label=text, style=discordbuttonstyle)

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_modal(TicketModal())


class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton("Bewerben",
                      discord.ButtonStyle.success)) """


class BewerbenCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bewerbung geladen!")

    @commands.command()
    async def bewerben(self, ctx):
        if ctx.author.guild_permissions.administrator:
            id = ctx.guild.id
            channelid = sjson[str(id)]['bewerben']
            channel = self.bot.get_channel(channelid)
            text = "Klicke auf den unteren Knopf um dich zu Bewerben."
            embed = discord.Embed(
                title="Bewerben", description=text, color=0x0094ff)
            await ctx.reply(content="erstellt", ephemeral=True)
          #  await channel.send(embed=embed, view=TicketView())
        else:
            await ctx.reply(rjson['catnewspaper'])

    @commands.command()
    async def channel_bewerben(self, ctx):
        print("dfj")


async def setup(bot):
    await bot.add_cog(BewerbenCog(bot))
