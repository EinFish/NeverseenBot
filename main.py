import discord
import datetime
import time
import os
import asyncio
import json
from discord.ext import commands
from discord.ext.tasks import loop
from twitch import get_notifications

with open("config.json", "r") as file:
    config = json.load(file)


bot = commands.Bot("neverseen.", intents=discord.Intents.all(),
                   application_id=config["APP_ID"])


if __name__ == "__main__":
    print(discord.__version__)
    for extension in os.listdir(os.fsencode("befehle")):
        if os.fsdecode(extension).endswith(".py"):
            try:
                asyncio.run(bot.load_extension(
                    f"befehle.{os.fsdecode(extension)[:-3]}"))
            except:
                print(
                    f"Die extension {os.fsdecode(extension)[:-3]} konnte nicht geladen werden.")
                raise


@loop(seconds=90)
async def check_twitch_online_streamers():
    channel = bot.get_channel(1063958884605243524)
    if not channel:
        return
    notifications = get_notifications()
    for notification in notifications:
        embed = discord.Embed(title="{} ist jetzt live".format(
            notification["user_name"]), color=0x0094ff, timestamp=datetime.datetime.now())
        embed.add_field(name="{}".format(
            notification["title"]), inline=False, value="")
        embed.add_field(name="{}".format(
            notification["game_name"]), value="{}".format(notification["tags"]))
        embed.set_thumbnail(url="{}".format(notification["thumbnail_url"]))
        await channel.send("streamer {} ist jetzt online: {}".format(notification["user_login"], notification))
        await channel.send(embed=embed)


@loop(seconds=10)
async def presences():
    c = 1
    while (True):
        if (c == 1):
            await bot.change_presence(activity=discord.Game(name="die Konsole durch"))

        elif (c == 2):
            await bot.change_presence(activity=discord.Game(name="bald Musik"))

        elif (c == 3):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dir über die Schulter"))

        elif (c == 4):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="guter Musik"))

        elif (c == 5):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dem Chat zu"))

        elif (c == 6):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dir über die Schulter"))

        elif (c == 7):
            await bot.change_presence(activity=discord.Streaming(name="Neverseen_Minecraft", url=config["TWITCH_URL"]))

        c += 1
        if (c > 7):
            c = 1
        await asyncio.sleep(30)


@loop(hours=1)
async def birthdayloop():
    with open("serverconfig.json") as file:
        sjson = json.load(file)

    with open("users.json") as file:
        bjson = json.load(file)

    currenttime = datetime.datetime.fromtimestamp(
        int(time.time())).strftime('%H')
    if currenttime == "8":  # Es ist 3 Uhr morgends
        try:
            config = sjson  # config laden
            for server in config:
                try:

                    roleid = int(config[server]["bdayrole"])
                    channelid = int(config[server]["bday"])

                    # <- Wenn es einen Ping geben soll
                    pingid = int(config[server]["bdayrole"])
                    guild = bot.get_guild(int(server))

                    birthdayconfig = bjson  # Birthdayconfig von den Server laden

                    birthdayMembers = []
                    daytoday = datetime.datetime.now().strftime("%d")  # Heutiger Tag
                    monthtoday = datetime.datetime.now().strftime("%m")  # Heutiger Monat
                    for member in guild.members:
                        try:
                            bday = birthdayconfig[str(member.id)]["bday"]
                            if str(daytoday) == bday.split("/")[0] and str(monthtoday) == bday.split("/")[1]:
                                birthdayMembers.append(member)
                        except:
                            pass  # Mitglied hat den geburtstag nicht eingetragen
                    if len(birthdayMembers) == 0:
                        continue  # Es hat heute niemand auf den Server geburtstag

                    try:
                        role = guild.get_role(roleid)
                        for member in birthdayMembers:
                            try:
                                await member.add_roles(role)
                            except:
                                pass  # Der Bot darf den Member nicht bearbeiten
                    except:
                        pass  # Die Rolle existiert nicht

                    try:

                        # <- Wenn ping gewünscht
                        content = guild.get_role(int(pingid)).mention
                        pass
                    except:
                        content = None

                    channel = guild.get_channel(channelid)
                    birthdayPings = ""
                    for member in birthdayMembers:
                        birthdayPings += f"{member.mention} "
                    await channel.send(embed=discord.Embed(title="Herzlichen Glückwunsch!", description=f"{birthdayPings} {'Hat' if len(birthdayMembers) == 1 else 'Haben'} heute Geburtstag!!!", color=0x0094ff), content=content)
                except:
                    pass
        except:
            pass


@bot.event
async def on_ready():
    print("Bot is running!")
    check_twitch_online_streamers.start()
    presences.start()
    birthdayloop.start()


bot.run(config["TOKEN"])
