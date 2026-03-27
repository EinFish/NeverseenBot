from email import message_from_string

import discord
import datetime
import json
from discord import app_commands
from discord.ext import commands
from typing import Union, Any

import utils


async def get_rrList(interaction, message_id, reactionList = None):

	if not reactionList:
		sjson = utils.serverjson()
		try:
			reactionList = sjson[str(interaction.guild_id)]["reactionroles"][message_id]
		except KeyError:
			return await interaction.response.send_message("ReactionRole System nicht gefunden", ephemeral=True)

	final_reaactrolesStr = ""
	# i = {"emojiID": {"Name": 12335345}} "mond: asd (role.mention)" reactionList
	# i = {"messageID": {"emojiID": {"Name": 12335345}}} "mond: asd (role.mention)" is nicht
	count = 1
	for i in reactionList:
		emoji: discord.Emoji = await interaction.guild.fetch_emoji(list(i)[0])

		name_und_id = list(i.values())[0]
		name, role_id = next(iter(name_und_id.items()))

		role = interaction.guild.get_role(role_id)

		final_reaactrolesStr = final_reaactrolesStr + f"### ({count}) <:{emoji.name}:{emoji.id}> · {name} ({role.mention})\n"
		count+=1

	embed = discord.Embed(title="ReactionRoles System bearbeiten",
						  description=f"Momentaner Stand:\n\n{final_reaactrolesStr}", color=0x0094ff)

	# message = await interaction.channel.fetch_message(int(message_id))
	# channel = message.channel

	return embed



class deleteModal(discord.ui.Modal):
	def __init__(self, channel, message_id):
		self.channel = channel
		self.message_id = message_id
		super().__init__(title="ReactionRole eintrag entfernen")

	id_field = discord.ui.TextInput(label="ID des Eintrags", style=discord.TextStyle.short, max_length=2, placeholder="Die ID, die vor dem Eintrag steht", required=True)

	async def on_submit(self, interaction: discord.Interaction) -> None:
		sjson = utils.serverjson()
		try:
			self.id_field = int(str(self.id_field)) -1
		except Exception as e:
			print(e)
			return await interaction.response.send_message("Ungültiger Wert", ephemeral=True)

		reactionList = sjson[str(interaction.guild_id)]["reactionroles"][self.message_id]
		del reactionList[self.id_field]
		utils.savejson(sjson, "serverconfig")

		embed = await get_rrList(interaction, self.message_id)

		return await interaction.response.edit_message(embed=embed, view=bearbeitenView(self.channel, reactionList, self.message_id))


class bearbeitenView(discord.ui.View):
	def __init__(self, channel, reactionList, message_id):
		self.channel = channel
		self.reactionList = reactionList
		self.message_id = message_id
		super().__init__(timeout=None)
		self.add_item(bearbeitenButtonAdd("Weitere Hinzufügen", self.channel, self.reactionList, self.message_id))
		self.add_item(bearbeitenButtonDelete("Eine entfernen", self.channel, self.reactionList, self.message_id))
		self.add_item(bearbeitenButtonFinish("Fertig", self.channel, self.reactionList, self.message_id))



