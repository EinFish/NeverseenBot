from email import message_from_string

import discord
import datetime
import json
from discord import app_commands
from discord.ext import commands
from typing import Union, Any

import utils


class bearbeitenView(discord.ui.View):
	def __init__(self, reactionList):
		super().__init__(timeout=None)
		self.add_item()
		self.add_item()
		self.add_item()

class bearbeitenButtonFinish(discord.ui.Button):
	def __init__(self, text, reactonList):
		super().__init__(label=text, style=discord.ButtonStyle.grey)

	async def callback(self, interaction: discord.Interaction) -> Any:

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen

		return await interaction.response.send_message("Link im Browser geöffnet", ephemeral=True)


class bearbeitenButtonDelete(discord.ui.Button):
	def __init__(self, text, reactonList):
		super().__init__(label=text, style=discord.ButtonStyle.danger)

	async def callback(self, interaction: discord.Interaction) -> Any:

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen

		return await interaction.response.send_message("Link im Browser geöffnet", ephemeral=True)


class bearbeitenButtonAdd(discord.ui.Button):
	def __init__(self, text, reactonList):
		super().__init__(label=text, style=discord.ButtonStyle.success)

	async def callback(self, interaction: discord.Interaction) -> Any:

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen

		return await interaction.response.send_message("Link im Browser geöffnet", ephemeral=True)



class linkRoleView(discord.ui.View):
	def __init__(self, roles, emoji, name, reactionList, channel, message_obj):
		super().__init__(timeout=None)
		self.add_item(linkRoleSelect(roles, emoji, name, reactionList, channel, message_obj))


class checkView(discord.ui.View):
	def __init__(self, reactionList, channel):
		super().__init__(timeout=None)
		self.add_item(checkButtonsAccept("Korrekt", reactionList))
		self.add_item(checkButtonsDeny("Ändern", reactionList, channel))



class checkButtonsAccept(discord.ui.Button):
	def __init__(self, text, reactonList: list):
		self.reactionList = reactonList
		super().__init__(label=text, style=discord.ButtonStyle.success)

	async def callback(self, interaction: discord.Interaction) -> Any:

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen




		sjson = utils.serverjson()
		try:
			sjson[interaction.guild_id]["reactionroles"] = self.reactionList
		except KeyError:
			sjson[interaction.guild_id] = {
				"reactionroles": self.reactionList
			}
		utils.savejson(sjson, "serverconfig")

		final_reaactrolesStr = ""
		# i = {"emojiID": {"Name": 12335345}} "mond: asd (role.mention)" appendList
		# i = {"messageID": {"emojiID": {"Name": 12335345M}}} "mond: asd (role.mention)" reactionList
		for i in self.reactionList:
			print(i, type(i))
			print(i.keys())
			print(i.values())
			emoji: discord.Emoji = await interaction.guild.fetch_emoji(list(i)[0])

			name_und_id = list(i.values())[0]
			name, role_id = next(iter(name_und_id.items()))

			role = interaction.guild.get_role(role_id)

			final_reaactrolesStr = final_reaactrolesStr + f"<:{emoji.name}:{emoji.id}>: {name}, ({role.mention})\n"
			print(final_reaactrolesStr)

		embed = discord.Embed(title="ReactionRoles System bearbeiten", description=f"Momentaner Stand:\n\n {final_reaactrolesStr}")


		return await interaction.response.send_message("Link im Browser geöffnet", ephemeral=True)


class checkButtonsDeny(discord.ui.Button):
	def __init__(self, text, reactionList, channel):
		self.reactionList = reactionList
		self.channel = channel
		super().__init__(label=text, style=discord.ButtonStyle.danger)

	async def callback(self, interaction: discord.Interaction) -> Any:

		# BearbeitungsModal neu öffnen

		return await interaction.response.send_modal(reactionCreateModal(self.channel, self.reactionList))


class linkRoleSelect(discord.ui.Select):
	def __init__(self, options, emoji, name, reactionList, channel, message_obj: discord.Message = None):
		self.emoji = emoji
		self.name = name
		self.reactionList = reactionList
		self.appendList = []
		self.channel = channel
		self.message_obj = message_obj
		#self.options = options
		super().__init__(placeholder="Auswählen einer Rolle..",
						 max_values=1, min_values=1, options=options)


	async def callback(self, interaction: discord.Interaction) -> Any:

		embed = discord.Embed(title="Bestätigen und Hinzufügen", description="Sind Diese Informationen Korrekt?", color=0x0094ff, timestamp=datetime.datetime.now())

		role = interaction.guild.get_role(int(self.values[0]))
		print(interaction.guild.emojis)
		emojistr = "😃"
		for emoji in interaction.guild.emojis:
			print(self.emoji)
			self.emoji = str(self.emoji).replace(":", "")
			print(emoji.name)
			if emoji.name == self.emoji:
				print("eeezz")
				emojistr = f"<:{emoji.name}:{emoji.id}>"


		embed.add_field(name="Emoji und Name:", value=f"{emojistr}: {self.name}", inline=False)
		embed.add_field(name="Damit verlinkte Rolle:", value=role.mention, inline=False)

		if self.message_obj == None:
			reactionRolesEmbed = discord.Embed(title="Reaction Roles", description="Reagiere mit dem jeweiligen Emoji, um die Rolle zu bekommen.\n", color=0x0094ff)

			self.message_obj = await self.channel.send(embed=reactionRolesEmbed)

		# self.reactionList.append({self.message_obj.id: {str(emoji.id): {str(self.name): role.id}}})

		self.reactionList[self.message_obj.id] = {}

		await interaction.response.edit_message(embed=embed, view=checkView(self.reactionList, self.channel))

