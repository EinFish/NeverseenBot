import discord
from discord.ext import commands
from discord import app_commands, ui
from googletrans import Translator
import json
import googletrans
from utils import EmbedBuilder
import datetime


class bugReportModal(ui.Modal, title="Bugreport"):
    command = ui.TextInput(label="in welchem Befehl tritt der Bug auf?",
                           style=discord.TextStyle.short, placeholder="/fun twitch", required=True, max_length=255)
    excepted = ui.TextInput(label="Was hast du von dem Befehl erwartet?", style=discord.TextStyle.long,
                            placeholder="Informationen über einen Twitch Streamer", required=True, max_length=255)
    actual = ui.TextInput(label="Was hat dir der Befehl zurückgegeben?", style=discord.TextStyle.long,
                          placeholder="Nichts. Es lädt nur für immer", required=True, max_length=1024)
    reproduce = ui.TextInput(label="Was hast du gemacht, dass der Bug auftritt?",
                             style=discord.TextStyle.long, placeholder="Den Befehl ausgeführt", required=True, max_length=1024)
    extra = ui.TextInput(label="Sonst noch etwas, das wichtig ist?",
                         style=discord.TextStyle.long, placeholder="", required=False, max_length=1024)

    async def on_submit(self, interaction) -> None:
        with open('config.json') as file:
            config = json.load(file)
        recivers = config["OWNER_ID"]
        for reciver in recivers:
            reciv = interaction.client.get_user(reciver)
            await reciv.send(embed=discord.Embed(title="Bugreport", description=f"Bug reportet von {interaction.user} ({interaction.user.id})\n```\nBefehl: {self.command}\n\nerwartet: {self.excepted}\n\ntatsächlich: {self.actual}\n\nreproduce: {self.reproduce}\n\nExtra: {self.extra}\n```", color=0x0094ff))
        embed = discord.Embed(
            title="Danke", description="Der Bug wurde reportet. Vielen Dank!", color=0x0094ff)
        await interaction.response.send_message(embed=embed, ephemeral=True)


class Utilities(discord.app_commands.Group):

    @app_commands.command(name="blacklist", description="blackliste einen user")
    @app_commands.checks.cooldown(1, 20)
    async def blacklist(self, interaction, user: discord.Member, blacklist: bool):
        with open('config.json') as file:
            config = json.load(file)
        with open("users.json") as file:
            ujson = json.load(file)
        if interaction.user.guild_permissions.administrator:
            userid = user.id

            id = config["OWNER_ID"]
            if interaction.user.id not in id:
                await interaction.response.send_message("Das solltest du besser lassen :)", ephemeral=True)
                return
            ujson[str(userid)] = {"blacklist": blacklist}
            with open("users.json", 'w') as json_file:
                json.dump(ujson, json_file, indent=4)

            if blacklist == True:
                await interaction.response.send_message(f"Der User {user.display_name} ist nun auf der Blacklist!", ephemeral=True)
            if blacklist == False:
                await interaction.response.send_message(f"Der User {user.display_name} ist nun nicht mehr auf der Blacklist!", ephemeral=True)
        else:
            await interaction.response.send_message(content="Dir fehlen die rechte dazu.",  ephemeral=True)

    @app_commands.command(name="bugreport", description="reporte einen Bug")
    @app_commands.checks.cooldown(1, 20)
    async def bugreport(self, ctx):
        with open("users.json") as file:
            ujson = json.load(file)
        if ujson[str(ctx.user.id)] != {"blacklist": True}:
            await ctx.response.send_modal(bugReportModal())
        else:
            await ctx.response.send_message("Du bist auf der Blacklist.", ephemeral=True)

    @app_commands.command(name="embed-builder", description="Erstelle ein Embed")
    async def eb(self, interaction, channel: discord.TextChannel, timestamp: bool = False):
        if interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_modal(EmbedBuilder(channel=channel, timestamp=timestamp))
        else:
            await interaction.response.send_message(content="Du hast keine Berechtigung dafür.", ephemeral=True)

    @app_commands.command(name="translate", description="Translates a Sentence")
    async def translate(self, interacion: discord.Interaction, lang: app_commands.Range[str, 2, 20], sentence: str):
        if not lang.lower() in googletrans.LANGCODES.values():
            if not lang.lower() in googletrans.LANGCODES.keys():
                await interacion.response.send_message(content="Translation Failed!\nThe target language must be a real Language.", ephemeral=True)
                return
            else:
                pass
        t = Translator()
        a = t.translate(sentence, dest=lang)
        detected_lang = t.detect(sentence)
        lang_str = str(detected_lang.lang.capitalize())
        embed = discord.Embed(title="Translator",
                              timestamp=datetime.datetime.now(), color=0x7A50BE, description=f"Detected: {lang_str.lower()}")
        embed.add_field(name="Translated Text:", value=a.text, inline=False)
        embed.add_field(name="Original Text:", value=sentence, inline=False)
        embed.set_footer(text="Translated via Google")
        await interacion.response.send_message(embed=embed)


class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        utilitiescmds = Utilities(
            name="utility", description="nützliche befehle")
        self.bot.tree.add_command(utilitiescmds)
        print("UtilityCommands Geladen!")


async def setup(bot):
    await bot.add_cog(UtilitiesCog(bot))
