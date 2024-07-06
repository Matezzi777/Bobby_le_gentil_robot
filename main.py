#	     ____     ______  ____     ____    __  __          __       ______          ____     ______  ____     ______  ________
#	    / __ |   / __  / / __ |   / __ |  / / / /         / /      / ____/         / __ |   / __  / / __ |   / __  / /__  ___/
#	   / /_/ /  / / / / / /_/ /  / /_/ / / /_/ /         / /      / /_            / /_/ /  / / / / / /_/ /  / / / /    / /
#	  / ___ |  / / / / / ___ |  / ___ |  |__  /         / /      / __/           / __  /  / / / / / ___ |  / / / /    / /
#	 / /__/ / / /_/ / / /__/ / / /__/ /    / /         / /____  / /___          / /  | | / /_/ / / /__/ / / /_/ /    / /
#	/______/ /_____/ /______/ /______/    /_/         /______/ /_____/         /_/  /_/ /_____/ /______/ /_____/    /_/

#==================== INITIALISATION ====================
import discord
import discord.ui
from classes import Bot, BotEmbed
from config import TOKEN

bot = Bot()
serveurs = [689646413788872718, 1212545993455964180]

#====================== CONSTANTES ======================

#======================== EVENTS ========================
@bot.event
async def on_ready():
    print("         ____     ______  ____     ____    __  __          __       ______          ____     ______  ____     ______  ________")
    print("        / __ |   / __  / / __ |   / __ |  / / / /         / /      / ____/         / __ |   / __  / / __ |   / __  / /__  ___/")
    print("       / /_/ /  / / / / / /_/ /  / /_/ / / /_/ /         / /      / /_            / /_/ /  / / / / / /_/ /  / / / /    / /")
    print("      / ___ |  / / / / / ___ |  / ___ |  |__  /         / /      / __/           / __  /  / / / / / ___ |  / / / /    / /")
    print("     / /__/ / / /_/ / / /__/ / / /__/ /    / /         / /____  / /___          / /  | | / /_/ / / /__/ / / /_/ /    / /")
    print("    /______/ /_____/ /______/ /______/    /_/         /______/ /_____/         /_/  /_/ /_____/ /______/ /_____/    /_/")
    return print(f"\n... est connecté.\nRock n'Roll !")

#====================== COMMANDES =======================

@bot.slash_command(guild_ids=serveurs, name="ping", description="PONG !")
async def ping(interaction: discord.Interaction):
    embed = BotEmbed(title="PONG", colour=discord.Colour.green())
    embed.remove_footer()
    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.slash_command(guild_ids=serveurs, name="hello", description="Dis bonjour !")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!\nThis is a slash command!", ephemeral=True)

#========================= RUN ==========================
bot.run(TOKEN)