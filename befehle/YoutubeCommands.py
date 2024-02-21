import discord
import asyncio
from discord.ext import commands, tasks
from typing import Union, Literal
from discord import app_commands
import utils
import datetime
import scrapetube


class YoutubeCommands(discord.app_commands.Group):
    @app_commands.command(name="add", description="Fügt Video Benachrichtigungen vom Youtube Kanal von Neverseen_TV hinzu.")
    async def add(self, interaction: discord.Interaction, youtuber: Literal["NiemalsGesehen", "neverseen_tv"], channel: Union[discord.TextChannel, discord.Thread], ping: discord.Role = None):
        if not interaction.user.guild_permissions.administrator:
            return interaction.response.send_message("Du bist nicht berechtigt dazu.", ephemeral=True)
        sjson = utils.serverjson()
        sjson[str(interaction.guild.id)]["youtuber"][youtuber] = {"url": f"https://youtube.com/@{youtuber}", "kanal": channel.id, "ping" : str(ping.id) if ping != None else ""}
        utils.savejson(sjson, 'serverconfig')
        await interaction.response.send_message(f"Youtuber {youtuber} erfolgreich zur Liste hinzugefügt!", ephemeral=True)

    @app_commands.command(name="remove", description="Entfernt einen Youtube Kanal von Neverseen_TV")
    async def remove(self, interaction: discord.Interaction, youtuber: Literal["NiemalsGesehen", "neverseen_tv"]):
        if not interaction.user.guild_permissions.administrator:
            return interaction.response.send_message("Du bist nicht berechtigt dazu.", ephemeral=True)
        sjson = utils.serverjson()
        del sjson[str(interaction.guild.id)]["youtuber"][youtuber]
        utils.savejson(sjson, 'serverconfig')
        await interaction.response.send_message("Erfolgreich entfernt.", ephemeral=True)

    @app_commands.command(name="list", description="Zeigt die Kanal liste mit Infos an")
    async def show(self, interaction: discord.Interaction):
        sjson = utils.serverjson()
        embed = discord.Embed(title=f"Youtuber Liste von {interaction.guild.name}", timestamp=datetime.datetime.now(), color=0x0094ff)
        yt = sjson[str(interaction.guild.id)]["youtuber"]
        if yt == {}:
            return await interaction.response.send_message("Es steht kein Kanal auf der Liste.", ephemeral=True)
        for i in list(yt.values()):
            name = i["url"].split("@")[1]
            url = i["url"]
            ping = await interaction.guild.fetch_roles(i["ping"])
            kanal = await interaction.guild.fetch_channel(i["kanal"])
            embed.add_field(name=f"Youtube Kanal: {name}\n({url})\n", value=f"Discord Kanal: {kanal.mention}\nRolle: {ping.mention}", inline=False)

        await interaction.response.send_message(embed=embed)
        

class YoutubeCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.videos = {}

    @tasks.loop(seconds=30)
    async def check(self):
        sjson = utils.serverjson()
        for i in sjson.values():
            i = i["youtuber"]
            try:
                discord_channel = self.bot.get_channel(list(list(i.values())[0].values())[1])
            except:
                discord_channel = None

            for channel_url in list(i.values()):
                videos = scrapetube.get_channel(channel_url=channel_url["url"], limit=5)
                video_ids = [video["videoId"] for video in videos]
                if self.check.current_loop == 0:
                    self.videos[channel_url["url"].split("@")[1]] = video_ids
                    continue
            
            for video_id in video_ids:
                if video_id not in self.videos[channel_url["url"].split("@")[1]]:
                    ping = discord_channel.guild.get_role(int(channel_url["ping"])).mention if channel_url["ping"] != "" else ""
                    youtuber = channel_url["url"].split("@")[1]
                    url = f"https://youtu.be/{video_id}"
                    await discord_channel.send(f"{ping} {youtuber} hat ein neues Video Hochgeladen!\n{url}")
            self.videos[channel_url["url"].split("@")[1]] = video_ids


    @commands.Cog.listener()
    async def on_ready(self):
        strcmd = YoutubeCommands(name="youtuber", description="Commands for the Youtube Notifications")
        self.bot.tree.add_command(strcmd)
        print("YoutubeCommands Geladen!")
        self.check.start()

async def setup(bot):
    await bot.add_cog(YoutubeCog(bot))