class bearbeitenButtonFinish(discord.ui.Button):
	def __init__(self, text, channel, reactionList, message_id):
		self.channel = channel
		self.reactionList = reactionList
		self.message_id = message_id
		super().__init__(label=text, style=discord.ButtonStyle.grey, emoji="✔️")

	async def callback(self, interaction: discord.Interaction) -> Any:
		await interaction.response.defer()

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen
		# ReactionRole Message bearbeiten oder neu erstellen
		final_embed_description: str = ">>> "
		emojiList: list = []
		for item in self.reactionList:
			emoji: discord.Emoji = await interaction.guild.fetch_emoji(list(item)[0])
			emojiList.append(emoji)
			name_und_id = list(item.values())[0]
			name, role_id = next(iter(name_und_id.items()))

			role = interaction.guild.get_role(role_id)

			final_embed_description += f"### <:{emoji.name}:{emoji.id}> · {name}\n"


		embed = discord.Embed(title="Reagiert auf die Nachricht um folgende Rollen zu bekommen!", description=final_embed_description, color=0x0094ff)

		if not self.message_id:
			message = await self.channel.send(embed=embed)
		else:
			message: discord.Message = await self.channel.fetch_message(self.message_id)
			await message.edit(embed=embed)

		for item in emojiList:
			await message.add_reaction(item)

		# speichern
		sjson = utils.serverjson()
		try:
			sjson[str(interaction.guild_id)]["reactionroles"][str(message.id)] = self.reactionList
		except KeyError:
			sjson[str(interaction.guild_id)]["reactionroles"] = {str(message.id): self.reactionList}
		utils.savejson(sjson, "serverconfig")


		return await interaction.followup.send("Gespeichert!")


class bearbeitenButtonDelete(discord.ui.Button):
	def __init__(self, text, channel, reactionList, message_id):
		self.channel = channel
		self.message_id = message_id
		super().__init__(label=text, style=discord.ButtonStyle.danger, emoji="➖")

	async def callback(self, interaction: discord.Interaction) -> Any:

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen
		# modal öffnen, wo man ID eingibt

		return await interaction.response.send_modal(deleteModal(self.channel, self.message_id))


class bearbeitenButtonAdd(discord.ui.Button):
	def __init__(self, text, channel, reactionList, message_id):
		self.channel = channel
		self.reactionList = reactionList
		self.message_id = message_id
		super().__init__(label=text, style=discord.ButtonStyle.success, emoji="➕")

	async def callback(self, interaction: discord.Interaction) -> Any:

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen

		return await interaction.response.send_modal(reactionCreateModal(self.channel, self.reactionList, self.message_id))



class linkRoleView(discord.ui.View):
	def __init__(self, roles, emoji, name, reactionList, channel, message_id, options2):
		super().__init__(timeout=None)
		self.add_item(linkRoleSelect(roles, emoji, name, reactionList, channel, message_id))
		if options2:
			self.add_item(linkRoleSelect2(options2, emoji, name, reactionList, channel, message_id))



class checkView(discord.ui.View):
	def __init__(self, reactionList, channel, message_id):
		super().__init__(timeout=None)
		self.add_item(checkButtonsAccept("Korrekt", reactionList, message_id, channel))
		self.add_item(checkButtonsDeny("Ändern", reactionList, channel))



class checkButtonsAccept(discord.ui.Button):
	def __init__(self, text, reactonList: list, message_id, channel):
		self.reactionList = reactonList
		self.message_id = message_id
		self.channel = channel
		super().__init__(label=text, style=discord.ButtonStyle.success)

	async def callback(self, interaction: discord.Interaction) -> Any:

		# drei buttons, Änderungen speichern, Rolle hinzufügen, Rolle entfernen

		embed = await get_rrList(interaction, self.message_id, self.reactionList)


		return await interaction.response.edit_message(embed=embed, view= bearbeitenView(self.channel, self.reactionList, self.message_id))


class checkButtonsDeny(discord.ui.Button):
	def __init__(self, text, reactionList, channel):
		self.reactionList = reactionList
		self.channel = channel
		super().__init__(label=text, style=discord.ButtonStyle.danger)

	async def callback(self, interaction: discord.Interaction) -> Any:

		# BearbeitungsModal neu öffnen

		return await interaction.response.send_modal(reactionCreateModal(self.channel, self.reactionList))