class reactionCreateModal(discord.ui.Modal):
	def __init__(self, channel, reactionList, message_obj) -> None:
		self.channel = channel
		self.reactionList = reactionList
		self.message_obj = message_from_string()
		super().__init__(title="ReactionRole System erstellen oder bearbeiten")

	emoji = discord.ui.TextInput(label="Reaktion Emoji - Rolle hinzufügen", placeholder="Emoji eingeben | Bsp.: :youtube:", style=discord.TextStyle.short, max_length=20, required=True)
	name = discord.ui.TextInput(label="Reaktion Name - Rolle hinzufügen", placeholder="Name eingeben | Bsp.: YouTube Benachrichtigungen", style=discord.TextStyle.long, max_length=100, required=True)

	async def on_submit(self, interaction: discord.Interaction) -> None:

		emojistr = "😃"
		for emoji in interaction.guild.emojis:
			print(self.emoji)
			self.emoji = str(self.emoji).replace(":", "")
			print(emoji.name)
			if emoji.name == self.emoji:
				print("eeezz")
				emojistr = f"<:{emoji.name}:{emoji.id}>"

		embed = discord.Embed(title="Rolle verlinken", description=f"Wähle eine Rolle aus für das die erste Rolle:\n{emojistr}: {self.name}", color=0x0094ff, timestamp=datetime.datetime.now())

		options = []
		for role in interaction.guild.roles:
			#options.append(role)

			options.append(
				discord.SelectOption(label=role.name, value=role.id)
			)

		print(options)
		try:
			await interaction.response.edit_message(embed=embed, view=linkRoleView(options, self.emoji, self.name, self.reactionList, self.channel, self.message_obj))
		except discord.NotFound:
			#print(e)
			await interaction.response.send_message(embed=embed, view=linkRoleView(options, self.emoji, self.name, self.reactionList, self.channel, self.message_obj))



# Commands

class reactionCommands(discord.app_commands.Group):


#	ReactionRoles System planung
#
#	erstellen command, der nachricht mit Embed erstellt: Kanal; Schickt embed, wo man das erste hinzufügt emoji und name, dann kommt embed mit rollenauswahl und bestätigung -> dann überprüfungsembed, wo man sendet oder neue rolle hinzufügt oder entfernt
#	bearbeiten command, der ReactionRoles anhand der MessageID bearbeitet, wo man hinzufügen und entfernen kann
#	delete Command, der die ReactionRoles entfernt
#

	@app_commands.command(name="erstellen", description="aaaaaaaaaaaaaaaaaaaa")
	async def create(self, interaction: discord.Interaction, channel: Union[discord.TextChannel, discord.Thread, discord.ForumChannel]):
		if not interaction.user.guild_permissions.manage_roles:
			return await interaction.response.send_message("Du hast keine Berechtigung dazu", ephemeral=True)

		reactionList: dict = {}

		await interaction.response.send_modal(reactionCreateModal(channel, reactionList, None))

	@app_commands.command(name="bearbeiten", description="aaaaaaaaaaaaaa")
	async def edit(self, interaction: discord.Interaction, message_id: int):
		if not interaction.user.guild_permissions.manage_roles:
			return await interaction.response.send_message("Du hast keine Berechtigung dazu", ephemeral=True)

	@app_commands.command(name="entfernen", description="Lösche ein ReactionRole System")
	async def delete(self, interaction: discord.Interaction, message_id: int):
		if not interaction.user.guild_permissions.manage_roles:
			return await interaction.response.send_message("Du hast keine Berechtigung dazu", ephemeral=True)


class reactionCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_ready(self):
		setupcmds = reactionCommands(
			name="reaction-roles", description="Befehle für das ReactionRoles System")
		self.bot.tree.add_command(setupcmds)
		print("ReactionCommands Geladen!")


async def setup(bot):
	await bot.add_cog(reactionCog(bot))