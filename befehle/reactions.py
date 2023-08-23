import asyncio
import discord
from discord.ext import commands
import json

with open("reactions.json") as file:
    rjson = json.load(file)

class Reactions(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Reactions geladen!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if "test" in message.content.lower():
                await message.reply(content="test bestanden")

            if "xd" in message.content.lower():
               await message.add_reaction(rjson["youtube"])



async def setup(bot):
    await bot.add_cog(Reactions(bot))