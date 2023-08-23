import asyncio
import datetime
import discord
from discord.ext import commands
import json

with open("serverconfig.json") as file:
    sjson = json.load(file)

class Automod(commands.Cog):
    banned_words = ["hs", "Hurensohn", "töst"]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Automod geladen!")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        guildid = before.guild.id
        if not before.author.bot:
            channel = after.guild.get_channel(int(sjson[str(guildid)]["log"]))
            embed = discord.Embed(title="Nachricht bearbeitet", description="eine nachricht von " + before.author.name + " wurde bearbeitet.", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Vorher:", value=before.content, inline=True)
            embed.add_field(name="Nachher:", value=after.content, inline=True)
            embed.add_field(name="Channel:", value=after.jump_url, inline=True)
            await channel.send(embed=embed)
            print("nachricht bearbeitet")
            print("Vorher: " + before.content)
            print("Nachher: " + after.content)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guildid = message.guild.id
        channel = message.guild.get_channel(int(sjson[str(guildid)]["log"]))
        embed = discord.Embed(title="Nachricht gelöscht", description="eine nachricht von " + message.author.name + " wurde von " + message + "", color=0x0094ff, timestamp=datetime.datetime.now())
        embed.add_field(name="Nachricht:", value=message.content, inline=True)
        embed.add_field(name="Channel:", value=message.channel.jump_url, inline=True)
        await channel.send(embed=embed)
        print("nachricht gelöscht")
        print(message.content)



    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content in self.banned_words:
            await message.delete()
            await message.author.ban()




async def setup(bot):
    await bot.add_cog(Automod(bot))