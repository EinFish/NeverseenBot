import discord
import asyncio
from discord.ext import commands
from typing import Union
from discord import app_commands
import utils
import datetime

class StreamerCommands(discord.app_commands.Group):
    @app_commands.command(name="add", description="adds a Streamer to the Notification List")
    async def add(self, interaction: discord.Interaction, channel: Union[discord.TextChannel, discord.Thread], ping: discord.Role = None):
        if interaction.user.guild_permissions.administrator:
            streamer = "neverseen_tv"
            sjson = utils.serverjson()
            dict = sjson[str(interaction. guild. id)]["watchlist"]
            if streamer in dict.keys():
                del sjson[str(interaction. guild.id)]["watchlist"][streamer]
            if ping != None:
                ping = ping.id
            new_streamer = {streamer.lower(): {"channel": channel.id, "ping": ping}}
            dict.update(new_streamer)
            sjson[str(interaction. guild.id)]["watchlist"] = dict
            utils.savejson(sjson, 'serverconfig')
            await interaction.response.send_message(content=utils.buildsentence(interaction.guild.id, "done"))
        else:
            await interaction.response.send_message(content=utils.buildsentence(interaction.guild.id, "No_Permission"))


    @app_commands.command(name="remove", description="remove's a Streamer from the Notification List")
    async def remove_streamer(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            sjson = utils.serverjson()
            try:
                del sjson[str(interaction. guild. id)]["watchlist"]["neverseen_minecraft"]
            except KeyError:
                await interaction.response.send_message(content=utils.buildsentence(interaction.guild.id, "sremoveerr1", "streamer"))
                return 
            utils.savejson(sjson, 'serverconfig')
            await interaction.response.send_message(content=utils.buildsentence(interaction.guild.id, "done"))
        else:
            await interaction.response.send_message(content=utils.buildsentence(interaction.guild.id, "No_Permission"))


    @app_commands.command(name="list", description="Display's a list of the Streamers for this Server")
    async def list(self, interaction: discord.Interaction):
        sjson = utils.serverjson()
        streamer = sjson[str(interaction.guild.id)]["watchlist"]
        user_login = list(streamer.keys())
        p = 0
        embed = discord.Embed(title=utils.buildsentence(interaction.guild.id, "slistt", "streamer").format(interaction.guild.name), color=0x7A50BE, timestamp=datetime.datetime.now())
        for i in range(len(user_login)):
            channel = interaction.guild.get_channel(sjson[str(interaction.guild.id)]["watchlist"][user_login[p]]["channel"])
            try:
                ping = interaction.guild.get_role(sjson[str(interaction.guild.id)]["watchlist"][user_login[p]]["ping"])
                ping2 = ping.mention
            except:
                ping2 = "None"
            embed.add_field(name=f"{user_login[p]}:", value="Channel: {}\nPing: {}".format(channel.mention, ping2), inline=False)
            p+=1
        await interaction.response.send_message(embed=embed)
        




class StreamerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        strcmd = StreamerCommands(name="streamer", description="Commands for the Twitch Notifications")
        self.bot.tree.add_command(strcmd)
        print("StreamerCommands Geladen!")

async def setup(bot):
    await bot.add_cog(StreamerCog(bot))