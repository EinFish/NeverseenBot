import asyncio
import datetime
import discord
from discord.ext import commands
import json
import sys


with open("reactions.json") as file:
    rjson = json.load(file)


class Automod(commands.Cog):
    banned_words = ["hs", "Hurensohn", "töst"]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Listeners geladen!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if "test" in message.content.lower():
                await message.reply(content="test bestanden")

            if "xd" in message.content.lower():
                await message.add_reaction(rjson["youtube"])

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open("serverconfig.json") as file:
            sjson = json.load(file)
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
        with open("serverconfig.json") as file:
            sjson = json.load(file)

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
    async def on_guild_remove(self, guild):
        with open("serverconfig.json") as file:
            sjson = json.load(file)
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
                await dm_channel.send("Hey, \ndanke das du mich hinzugefügt hast. \nDamit du mich vollständig nutzen kannst, führe doch bitte `/admin setup` aus.\n \nFür Support kannst du gerne auf meinen Entwickler Discord kommen: \nhttps://discord.gg/KP59K8kkUW")
            except discord.Forbidden:
                print(
                    "Konnte keine Direktnachricht senden, da der Benutzer DMs deaktiviert hat.")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = member.guild.id

        if sjson[str(guildid)]["welcome"] != "None":
            titel = sjson[str(guildid)]["welcome"]["title"]
            beschreibung = sjson[str(guildid)]["welcome"]["description"]
            membercount = sjson[str(guildid)]["welcome"]["membercount"]
            timestamp = sjson[str(guildid)]["welcome"]["timestamp"]
            usermention = sjson[str(guildid)]["welcome"]["usermention"]
            profilepicture = sjson[str(guildid)]["welcome"]["profilepicture"]

            welcomechannelid = sjson[str(guildid)]["welcome"]["channel"]
            welcomechannel = await member.guild.fetch_channel(welcomechannelid)

            if usermention == True:
                welcome_embed = discord.Embed(title=f"Herzlich Willkommen {member.display_name}",
                                              description=f"Willkommen in der Neverseen Community {member.mention}", color=0x0094ff)
                if timestamp == True:
                    welcome_embed = discord.Embed(
                        title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", color=0x0094ff, timestamp=datetime.datetime.now())
                        members = member.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=member.avatar)
                if membercount == True:
                    welcome_embed = discord.Embed(
                        title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", color=0x0094ff)
                    members = member.guild.member_count
                    welcome_embed.add_field(
                        name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=member.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = member.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                if profilepicture == True:
                    welcome_embed = discord.Embed(
                        title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", color=0x0094ff)
                    welcome_embed.set_thumbnail(
                        url=member.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", timestamp=datetime.datetime.now(), color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=member.avatar)
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=f"Herzlich Willkommen {member.display_name}", description=f"Willkommen in der Neverseen Community {member.mention}", timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = member.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                        welcome_embed.set_thumbnail(
                            url=member.avatar)

            else:
                welcome_embed = discord.Embed(
                    title=titel, description=beschreibung, color=0x0094ff)
                if timestamp == True:
                    welcome_embed = discord.Embed(
                        title=titel, description=beschreibung, color=0x0094ff, timestamp=datetime.datetime.now())
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, color=0x0094ff, timestamp=datetime.datetime.now())
                        members = member.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=member.avatar)
                if membercount == True:
                    welcome_embed = discord.Embed(
                        title=titel, description=beschreibung, color=0x0094ff)
                    members = member.guild.member_count
                    welcome_embed.add_field(
                        name=f"Member: #{members}", value="")
                    if profilepicture == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=member.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = member.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                if profilepicture == True:
                    welcome_embed = discord.Embed(
                        title=titel, description=beschreibung, color=0x0094ff)
                    welcome_embed.set_thumbnail(
                        url=member.avatar)
                    if timestamp == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, timestamp=datetime.datetime.now(), color=0x0094ff)
                        welcome_embed.set_thumbnail(
                            url=member.avatar)
                    if membercount == True:
                        welcome_embed = discord.Embed(
                            title=titel, description=beschreibung, timestamp=datetime.datetime.now(), color=0x0094ff)
                        members = member.guild.member_count
                        welcome_embed.add_field(
                            name=f"Member: #{members}", value="")
                        welcome_embed.set_thumbnail(
                            url=member.avatar)

            await welcomechannel.send(embed=welcome_embed)
            print("dfj")


async def setup(bot):
    await bot.add_cog(Automod(bot))
