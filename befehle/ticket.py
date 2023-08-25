import asyncio
import discord
from discord.ext import commands


class Tickets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Tickets geladen!")


async def setup(bot):
    await bot.add_cog(Tickets(bot))
