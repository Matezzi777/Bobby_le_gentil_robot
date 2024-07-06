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
#Renvoit PONG si le bot est connecté
@bot.slash_command(guild_ids=serveurs, name="ping", description="PONG !")
async def ping(interaction: discord.Interaction):
    embed = BotEmbed(title="PONG", colour=discord.Colour.green())
    embed.remove_footer()
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Renvoit une présentation du bot
@bot.slash_command(guild_ids=serveurs, name="hello", description="Dis bonjour !")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Bonjour maître {interaction.user.mention} !\nC'est un plaisir de faire votre connaissance!\n\nN'hésitez pas à faire appel à moi pour préparer vos parties de civilisation, garder une trace de vos résultats et de vos statistiques dans différent jeux.\n\nSi vous avez une idée pour m'améliorer, utilisez la commande ***/feedback*** pour faire une suggestion !", ephemeral=True)

#Distribue des leaders de civilization vi aux joueurs présents dans le salon vocal
@bot.slash_command(guild_ids=serveurs, name="civ_draft", description="Distribue aléatoirement des leaders aux joueurs dans le salon vocal.")
async def civ_draft(interaction: discord.Interaction):
    ...

#Renvoit un formulaire pour émettre des suggestions d'amélioration du bot
@bot.slash_command(guild_ids=serveurs, name="feedback", description="Formulaire pour envoyer une suggestion d'amélioration.")
async def feedback(interaction: discord.Interaction):
    ...

#========================= RUN ==========================
bot.run(TOKEN)