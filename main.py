import discord
import os
import asyncio
import json
from discord.ext import commands

bot = commands.Bot("neverseen.", intents=discord.Intents.all(),
                   application_id="1135990698517221376")


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
    await bot.change_presence(activity=discord.Streaming(name="omg", url="https://www.twitch.tv/lefish9873"))

with open("config.json", "r") as file:
    config = json.load(file)

bot.run(config["TOKEN"])
