import discord
import discord.ui
from classes import *

class ReportView(discord.ui.View):
    def __init__(self, embed, players: list[discord.Member]):
        super().__init__(timeout=None)
        self.embed = embed
        self.players: list[discord.Member] = players
        self.result: list[discord.Member] = []
        self.add_item(SelectPlayer(self.players, 1))

class SelectPlayer(discord.ui.Select):
    def __init__(self, players: list[discord.Member], n: int):
        super().__init__(
            placeholder=f"Select the player as top{n}."
        )
        self.n = n
        for player in players:
            self.add_option(label=f"@{player.name}", value=f"{player.id}", description=f"Select @{player.name} as top{n}.")

    async def callback(self,  interaction: discord.Interaction):
        chosen_member: discord.Member = interaction.guild.get_member(int(self.values[0]))
        print(f"    {self.n} : @{chosen_member.name}")
        self.view.result.append(chosen_member)
        self.view.players.remove(chosen_member)
        embed_content: str = ""
        i: int = 1
        for user in self.view.result:
            embed_content = f"{embed_content}- **{i} :** {user.mention}\n"
            i += 1
        new_embed = BotEmbed(title="REPORT", description=embed_content)
        self.view.children.pop(0)
        self.view.clear_items()
        if (len(self.view.players)!=0):
            self.view.add_item(SelectPlayer(self.view.players, self.n + 1))
        else:
            self.view.add_item(ConfirmReportButton(self.view.result))
            self.view.add_item(RestartReportButton(interaction.user, self.view.result))
            self.view.add_item(CancelReportButton(interaction.user))
        await interaction.response.edit_message(embed=new_embed, view=self.view)

class ConfirmReportButton(discord.ui.Button):
    def __init__(self, result: list[discord.Member]):
        super().__init__(style=discord.ButtonStyle.green,
                         label="Confirm Report",
                         disabled=False,
                         emoji="✅")
        self.users: list[discord.Member] = result

    async def callback(self, interaction: discord.Interaction):
        embed_content: str = ""
        i: int = 1
        for user in self.users:
            embed_content = f"{embed_content}- {i} {user.mention}\n"
            i += 1
        result_embed = BotEmbed(title="REPORT", description="Result confirmed and stored in the database.", colour=discord.Colour.green())
        result_embed.add_field(name="", value=embed_content, inline=False)
        await interaction.response.edit_message(embed=result_embed, view=None)

class RestartReportButton(discord.ui.Button):
    def __init__(self, user: discord.Member, players: list[discord.Member]):
        super().__init__(style=discord.ButtonStyle.blurple,
                         label="Restart",
                         disabled=False,
                         emoji="♻️")
        self.user: discord.Member = user
        self.players: list[discord.Member]= players

    async def callback(self, interaction: discord.Interaction):
        embed = BotEmbed(title="REPORT", description=f"Please follow the process to complete the report of this game for *{len(self.players)} players*.")
        await interaction.response.edit_message(embed=embed, view=ReportView(embed, self.players))

class CancelReportButton(discord.ui.Button):
    def __init__(self, user: discord.Member):
        super().__init__(style=discord.ButtonStyle.red,
                         label="Cancel",
                         disabled=False,
                         emoji="✖️")
        self.user: discord.Member = user

    async def callback(self, interaction: discord.Interaction):
        cancel_embed = BotEmbed(title="REPORT CANCELED", description="Report attempt aborted. Please use */report* again if you finaly want to make a report.", colour=discord.Colour.red())
        await interaction.response.edit_message(embed=cancel_embed, view=None)