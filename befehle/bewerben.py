import asyncio
import discord
from typing import Any
from discord.ext import commands
import json
from discord import app_commands

with open("reactions.json") as file:
    rjson = json.load(file)


with open("serverconfig.json") as file:
    sjson = json.load(file)


class TicketModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Bewerben")
    frage0 = discord.ui.TextInput(label="Kurze Selbstvorstellung & Deine Motivation", placeholder="Required",
                                   required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage1 = discord.ui.TextInput(label="Hast du Erfahrung im Umgang mit Twitch?", placeholder="Required",
                                   required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage2 = discord.ui.TextInput(label="Hast du gute Kommunikationsfähigkeiten?", placeholder="Required",
                                   required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage3 = discord.ui.TextInput(label="Verantfortungsbewusst und Zeitlich Flexibel?", placeholder="Required",
                                   required=True, style=discord.TextStyle.paragraph, max_length=500, min_length=10)
    frage4 = discord.ui.TextInput(label="Kannst du in einem Team arbeiten?", placeholder="Required",
                                   required=True, style=discord.TextStyle.short, max_length=500, min_length=10)

    async def on_submit(self, interaction) -> None:
        """ guildid = interaction.guild.id
        mod = sjson[str(guildid)]["modrole"]
        Channel = interaction.channel
        self.person = interaction.user.mention
        id = interaction.user.id
        self.Thread = await Channel.create_thread(name=interaction.user.display_name)
        await interaction.response.send_message(content="Dein Ticket findest du hier: " + self.Thread.jump_url, ephemeral=True)
        embed = discord.Embed(color=0x0094ff, timestamp=datetime.datetime.now(), title=self.problem, description=interaction.user.mention +
                              " bitte beschreibe dein Problem näher. Es wird sich bald ein Team Mitglied um dein Problem kümmern.")
        await self.Thread.send(content=f"{self.person}, {mod}", embed=embed, view=TicketView2()) """
        await interaction.response.send_message(content="Bewerbung eingereicht!", ephemeral=True)




class TicketButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle):
        super().__init__(label=text, style=discordbuttonstyle)

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_modal(TicketModal())





class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton("Bewerben",
                      discord.ButtonStyle.success))





class BewerbenCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bewerbung geladen!")


    @commands.command()
    async def bewerben(self, ctx):
        if ctx.author.guild_permissions.administrator:
            id = ctx.guild.id
            channelid = sjson[str(id)]['bewerben']
            channel = self.bot.get_channel(channelid)
            text = "Klicke auf den unteren Knopf um dich zu Bewerben."
            embed = discord.Embed(title="Bewerben", description=text, color=0x0094ff)
            await ctx.reply(content="erstellt", ephemeral=True)
            await channel.send(embed=embed, view=TicketView())
        else:
            await ctx.reply(rjson['catnewspaper']) 



    @commands.command()
    async def channel_bewerben(self, ctx):
        print("dfj")   
    

async def setup(bot):
    await bot.add_cog(BewerbenCog(bot))