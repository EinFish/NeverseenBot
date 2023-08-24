import asyncio
import discord
from discord.ext import commands
from discord import app_commands
import json

with open("serverconfig.json") as file:
    sjson = json.load(file)

with open("config.json") as file:
    config = json.load(file)

with open("reactions.json") as file:
    rjson = json.load(file)


class AdminCommands(discord.app_commands.Group):
    @app_commands.command(name="setup", description="Passe die Einstellungen des Bots an deinen Server an")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def setupserver(self, interaction, modrole: discord.Role, logchannel: discord.TextChannel = None, birthdaychannel: discord.TextChannel = None, welcomechannel: discord.TextChannel = None, birthdayrole: discord.Role = None):
        await interaction.response.defer()
        if interaction.user.guild_permissions.administrator:
            guildid = interaction.guild.id
            guildname = interaction.guild.name
            birthdayrole2 = ""
            modrole2 = modrole.mention
            if birthdayrole != None: birthdayrole2 = birthdayrole.mention
            if welcomechannel == None: welcomechannel = "None"
            print(modrole2)
            sjson[str(guildid)] = {"name": guildname, "modrole": modrole2}
            if logchannel != None: sjson[str(guildid)]["bday"] = birthdaychannel.id
            if logchannel != None: sjson[str(guildid)]["logchannel"] = logchannel.id
            if welcomechannel != "None": sjson[str(guildid)]["welcome"] = welcomechannel.id
            else: sjson[str(guildid)]["welcome"] = welcomechannel
            if birthdayrole2 != "": sjson[str(guildid)]["bdayrole"] = birthdayrole2
            with open("serverconfig.json", "w") as json_file:
                json.dump(sjson, json_file, indent=4)

            print("sdj")
        else:
            interaction.followup.send(content=f"{rjson['catnewspaper']}", ephemeral=True)

    @app_commands.command(name="welcome-embed", description="Legt die willkommensnachricht fest.")
    @commands.cooldown(1, 30, commands.BucketType.guild)
    async def wmessage(self, interaction, titel: str, beschreibung: str = None, farbe: str = None, membercount: bool = False,):
        guildid = interaction.guild.id
        await interaction.response.defer()
        if interaction.user.guild_permissions.administrator:
            if sjson[str(guildid)]["welcome"] != "None":
                print("dfj")


            else:
                await interaction.followup.send(content="Bitte lege erst den welcome channel fest mit `/admin setup`", ephemeral=True)
                print("dfj")
            print("dfj")

        else:
            interaction.followup.send(
                content=f"{rjson['catnewspaper']}", ephemeral=True
            )


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        admincmds = AdminCommands(name="admin", description="Befehle für admins")
        self.bot.tree.add_command(admincmds)
        print("AdminCommands Geladen!")

    @commands.command()
    async def sync(self, ctx) -> None:
        id = config["OWNER_ID"]
        id2 = int(id)
        if ctx.author.id != id2:
            await ctx.send("Das solltest du besser lassen :)")
            return
        print("started sync")
        fmt = await ctx.bot.tree.sync()
        await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} Befehle wurden gesynced.")
        print("finished sync")


async def setup(bot):
    await bot.add_cog(AdminCog(bot))
