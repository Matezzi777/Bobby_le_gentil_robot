import discord
import discord.ui
from classes import *

class RPC_Player1View(discord.ui.View):
    def __init__(self, player2: discord.Member, channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.player2: discord.Member = player2
        self.channel: discord.TextChannel = channel
        self.add_item(RPC_Select1())

class RPC_Select1(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Make your choice..")
        self.add_option(label="Rock", value="R", description="Choose me !", emoji="✊"),
        self.add_option(label="Paper", value="P", description="No I'm better !", emoji="✋"),
        self.add_option(label="Scissors", value="S", description="I'm definitely your best option.", emoji="✌️"),
        self.add_option(label="Cancel", value="X", description="", emoji="❌")

    async def callback(self, interaction: discord.Interaction):
        choice_player1: str = self.values[0]
        if (choice_player1 == "X"):
            await interaction.response.edit_message(embed=ErrorEmbed(title="CHALLENGE CANCELED"), view=None)
            return self.view.stop()
        else:
            channel: discord.TextChannel = self.view.channel
            player1: discord.User = interaction.user
            player2: discord.Member = self.view.player2
            embed_player2 = BotEmbed(title=f"@{interaction.user.name.upper()} SENT YOU A CHALLENGE", description=f"**@{interaction.user.name}** sent you a **Rock Paper Scissors** challenge.")
            await player2.send(embed=embed_player2, view=RPC_Player2View(player1, player2, choice_player1, channel))
            embed = SuccessEmbed(title=f"CHALLENGE SENT TO @{player2.name.upper()}")
            await interaction.response.edit_message(embed=embed, view=None)
            return self.view.stop()


class RPC_Player2View(discord.ui.View):
    def __init__(self, player1: discord.User, player2: discord.Member, choice_player1: str, channel: discord.TextChannel):
        super().__init__(timeout=None)
        self.player1: discord.User = player1
        self.player2: discord.Member = player2
        self.choice_player1: str = choice_player1
        self.channel: discord.TextChannel = channel
        self.add_item(RPC_Select2())

class RPC_Select2(discord.ui.Select):
    def __init__(self):
        super().__init__(placeholder="Make your choice..")
        self.add_option(label="Rock", value="R", description="Choose me !", emoji="✊"),
        self.add_option(label="Paper", value="P", description="No I'm better !", emoji="✋"),
        self.add_option(label="Scissors", value="S", description="I'm definitely your best option.", emoji="✌️"),
        self.add_option(label="Cancel", value="X", description="", emoji="❌")

    async def callback(self, interaction: discord.Interaction):
        choice_player2: str = self.values[0]
        player1: discord.User = self.view.player1
        player2: discord.User = interaction.user
        if (choice_player2 == "X"):
            await player1.send(embed=ErrorEmbed(title=f"CHALLENGE REFUSED", description=f"**@{player2.name}** refused your **Rock Paper Scissors** challenge."), view=None)
            await interaction.response.edit_message(embed=ErrorEmbed(title="CHALLENGE CANCELED", description=f"You canceled the **Rock Paper Scissors** challenge sent by **@{player1.name}**"), view=None)
            return self.view.stop()

        else:
            choice_player1: str = self.view.choice_player1
            channel: discord.TextChannel = self.view.channel
            embeds_description: str = f"**@{player1.name}** {get_rpc_emote_from_choice(choice_player1)} - {get_rpc_emote_from_choice(choice_player2)} **@{player2.name}**"
            if (choice_player1 == choice_player2):
                tie_embed = BotEmbed(title="IT'S A DRAW", description=embeds_description)
                await player1.send(embed=tie_embed, view=None)
                await channel.send(embed=tie_embed, view=None)
                await interaction.response.edit_message(embed=tie_embed, view=None)
                return self.view.stop()

            else:
                win_embed = SuccessEmbed(title="YOU WON", description=embeds_description)
                neutral_embed = BotEmbed(title="ROCK PAPER SCISSORS", description=embeds_description)
                lose_embed = ErrorEmbed(title="YOU LOST", description=embeds_description)
                if (choice_player1 == "R"):
                    if (choice_player2 == "P"):
                        neutral_embed.add_field(name="Winner :", value=f"**@{player2.name}**", inline=False)
                        await player1.send(embed=lose_embed, view=None)
                        await channel.send(embed=neutral_embed, view=None)
                        await interaction.response.edit_message(embed=win_embed, view=None)
                        return self.view.stop()

                    elif (choice_player2 == "S"):
                        neutral_embed.add_field(name="Winner :", value=f"**@{player1.name}**", inline=False)
                        await player1.send(embed=win_embed, view=None)
                        await channel.send(embed=neutral_embed, view=None)
                        await interaction.response.edit_message(embed=lose_embed, view=None)
                        return self.view.stop()

                    else:
                        print(f"    ERROR : A supposed impossible value for choice_player2 happened... ({choice_player2})")
                        await player1.send(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                        await interaction.response.edit_message(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                        return self.view.stop()

                elif (choice_player1 == "P"):
                    if (choice_player2 == "R"):
                        neutral_embed.add_field(name="Winner :", value=f"**@{player1.name}**", inline=False)
                        await player1.send(embed=win_embed, view=None)
                        await channel.send(embed=neutral_embed, view=None)
                        await interaction.response.edit_message(embed=lose_embed, view=None)
                        return self.view.stop()

                    elif (choice_player2 == "S"):
                        neutral_embed.add_field(name="Winner :", value=f"**@{player2.name}**", inline=False)
                        await player1.send(embed=lose_embed, view=None)
                        await channel.send(embed=neutral_embed, view=None)
                        await interaction.response.edit_message(embed=win_embed, view=None)
                        return self.view.stop()

                    else:
                        print(f"    ERROR : A supposed impossible value for choice_player2 happened... ({choice_player2})")
                        await player1.send(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                        await interaction.response.edit_message(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                        return self.view.stop()

                elif (choice_player1 == "S"):
                    if (choice_player2 == "P"):
                        neutral_embed.add_field(name="Winner :", value=f"**@{player1.name}**", inline=False)
                        await player1.send(embed=win_embed, view=None)
                        await channel.send(embed=neutral_embed, view=None)
                        await interaction.response.edit_message(embed=lose_embed, view=None)
                        return self.view.stop()

                    elif (choice_player2 == "R"):
                        neutral_embed.add_field(name="Winner :", value=f"**@{player2.name}**", inline=False)
                        await player1.send(embed=lose_embed, view=None)
                        await channel.send(embed=neutral_embed, view=None)
                        await interaction.response.edit_message(embed=win_embed, view=None)
                        return self.view.stop()

                    else:
                        print(f"    ERROR : A supposed impossible value for choice_player2 happened... ({choice_player2})")
                        await player1.send(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                        await interaction.response.edit_message(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                        return self.view.stop()

                else:
                    print(f"    ERROR : A supposed impossible value for choice_player1 happened... ({choice_player1})")
                    await player1.send(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                    await interaction.response.edit_message(content="SOMETHING WEIRD HAPPENED ! CHECK THE LOGS !", view=None)
                    return self.view.stop()


def get_rpc_emote_from_choice(choice: str) -> str:
    if (choice == "R"):
        return ("✊")
    elif (choice == "P"):
        return ("✋")
    elif (choice == "S"):
        return ("✌️")
    else:
        return ("❔")