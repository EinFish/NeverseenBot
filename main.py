import discord
import datetime
import time
import os
import asyncio
import json
import utils
from befehle import commands as cmds
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
    sjson = utils.serverjson()
    notifications = get_notifications()
    for notification in notifications:
        image = "{}".format(notification["thumbnail_url"]).replace(
            "{width}x{height}", "1920x1080")
        liste = notification["tags"]
        tags = "Tags: "
        for i in liste:
            tags += i + ", "
        embed = discord.Embed(title="{} ist jetzt live".format(
            notification["user_name"]), color=0x7A50BE, timestamp=datetime.datetime.now())
        embed.add_field(name="{}".format(
            notification["title"]), inline=False, value="")
        embed.add_field(name="{} | {} | Viewer: {}".format(
            notification["game_name"], notification["language"], notification["viewer_count"]), value="{}".format(tags))
        embed.set_image(url=image)
        for server in sjson:
            ping = sjson[server]["watchlist"][notification["user_login"]]["ping"]
            try:
                channel = bot.get_channel(
                    sjson[server]["watchlist"][notification["user_login"]]["channel"])
            except KeyError:
                pass
            try:
                content = channel.guild.get_role(ping).mention
            except:
                content = None
            if not channel:
                pass
            await channel.send(embed=embed, content=content)


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
            if config["TWITCH_URL"] == "skip":
                c = 1
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
    if currenttime == "08":  # Es ist 3 Uhr morgends
        try:
            config = sjson  # config laden
            for server in config:
                try:
                    try:
                        roleid = int(config[server]["bdayrole"])
                        channelid = int(config[server]["bday"])
                    except:
                        pass

                    # pingid = int(config[server]["bdayrole"]) <- Wenn es einen Ping geben soll
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

                        # content = guild.get_role(int(pingid)).mention <- Wenn ping gewünscht
                        content = None
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
    
    check_twitch_online_streamers.start()
    presences.start()
    birthdayloop.start()
    print("Loop's started!")
    bot.add_view(cmds.TicketView())
    bot.add_view(cmds.TicketView2())
    bot.add_view(utils.BewerbenView())
    print("Added Views!")
    print(10* "-")
    print("Bot is running!")


bot.run(config["TOKEN"])
