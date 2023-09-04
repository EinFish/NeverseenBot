import asyncio
import discord
from typing import Any
from discord.ext import commands
import json
from discord import app_commands


class BewerbenCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bewerbung geladen!")

    @commands.command()
    async def bewerben(self, ctx, message: int):
        with open("reactions.json") as file:
            rjson = json.load(file)
        with open("serverconfig.json") as file:
            sjson = json.load(file)
        if ctx.author.guild_permissions.administrator:
            id = ctx.guild.id
            sjson[str(id)]['bewechannel'] = message
            with open("serverconfig.json", "w") as file:
                json.dump(sjson, file, indent=4)
        else:
            await ctx.reply(rjson['catnewspaper'])


async def setup(bot):
    await bot.add_cog(BewerbenCog(bot))
