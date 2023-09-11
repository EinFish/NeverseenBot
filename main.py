import discord
import sys
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
        await channel.send("streamer {} ist jetzt online: {}".format(notification["user_login"], notification))


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


@bot.event
async def on_ready():
    print("Bot is running!")
    check_twitch_online_streamers.start()
    presences.start()


bot.run(config["TOKEN"])
