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
    async def bewerben(self, ctx, message: int):
        if ctx.author.guild_permissions.administrator:
            id = ctx.guild.id
            print(message)
            sjson[str(id)]['bewechannel'] = message
            with open("serverconfig.json", "w") as file:
                json.dump(sjson, file, indent=4)
        else:
            await ctx.reply(rjson['catnewspaper'])


async def setup(bot):
    await bot.add_cog(BewerbenCog(bot))
