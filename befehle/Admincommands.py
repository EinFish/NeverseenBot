import asyncio
import discord
from discord.ext import commands
import json

with open('serverconfig.json') as file:
    sjson = json.load(file)

with open('config.json') as file2:
    config = json.load(file2)


class AdminCommands(discord.app_commands.Group):
    pass


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        admincmds = AdminCommands(
            name="admin", description="Befehle für admins")
        self.bot.tree.add_command(admincmds)
        print("AdminCommands Geladen!")

    @commands.command()
    async def sync(self, ctx) -> None:
        id = config["OWNER_ID"]
        id2 = int(id)
        if ctx.author.id != id2:
            await ctx.send("Das solltest du besser lassen :)")
            return
        print("started sync")
        fmt = await ctx.bot.tree.sync()
        await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} Befehle wurden gesynced.")
        print("finished sync")

   


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
