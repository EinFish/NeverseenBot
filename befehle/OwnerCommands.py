import discord
from discord.ext import commands
from discord import app_commands, ui
import json
import utils


with open("config.json") as file:
    config = json.load(file)


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("OwnerCommands Geladen!")

    @commands.command()
    async def sync(self, ctx) -> None:
        id = config["OWNER_ID"]
        # id2 = int(id)
        if ctx.author.id not in id:
            await ctx.send("Das solltest du besser lassen :)")
            return
        print("started sync")
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} Gruppen wurden gesynced.")
        print("finished sync")

    @commands.command()
    async def twitch_access(self, ctx):
        id = config["OWNER_ID"]
        if ctx.author.id not in id:
            await ctx.send("Das solltest du besser lassen :)")
            return
        tconfig = utils.twitchconfig()
        access_token = utils.get_app_access_token()
        tconfig["access_token"] = access_token
        utils.savejson(tconfig, 'twitch')
        await ctx.send("Token gesetzt!")


async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