class linkRoleSelect(discord.ui.Select):
	def __init__(self, options, emoji, name, reactionList, channel, message_id = None):
		self.emoji = emoji
		self.name = name
		self.reactionList = reactionList
		self.appendList = []
		self.channel = channel
		self.message_id = message_id
		#self.options = options
		super().__init__(placeholder="Auswählen einer Rolle..",
						 max_values=1, min_values=1, options=options)


	async def callback(self, interaction: discord.Interaction) -> Any:

		embed = discord.Embed(title="Bestätigen und Hinzufügen", description="Sind Diese Informationen Korrekt?", color=0x0094ff, timestamp=datetime.datetime.now())

		role = interaction.guild.get_role(int(self.values[0]))
		emojistr = "😃"
		for emoji in interaction.guild.emojis:
			self.emoji = str(self.emoji).replace(":", "")
			if emoji.name == self.emoji:
				emojistr = f"<:{emoji.name}:{emoji.id}>"
				break

		if emojistr == "😃": emojistr = str(self.emoji)

		if "@role" in str(self.name):
			self.name = str(self.name).replace("@role", role.mention)

		embed.add_field(name="Emoji und Name:", value=f"{emojistr}: {self.name}", inline=False)
		embed.add_field(name="Damit verlinkte Rolle:", value=role.mention, inline=False)

		# if self.message_obj == None:
		# 	reactionRolesEmbed = discord.Embed(title="Reaction Roles", description="Reagiere mit dem jeweiligen Emoji, um die Rolle zu bekommen.\n", color=0x0094ff)
		#
		# 	self.message_obj = await self.channel.send(embed=reactionRolesEmbed)

		self.reactionList.append({str(emoji.id): {str(self.name): role.id}})

		# self.reactionList[self.message_obj.id] = {}

		await interaction.response.edit_message(embed=embed, view=checkView(self.reactionList, self.channel, self.message_id))



class linkRoleSelect2(discord.ui.Select):
	def __init__(self, options, emoji, name, reactionList, channel, message_id = None):
		self.emoji = emoji
		self.name = name
		self.reactionList = reactionList
		self.appendList = []
		self.channel = channel
		self.message_id = message_id
		#self.options = options
		super().__init__(placeholder="Auswählen einer Rolle..",
						 max_values=1, min_values=1, options=options)


	async def callback(self, interaction: discord.Interaction) -> Any:

		embed = discord.Embed(title="Bestätigen und Hinzufügen", description="Sind Diese Informationen Korrekt?", color=0x0094ff, timestamp=datetime.datetime.now())

		role = interaction.guild.get_role(int(self.values[0]))
		emojistr = "😃"
		for emoji in interaction.guild.emojis:
			self.emoji = str(self.emoji).replace(":", "")
			if emoji.name == self.emoji:
				emojistr = f"<:{emoji.name}:{emoji.id}>"
				break

		if emojistr == "😃": emojistr = str(self.emoji)

		if "@role" in str(self.name):
			self.name = str(self.name).replace("@role", role.mention)

		embed.add_field(name="Emoji und Name:", value=f"{emojistr}: {self.name}", inline=False)
		embed.add_field(name="Damit verlinkte Rolle:", value=role.mention, inline=False)

		# if self.message_obj == None:
		# 	reactionRolesEmbed = discord.Embed(title="Reaction Roles", description="Reagiere mit dem jeweiligen Emoji, um die Rolle zu bekommen.\n", color=0x0094ff)
		#
		# 	self.message_obj = await self.channel.send(embed=reactionRolesEmbed)

		self.reactionList.append({str(emoji.id): {str(self.name): role.id}})

		# self.reactionList[self.message_obj.id] = {}

		await interaction.response.edit_message(embed=embed, view=checkView(self.reactionList, self.channel, self.message_id))





