import asyncio
from typing import Any
import discord
from discord.ext import commands
from discord import app_commands
import datetime

with open("serverconfig.json") as file:
    sjson = json.load(file)
with open("reactions.json") as file:
    rjson = json.load(file)
with open("config.json", "r") as file:
    config = json.load(file)

class TicketButtons(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle, mode):
        super().__init__(label=text, style=discordbuttonstyle)
        self.mode = mode

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

        if self.mode == 0:
            await interaction.channel.edit(locked=True)
            #await interaction.channel.remove_user()
            print(interaction.channel.last_message.content)
            content = interaction.channel.last_message.content.split(',')
            content2 = content[0]
            content3 = content2[2:20]
            content4 = int(content3)
            member = interaction.channel.fetch_member(content4)
            await interaction.channel.remove_user(member)



        if self.mode == 1:
           pass 

class TicketView2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButtons("Ticket schließen", discord.ButtonStyle.danger, 0))
        self.add_item(TicketButtons("Ticket Beanspruchen", discord.ButtonStyle.success, 1))

class EmbedBuilder(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title="Embed Builder")
    titel = discord.ui.TextInput(label="Titel:", placeholder="Setzte einen Titel", style=discord.TextStyle.short)
  #  farbe = discord.ui.TextInput(label="Farbe:", placeholder="Bitte einen Hex farbcode ohne #", style=discord.TextStyle.short)
    description = discord.ui.TextInput(label="Beschreibung", placeholder="Füge eine Beschreibung hinzu", style=discord.TextStyle.long, max_length=1500, required=False)    
    

    async def on_submit(self, interaction) -> None:
        embed = discord.Embed(title=EmbedBuilder.titel, color=0x0094ff, description=EmbedBuilder.description)
        await interaction.response.defer()
        await interaction.followup.send(embed=embed)

class TicketModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Problembeschreibung:")
    problem = discord.ui.TextInput(label="Was ist dein Anliegen?", placeholder="Problem", required=True, style=discord.TextStyle.short, max_length=100, min_length=10)
    async def on_submit(self, interaction) -> None:
        mod = sjson["mod"]
        Channel = interaction.channel
        self.person = interaction.user.mention
        id = interaction.user.id
        self.Thread = await Channel.create_thread(name=interaction.user.display_name)
        await interaction.response.send_message(content="Dein Ticket findest du hier: " + self.Thread.jump_url , ephemeral=True)
        embed = discord.Embed(color=0x0094ff, timestamp=datetime.datetime.now(), title=self.problem, description=interaction.user.mention + " bitte beschreibe dein Problem näher. Es wird sich bald ein Team Mitglied um dein Problem kümmern.")
        await self.Thread.send(content=self.person + "," + mod, embed=embed, view=TicketView2())





        
class TicketButton(discord.ui.Button):
    def __init__(self, text, discordbuttonstyle):
        super().__init__(label=text, style=discordbuttonstyle)

    async def callback(self, interaction: discord.Interaction) -> Any:
        await interaction.response.send_modal(TicketModal())

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketButton("Ticket erstellen", discord.ButtonStyle.success))


