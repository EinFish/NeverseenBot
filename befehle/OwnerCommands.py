import discord
from discord.ext import commands
from discord import app_commands, ui
import json
import utils
from discord.ext.tasks import loop


with open("config.json") as file:
    config = json.load(file)



@loop(seconds=10)
async def status(self):
    bot = self.bot
    member = bot.get_guild(1063567516737224805).get_member(959798444195721226)
    role = bot.get_guild(1063567516737224805).get_role(1086378080311972001)
    if str(member.status) == "offline":
        channel = await bot.fetch_channel(1086735918494404651)
        await channel.send(f"{role.mention} Gyra ist Offline!")
        status.stop()


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        status.start(self)
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

    @commands.command()
    async def gyra_start(self, ctx):
        id = [753863284448428102, 849300381186916423]
        if ctx.author.id not in id:
            await ctx.send("Das solltest du besser lassen :)")
            return
        status.start(self)
        await ctx.send("Loop Started")


async def setup(bot):
    await bot.add_cog(OwnerCog(bot))
