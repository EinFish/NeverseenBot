import asyncio
import datetime
import discord
from discord.ext import commands
import json
import sys
import time


with open("reactions.json") as file:
    rjson = json.load(file)


class Automod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Listeners geladen!")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open("serverconfig.json") as file:
            sjson = json.load(file)
        guildid = after.guild.id
        if not before.author.bot:
            try:
                channel = after.guild.get_channel(
                    int(sjson[str(guildid)]["logchannel"]))
                embed = discord.Embed(title="Nachricht bearbeitet", description="eine nachricht von " +
                                      before.author.name + " wurde bearbeitet.", color=0x0094ff, timestamp=datetime.datetime.now())
                embed.add_field(
                    name="Vorher:", value=before.content, inline=True)
                embed.add_field(name="Nachher:",
                                value=after.content, inline=True)
                embed.add_field(name="Channel:",
                                value=after.jump_url, inline=True)
                await channel.send(embed=embed)
            except KeyError:
                pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = message.guild.id
        try:
            channel = message.guild.get_channel(
                int(sjson[str(guildid)]["logchannel"]))
            embed = discord.Embed(title="Nachricht gelöscht",
                                  description=f"eine nachricht von {message.author.mention} wurde Gelöscht", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Nachricht:",
                            value=message.content, inline=True)
            embed.add_field(name="Channel:",
                            value=message.channel.jump_url, inline=True)
            await channel.send(embed=embed)
        except KeyError:
            pass

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

        with open("serverconfig.json", 'w') as json_file:
            json.dump(sjson, json_file, indent=4)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        with open("serverconfig.json") as file:
            sjson = json.load(file)

        guildid = member.guild.id

        try:
            logchannelid = sjson[str(guildid)]["logchannel"]
            logchannel = await member.guild.fetch_channel(logchannelid)
            created = member.created_at
            created2 = time.mktime(created.timetuple())
            created3 = int(created2)
            embed = discord.Embed(
                title="User Verlassen", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Created:",
                            value=f"<t:{str(created3)}:D>")
            embed.add_field(name="User ID:", value=member.id)
            embed.add_field(name="User Name:", value=member.mention)
            embed.set_thumbnail(url=member.avatar)
            await logchannel.send(embed=embed)
        except KeyError:
            pass

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        async for bot_entry in guild.audit_logs(action=discord.AuditLogAction.bot_add, limit=1):
            user = bot_entry.user

            try:
                dm_channel = await user.create_dm()
                await dm_channel.send("Hey, \ndanke das du mich hinzugefügt hast. \nDamit du mich vollständig nutzen kannst, führe doch bitte `/admin setup` aus.\n \nFür Support kannst du gerne auf meinen Entwickler Discord kommen: \nhttps://discord.gg/KP59K8kkUW")
            except discord.Forbidden:
                pass

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open("serverconfig.json") as file:
            sjson = json.load(file)
        guildid = member.guild.id
        try:
            logchannelid = sjson[str(guildid)]["logchannel"]
            logchannel = await member.guild.fetch_channel(logchannelid)
        except KeyError:
            pass

        try:

            if sjson[str(guildid)]["welcome"] != "None":
                titel = sjson[str(guildid)]["welcome"]["title"]
                beschreibung = sjson[str(guildid)]["welcome"]["description"]
                membercount = sjson[str(guildid)]["welcome"]["membercount"]
                timestamp = sjson[str(guildid)]["welcome"]["timestamp"]
                usermention = sjson[str(guildid)]["welcome"]["usermention"]
                profilepicture = sjson[str(
                    guildid)]["welcome"]["profilepicture"]

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
                try:
                    logchannelid = sjson[str(guildid)]["logchannel"]
                    logchannel = await member.guild.fetch_channel(logchannelid)
                    created = member.created_at
                    created2 = time.mktime(created.timetuple())
                    created3 = int(created2)
                    embed = discord.Embed(
                        title="User Beigetreten", color=0x0094ff, timestamp=datetime.datetime.now())
                    embed.add_field(name="Created:",
                                    value=f"<t:{str(created3)}:D>")
                    embed.add_field(name="User ID:", value=member.id)
                    embed.add_field(name="User Name:", value=member.mention)
                    embed.set_thumbnail(url=member.avatar)
                    await logchannel.send(embed=embed)
                except Exception as error:
                    print(error)

        except:
            try:
                await logchannel.send(content="Willkommensnachrichten nicht eingerichtet!")
            except:
                pass


async def setup(bot):
    await bot.add_cog(Automod(bot))