class FunCommands(discord.app_commands.Group):
    @app_commands.command(name="twitch", description="Bekomme den Twitch Link!")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def twich(self, ctx):
        await ctx.response.defer()
        embed = discord.Embed(title="Twitch Link", description=sjson["twitch_link"], color=0x0094ff, timestamp=datetime.datetime.now())
        await ctx.followup.send(embed=embed)

    @app_commands.command(name="play-music", description="Spielt einen ausgewählten Song.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def playsong(self, interaction):
        await interaction.response.send_message("Nicht eingebaut!", ephemeral=True)


class ModCommands(discord.app_commands.Group):
    @app_commands.command(name="delete-messages", description="Lösche Nachrichten von einem Bestimmten User.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def delete(self, ctx, user: discord.Member):
        await ctx.response.defer()
        print(user)


    @app_commands.command(name="ticketchannel", description="Lege den Kanal für die Tickets fest.")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def ticket_channel(self, interaction, channel: discord.TextChannel, titel: str, text: str = ""):
        if text == "":
            text = "Klicke auf den unteren Knopf um ein " + titel + " ticket zu erstellen."
        await interaction.response.defer()
        print(channel.id)
        embed = discord.Embed(title=titel, description=text, color=0x0094ff)
        await interaction.followup.send(content="erstellt", ephemeral=True)
        await channel.send(embed=embed, view=TicketView())


    @app_commands.command(name="kick", description="Kicke einen Member")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, interaction, member: discord.Member, reason: str):
        if interaction.user.guild_permissions.administrator:
            channel = interaction.guild.get_channel(int(sjson["log_channel"]))
            await member.kick(reason=reason)
            await interaction.response.send_message(content=f"Du hast {member.mention} erfolgreich gekickt", ephemeral=True)

            embed = discord.Embed(title="User gekickt", description="Ein User wurde von " + interaction.user.mention + " gekickt.",color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Gekickt:", value=member.mention, inline=True)
            embed.add_field(name="Von:", value=interaction.user.mention, inline=True)
            await channel.send(embed=embed)

        else:
            await interaction.response.send_message(content="<a:catnewspaper:1096143115678662656> <a:catnewspaper:1096143115678662656> <a:catnewspaper:1096143115678662656>", ephemeral=True)


    @app_commands.command(name="ban", description="Banne einen Member")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def on_member_ban(self, interaction, user: discord.Member, reason: str):
     channel = interaction.guild.get_channel(int(sjson["log_channel"]))
     if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(content=f"Du hast {user.mention} erfolgreich gebannt", ephemeral=True)
        await user.ban(reason=reason)
   
        embed = discord.Embed(title="User gebannt", description="Ein User wurde von " + interaction.user.mention + " gebannt.",color=0x0094ff, timestamp=datetime.datetime.now())
        embed.add_field(name="Gebannt:", value=user.mention, inline=True)
        embed.add_field(name="Von:", value=interaction.user.mention, inline=True)
        await channel.send(embed=embed)
     else:
         await interaction.response.send_message(content="<a:catnewspaper:1096143115678662656> <a:catnewspaper:1096143115678662656> <a:catnewspaper:1096143115678662656>", ephemeral=True)
        

    @app_commands.command(name="unban", description="Entbanne einen Nutzer")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unban(self, interaction, user: discord.User, reason: str):
        if interaction.user.guild_permissions.administrator:
            channel = interaction.guild.get_channel(int(sjson["log_channel"]))
            await interaction.guild.unban(user, reason=reason)
            await interaction.response.send_message(content=f"Du hast {user.mention} erfolgreich entbannt", ephemeral=True)

            embed = discord.Embed(title="User entbannt", description="Ein User wurde von " + interaction.user.mention + " entbannt.",color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Entbannt:", value=user.mention, inline=True)
            embed.add_field(name="Von:", value=interaction.user.mention, inline=True)
            await channel.send(embed=embed)
        else:
            await interaction.response.send_message(content=f"{rjson["catnewspaper"]} {rjson["catnewspaper"]} {rjson["catnewspaper"]}", ephemeral=True)


    @app_commands.command(name="mute", description="Schicke einen Member in den Timeout")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def on_member_timeout(self, interaction, member: discord.Member, reason: str, seconds: int = 1, minutes: int = 0, hours: int = 0, days: int = 0, ):
        channel = interaction.guild.get_channel(int(sjson["log_channel"]))
        if interaction.user.guild_permissions.administrator:
            duration = datetime.timedelta(seconds=seconds, minutes=minutes, hours= hours, days=days)
            await interaction.response.send_message(content="Der User " + member.mention + f" wurde in ein Timeout geschickt für: {duration}", ephemeral=True)
            await member.timeout(duration, reason=reason)

            embed = discord.Embed(title="User im Timeout", description=f"Ein User wurde von {interaction.user.mention} ins Timeout versetzt.", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Im Timeout:", value=member.mention, inline=True)
            embed.add_field(name="Von:", value=interaction.user.mention, inline=True)
            embed.add_field(name="Für:", value=duration, inline=True)
            embed.add_field(name="Grund:", value=reason, inline=True)
            await channel.send(embed=embed)
        else:
           await interaction.response.send_message(content=f"{rjson["catnewspaper"]} {rjson["catnewspaper"]} {rjson["catnewspaper"]}", ephemeral=True)
    @app_commands.command(name="unmute", description="Hebe das Timeout von einem User auf")
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def unmute(self, interaction, member: discord.Member, reason: str):
        channel = interaction.guild.get_channel(int(sjson["log_channel"]))
        if interaction.user.guild_permissions.administrator:
            duration = None
            await interaction.response.send_message(content="Du hast das Timeout  von " + member.mention + " aufgehoben", ephemeral=True)
            await member.timeout(duration, reason=reason)

            embed = discord.Embed(title="User aus dem Timeout", description=interaction.user.mention + " hat ein Timeout von " + member.mention + " aufgehoben",color=0x0094ff, timestamp=datetime.datetime.now())
            embed.add_field(name="Aus dem Timeout:", value=member.mention, inline=True)
            embed.add_field(name="Von:", value=interaction.user.mention, inline=True)
            embed.add_field(name="Grund:", value=reason, inline=True)
            await channel.send(embed=embed)
        else:
           await interaction.response.send_message(content=f"{rjson["catnewspaper"]} {rjson["catnewspaper"]} {rjson["catnewspaper"]}", ephemeral=True)


    @app_commands.command(name="embed-builder", description="Baue ein Embed in einem Formular!")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def embedbuilder(self, interaction):
        await interaction.response.send_modal(EmbedBuilder())

class HelpView(discord.ui.View):
    def __init__(self, client, timeout=3600):
        super().__init__(timeout=timeout)
        options = HelpSelect.generate_options(client)
        self.add_item(HelpSelect(client, options))

class HelpSelect(discord.ui.Select):

    options = []

    def __init__(self, client, options):
        self.client = client
        super().__init__(placeholder="Wofür möchtest du Hilfe erhalten?",
                         max_values=1, min_values=1, options=options)

    async def callback(self, interaction):
        newtext = ""
        for group in interaction.client.tree.walk_commands():
            if group.name == self.values[0]:
                for command in group.commands:
                    newtext += f"\n`{command.name}"

                    for param in command.parameters:
                        if param.required:
                            newtext += f" {param.name}"
                        else:
                            newtext += f" ({param.name})"

                    newtext += f"`: {command.description}"
        embed = discord.Embed(
            title=self.values[0], description=newtext, color=0x0094ff)
        embed.set_footer(
            text=f"{interaction.user}", icon_url=interaction.user.avatar.url)
        await interaction.response.edit_message(embed=embed)

    @classmethod
    def generate_options(self, client):
        options = []
        groups = []
        for cmd in client.tree.walk_commands():
            if cmd.parent is not None:
                if cmd.parent.qualified_name not in groups:
                    groups.append(cmd.parent.qualified_name)
                    options.append(discord.SelectOption(
                        label=cmd.parent.qualified_name,
                        description=cmd.parent.description,
                        value=cmd.parent.qualified_name
                    ))
        return options
  


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        funcmds = FunCommands(name="fun", description="zum Spaß haben")
        modcmds = ModCommands(name="mod", description="Zum Moderieren")
        self.bot.tree.add_command(funcmds)
        self.bot.tree.add_command(modcmds)
        print("Commands geladen!")

    @app_commands.command(name="help", description="bekomme hilfe")
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def help(self, ctx):
        await ctx.response.defer()
        try:
            embed = discord.Embed(
                title="Wofür möchtest du hilfe erhalten?", description=f"Suche eine der unten stehenden Kategorien aus, um Hilfe zu erhalten", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.set_footer(
                text=f"{ctx.user}", icon_url=ctx.user.avatar.url if ctx.user.avatar != None else None)
            await ctx.followup.send(embed=embed, view=HelpView(ctx.client))
        except:
            embed = discord.Embed(
                title="Fehler!", description=f"Nicht einmal ich kann dir dabei helfen :c", color=0x0094ff, timestamp=datetime.datetime.now())
            embed.set_footer(
                text=f"{ctx.user}", icon_url=ctx.user.avatar.url if ctx.user.avatar != None else None)
            await ctx.followup.send(embed=embed)


    @commands.command()
    async def sync(self, ctx) -> None:
        if ctx.author.id != config["OWNER_ID"]:
            await ctx.send("Das solltest du besser lassen :)")
            return
        print("started sync")
        fmt = await ctx.bot.tree.sync()
        await ctx.bot.tree.sync()
        await ctx.send(f"{len(fmt)} Befehle wurden gesynced.")
        print("finished sync")



async def setup(bot):
    await bot.add_cog(Commands(bot))