class reactionCreateModal(discord.ui.Modal):
	def __init__(self, channel, reactionList, message_id) -> None:
		self.channel = channel
		self.reactionList = reactionList
		self.message_id = message_id
		super().__init__(title="ReactionRole System erstellen oder bearbeiten")

	emoji = discord.ui.TextInput(label="Reaktion Emoji - Rolle hinzufügen", placeholder="Emoji eingeben | Bsp.: :youtube:", style=discord.TextStyle.short, max_length=20, required=True)
	name = discord.ui.TextInput(label="Reaktion Name - Rolle hinzufügen", placeholder="Name eingeben | Bsp.: YouTube Benachrichtigungen | für rollenping @role eingeben", style=discord.TextStyle.long, max_length=100, required=True)

	async def on_submit(self, interaction: discord.Interaction) -> None:

		emojistr = "😃"
		for emoji in interaction.guild.emojis:
			self.emoji = str(self.emoji).replace(":", "")
			if emoji.name == self.emoji:
				emojistr = f"<:{emoji.name}:{emoji.id}>"
		if emojistr == "😃": emojistr = str(self.emoji)


		embed = discord.Embed(title="Rolle verlinken", description=f"Wähle eine Rolle aus für das die erste Rolle:\n{emojistr}: {self.name}", color=0x0094ff, timestamp=datetime.datetime.now())

		options = []
		options2 = []
		for role in interaction.guild.roles:
			#options.append(role)
			if len(options) >= 25:
				options2.append(
				discord.SelectOption(label=role.name, value=role.id))

			else:
				options.append(
					discord.SelectOption(label=role.name, value=role.id)
				)




		try:
			await interaction.response.edit_message(embed=embed, view=linkRoleView(options, self.emoji, self.name, self.reactionList, self.channel, self.message_id, options2))
		except discord.NotFound:
			await interaction.response.send_message(embed=embed, view=linkRoleView(options, self.emoji, self.name, self.reactionList, self.channel, self.message_id, options2))



# Commands

class reactionCommands(discord.app_commands.Group):


#	ReactionRoles System planung
#
#	erstellen command, der nachricht mit Embed erstellt: Kanal; Schikt embed, wo man das erste hinzufügt emoji und name, dann kommt embed mit rollenauswahl und bestätigung -> dann überprüfungsembed, wo man sendet oder neue rolle hinzufügt oder entfernt
#	bearbeiten command, der ReactionRoles anhand der MessageID bearbeitet, wo man hinzufügen und entfernen kann
#	delete Command, der die ReactionRoles entfernt
#

	@app_commands.command(name="erstellen", description="Erstellt ein neues ReactionRoles System")
	async def create(self, interaction: discord.Interaction, channel: Union[discord.TextChannel, discord.Thread, discord.ForumChannel]):
		if not interaction.user.guild_permissions.manage_roles:
			return await interaction.response.send_message("Du hast keine Berechtigung dazu", ephemeral=True)

		reactionList: list = []

		await interaction.response.send_modal(reactionCreateModal(channel, reactionList, None))

	@app_commands.command(name="bearbeiten", description="Bearbeitet ein vorhandenes ReactionRole System")
	async def edit(self, interaction: discord.Interaction, message_id: str, channel: Union[discord.TextChannel, discord.Thread, discord.ForumChannel]):
		if not interaction.user.guild_permissions.manage_roles:
			return await interaction.response.send_message("Du hast keine Berechtigung dazu", ephemeral=True)

		sjson = utils.serverjson()
		try:
			reactionList = sjson[str(interaction.guild_id)]["reactionroles"][message_id]
		except KeyError:
			return await interaction.response.send_message("ReactionRole System nicht gefunden", ephemeral=True)


		embed = await get_rrList(interaction, message_id)

		return await interaction.response.send_message(embed=embed, view=bearbeitenView(channel, reactionList, message_id))


	@app_commands.command(name="entfernen", description="Lösche ein ReactionRole System")
	async def delete(self, interaction: discord.Interaction, message_id: str, channel: Union[discord.TextChannel, discord.Thread, discord.ForumChannel]):
		if not interaction.user.guild_permissions.manage_roles:
			return await interaction.response.send_message("Du hast keine Berechtigung dazu", ephemeral=True)

		sjson = utils.serverjson()
		del sjson[str(interaction.guild_id)]["reactionroles"][str(message_id)]
		message: discord.Message = await channel.fetch_message(message_id)
		await message.delete()
		utils.savejson(sjson, "serverconfig")

		return await interaction.response.send_message("ReactionRoles System gelöscht.", ephemeral=True)


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