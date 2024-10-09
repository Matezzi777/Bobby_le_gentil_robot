from classes import *
import discord.ui

import discord.ext

############  BOUTONS  ############
class Validated_Choice(discord.ui.Button):
    def __init__(self, *, label=" - ", style=discord.ButtonStyle.green, emoji=None) -> None:
        super().__init__(
            emoji=emoji,
            label=label,
            style=style
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(view=self.view)
class Choice(discord.ui.Button):
    def __init__(self, emoji, label_content , list_users: list, needed_confirm: int) -> None:
        super().__init__(
            emoji=emoji,
            label=f"{label_content}",
            style=discord.ButtonStyle.grey
        )
        self.label_content = label_content
        self.list_users: list = list_users
        self.needed_confirm: int = needed_confirm
        self.count: int = 0
        self.users_who_clicked: list = []

    async def callback(self, interaction: discord.Interaction) -> None:
        user = interaction.user
        if (user in self.list_users):
            if (not user in self.users_who_clicked):
                self.count += 1
                self.users_who_clicked.append(user)
            else:
                self.count -= 1
                self.users_who_clicked.remove(user)
            if (self.count < self.needed_confirm):
                if (self.count == 0):
                    self.label = f"{self.label_content}"
                else:
                    self.label = f"{self.label_content} ({self.count})"
                await interaction.response.edit_message(view=self.view)
            else:
                validated = discord.ui.View()
                validated.add_item(Validated_Choice(label=f"{self.label_content}", emoji=self.emoji))
                await interaction.response.edit_message(view=validated)
        else:
            embed = ErrorEmbed(description="You tried to vote for a mapvote, but you are not in this game.\nIf you want to join this game, hop in the Voice Channel and ask for a new mapvote.")
            await user.send(embed=embed)
            await interaction.response.edit_message(view=self.view)
class Generic_NO(discord.ui.Button):
    def __init__(self, label_content: str, list_users: list, needed_confirm: int) -> None:
        super().__init__(
            label=f"❌ {label_content}",
            style=discord.ButtonStyle.grey
        )
        self.label_content = label_content
        self.list_users: list = list_users
        self.needed_confirm: int = needed_confirm
        self.count: int = 0
        self.users_who_clicked: list = []

    async def callback(self, interaction: discord.Interaction) -> None:
        user = interaction.user
        if (user in self.list_users):
            if (not user in self.users_who_clicked):
                self.count += 1
                self.users_who_clicked.append(user)
            else:
                self.count -= 1
                self.users_who_clicked.remove(user)
            if (self.count < self.needed_confirm):
                if (self.count == 0):
                    self.label = f"❌ {self.label_content}"
                else:
                    self.label = f"❌ {self.label_content} ({self.count})"
                await interaction.response.edit_message(view=self.view)
            else:
                validated = discord.ui.View()
                validated.add_item(Validated_Choice(label=f"❌ {self.label_content}", style=discord.ButtonStyle.red))
                await interaction.response.edit_message(view=validated)
        else:
            embed = ErrorEmbed(description="You tried to vote for a mapvote, but you are not in this game.\nIf you want to join this game, hop in the Voice Channel and ask for a new mapvote.")
            await user.send(embed=embed)
            await interaction.response.edit_message(view=self.view)

############   VIEWS   ############
class VersionBBG(discord.ui.View):
    def __init__(self, users) -> None:
        super().__init__(timeout=None)
        self.nb_users: int = len(users)
        self.needed_confirm: int = (self.nb_users // 2) + 1
        self.add_item(Choice(emoji="🛠️", label_content="BBG", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Choice(emoji="🛠️", label_content="BBG Beta", list_users=users, needed_confirm=self.needed_confirm))
class Drafts(discord.ui.View):
    def __init__(self, users) -> None:
        super().__init__(timeout=None)
        self.nb_users: int = len(users)
        self.needed_confirm: int = (self.nb_users // 2) + 1
        self.add_item(Choice(emoji="✅", label_content="YES", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Generic_NO("NO", users, self.needed_confirm))
class Religious(discord.ui.View):
    def __init__(self, users) -> None:
        super().__init__(timeout=None)
        self.nb_users: int = len(users)
        self.needed_confirm: int = (self.nb_users // 2) + 1
        self.add_item(Choice(emoji="✅", label_content="ENABLED", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Generic_NO("DISABLED", users, self.needed_confirm))
class BCY(discord.ui.View):
    def __init__(self, users) -> None:
        super().__init__(timeout=None)
        self.nb_users: int = len(users)
        self.needed_confirm: int = (self.nb_users // 2) + 1
        self.add_item(Choice(emoji="⭐", label_content="Cap Only", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Choice(emoji="🏙️", label_content="All Cities", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Generic_NO(label_content="OFF", list_users=users, needed_confirm=self.needed_confirm))
class Maps(discord.ui.View):
    def __init__(self, users) -> None:
        super().__init__(timeout=None)
        self.nb_users: int = len(users)
        self.needed_confirm: int = (self.nb_users // 2) + 1
        self.add_item(Choice(emoji="🌋", label_content="Pangaeae", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Choice(emoji="🌊", label_content="7 Seas", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Choice(emoji="🌍", label_content="Continents", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Choice(emoji="⛵", label_content="Lakes", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Choice(emoji="🗺️", label_content="TSL (True Start Locations)", list_users=users, needed_confirm=self.needed_confirm))
class Barbarians(discord.ui.View):
    def __init__(self, users) -> None:
        super().__init__(timeout=None)
        self.nb_users: int = len(users)
        self.needed_confirm: int = (self.nb_users // 2) + 1
        self.add_item(Choice(emoji="⚔️", label_content="Standard", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Choice(emoji="👔", label_content="Civilized", list_users=users, needed_confirm=self.needed_confirm))
        self.add_item(Generic_NO(label_content="OFF", list_users=users, needed_confirm=self.needed_confirm))

############ FONCTIONS ############
async def make_mapvote(interaction: discord.Interaction):
    author = interaction.user
    channel = author.voice.channel
    users = channel.members
    nb_users: int = len(users)
    message = ""
    i: int = 0
    while (i < nb_users):
        message = f"{message} {users[i].mention}"
        i += 1
    message = f"Let's vote !\n\n*{nb_users}* players in the game :\n{message}"
    await interaction.response.send_message(message)
    await interaction.followup.send("**BBG VERSION**", view=VersionBBG(users))
    await interaction.followup.send("**DRAFTS**", view=Drafts(users))
    await interaction.followup.send("**MAP**", view=Maps(users))
    await interaction.followup.send("**BALANCED CITY YIELDS (BCY)**", view=BCY(users))
    await interaction.followup.send("**RELIGIOUS VICTORY**", view=Religious(users))
    await interaction.followup.send("**BARBARIANS**", view=Barbarians(users))

async def make_generic_mapvote(interaction: discord.Interaction):
    channel : discord.TextChannel = interaction.channel
    await interaction.response.send_message(f"Let's vote @everyone !")
    message : discord.Message = await channel.send("**====================== BBG VERSION =======================**\n 🛠️ BBG **|** 🔎 BBG Beta")
    await message.add_reaction("🛠️")
    await message.add_reaction("🔎")
    message = await channel.send("**========================= DRAFTS =========================**\n ✅ YES **|** ❌ NO")
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    message = await channel.send("**========================== MAP ===========================**\n 🌋 Pangaeae **|** 🌊 7 Seas **|** 🌍 Continents **|** ⛵ Lakes **|** 🗺️ TSL (True Start Locations)")
    await message.add_reaction("🌋")
    await message.add_reaction("🌊")
    await message.add_reaction("🌍")
    await message.add_reaction("⛵")
    await message.add_reaction("🗺️")
    message = await channel.send("**=============== BALANCED CITY YIELDS (BCY) ===============**\n ⭐ All cities **|** 🏙️ Capital Only **|** ❌ Disabled")
    await message.add_reaction("⭐")
    await message.add_reaction("🏙️")
    await message.add_reaction("❌")
    message = await channel.send("**=================== RELIGIOUS VICTORY ====================**\n ✅ Enabled **|** ❌ Disabled")
    await message.add_reaction("✅")
    await message.add_reaction("❌")
    message = await channel.send("**======================= BARBARIANS =======================**\n ⚔️ Standard **|** 👔 Civilized **|** ❌ No Barbs")
    await message.add_reaction("⚔️")
    await message.add_reaction("👔")
    await message.add_reaction("❌")