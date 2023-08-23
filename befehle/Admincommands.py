import asyncio
import discord
from discord.ext import commands
import json

with open('serverconfig.json') as file:
    sjson = json.load(file)


class AdminCommands(discord.app_commands.Group):
    pass


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        admincmds = AdminCommands(
            name="Admin", description="Befehle für admins")
        self.bot.tree.add_command(admincmds)
        print("AdminCommands Geladen!")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
