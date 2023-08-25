import asyncio
import discord
from discord.ext import commands
from discord import app_commands, ui
from discord.interactions import Interaction
import utils


class bugReportModal(ui.Modal, title="Bugreport"):
    command = ui.TextInput(label="in welchen Befehl tritt der Bug auf?",
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
        recivers = [753863284448428102]
        for reciver in recivers:
            reciv = interaction.client.get_user(reciver)
            await reciv.send(embed=discord.Embed(title="Bugreport", description=f"Bug reportet von {interaction.user} ({interaction.user.id})\n```\nBefehl: {self.command}\n\nerwartet: {self.excepted}\n\ntatsächlich: {self.actual}\n\nreproduce: {self.reproduce}\n\nExtra: {self.extra}\n```", color=0x0094ff))
        embed = discord.Embed(
            title="Danke", description="Der Bug wurde reportet. Vielen Dank!", color=0x0094ff)
        await interaction.response.send_message(embed=embed)


class bugreportCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bugreport", description="reporte einen Bug")
    @app_commands.checks.cooldown(1, 20)
    async def bugreport(self, ctx):
        """ if api.isBugReportBlacklisted(ctx.user.id):
            embed = utils.embedFactory(
                title="tja", description="Da hat wohl jemand quatsch mit den bugreport befehl gemacht <:laugh:1096037745652138024>")
            await embed.sendEmbed(ctx, followup=False)
        else: """
        await ctx.response.send_modal(bugReportModal())


async def setup(bot):
    await bot.add_cog(bugreportCog(bot))
