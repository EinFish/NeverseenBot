import discord
from discord.ext import commands
import utils


class ExeptionHandler(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot

        bot.tree.error(coro=self.__dispatch_to_app_command_handler)

    async def __dispatch_to_app_command_handler(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        self.bot.dispatch("app_command_error", interaction, error)

    @commands.Cog.listener("on_app_command_error")
    async def get_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        try:
            await interaction.response.defer()
        except:
            pass
        if isinstance(error, discord.app_commands.CommandOnCooldown):
            await interaction.followup.send(content=f"Dieser Befehl is auf Cooldown! Du kannst ihn nutzen nach: \n{int(error.retry_after)} Sekunden")
        else:
            utils.errordcmessage(interaction=interaction, error=error)


async def setup(bot: commands.Bot):
    await bot.add_cog(ExeptionHandler(bot))
