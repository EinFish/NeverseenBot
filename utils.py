import discord


class ErrorMessage():

    async def errordcmessage(interaction, error):

        await interaction.response.send_message(content=f"Ein Error!\n\n```txt\n{error}```\nReporte bitte diesen Error mit `/utility bugreport`", ephemeral=True)
