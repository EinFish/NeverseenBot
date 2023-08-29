import asyncio
import datetime
import discord
from discord.ext import commands
import json
import sys

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
            channel = after.guild.get_channel(
                int(sjson[str(guildid)]["log"]))
            embed = discord.Embed(title="Nachricht bearbeitet", description="eine nachricht von " +
                                  before.author.name + " wurde bearbeitet.", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Vorher:", value=before.content, inline=True)
            embed.add_field(name="Nachher:", value=after.content, inline=True)
            embed.add_field(name="Channel:", value=after.jump_url, inline=True)
            await channel.send(embed=embed)
            print("nachricht bearbeitet")
            print("Vorher: " + before.content)
            print("Nachher: " + after.content)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        guild = message.guild
        async for bot_entry in guild.audit_logs(action=discord.AuditLogAction.message_delete, limit=1):
            user = bot_entry.user
            print(bot_entry)

        guildid = message.guild.id
        channel = message.guild.get_channel(
            int(sjson[str(guildid)]["log"]))
        embed = discord.Embed(title="Nachricht gelöscht",
                              description=f"eine nachricht von {message.author.mention} wurde von {user.mention} Gelöscht", color=0x0094ff, timestamp=datetime.datetime.now())
        embed.add_field(name="Nachricht:", value=message.content, inline=True)
        embed.add_field(name="Channel:",
                        value=message.channel.jump_url, inline=True)
        await channel.send(embed=embed)
        print("nachricht gelöscht")
        print(message.content)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content in self.banned_words:
            await message.delete()
            await message.author.ban()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        guildid = guild.id
        guildid2 = str(guildid)
        try:
            del sjson[guildid2]
        except KeyError:
            pass
        print("dfj")

        with open("serverconfig.json", 'w') as json_file:
            json.dump(sjson, json_file, indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print("dfj lol")

        async for bot_entry in guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=1):
            user = bot_entry.user
            print(bot_entry)

            try:
                dm_channel = await user.create_dm()
                await dm_channel.send("Hey, \ndanke das du mich Hinzugefügt hast. \nDamit du mich vollständig nutzen kannst, führe doch bitte `/ admin setup` aus.\n \nFür support kannst du gerne auf meinen Entwickler Discord kommen: \nhttps://discord.gg/KP59K8kkUW")
            except discord.Forbidden:
                print(
                    "Konnte keine Direktnachricht senden, da der Benutzer DMs deaktiviert hat.")


async def setup(bot):
    await bot.add_cog(Automod(bot))
