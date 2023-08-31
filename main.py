import discord
import sys
import os
import asyncio
import json
from discord.ext import commands

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


@bot.event
async def on_ready():
    print("Bot ist ready!")
    c = 1
    while (True):
        if (c == 1):
            await bot.change_presence(activity=discord.Game(name="die Konsole durch"))

        elif (c == 2):
            await bot.change_presence(activity=discord.Streaming(name="Neverseen Minecraft", url="twitch.tv/neverseen_minecraft"))

        elif (c == 3):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="guter Musik"))

        elif (c == 4):
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="dem Chat zu"))

        elif (c == 5):
            await bot.change_presence(activity=discord.Streaming(name="omg", url=config["TWITCH_URL"]))

        c += 1
        if (c > 5):
            c = 1
        await asyncio.sleep(30)


bot.run(config["TOKEN"])
