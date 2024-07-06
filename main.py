#	     ____     ______  ____     ____    __  __          __       ______          ____     ______  ____     ______  ________
#	    / __ |   / __  / / __ |   / __ |  / / / /         / /      / ____/         / __ |   / __  / / __ |   / __  / /__  ___/
#	   / /_/ /  / / / / / /_/ /  / /_/ / / /_/ /         / /      / /_            / /_/ /  / / / / / /_/ /  / / / /    / /
#	  / ___ |  / / / / / ___ |  / ___ |  |__  /         / /      / __/           / __  /  / / / / / ___ |  / / / /    / /
#	 / /__/ / / /_/ / / /__/ / / /__/ /    / /         / /____  / /___          / /  | | / /_/ / / /__/ / / /_/ /    / /
#	/______/ /_____/ /______/ /______/    /_/         /______/ /_____/         /_/  /_/ /_____/ /______/ /_____/    /_/

# IDÉES
# REPORT DES PARTIES (différent jeux pris en charge)
# HISTORIQUE DES PARTIES JOUEES (différent jeux pris en charge)
# STATISTIQUES (différents jeux pris en charge et stats liées au serveur)

#==================== INITIALISATION ====================
import discord
import discord.ui
from classes import Bot, BotEmbed, FeedbackForm
from config import TOKEN, SERVERS
from draft import *

bot = Bot()

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
    return print(f"\n... est connecté.\nRock n'Roll !\n")

#====================== COMMANDES =======================
#Renvoit PONG si le bot est connecté
@bot.slash_command(guild_ids=SERVERS, name="ping", description="PONG !")
async def ping(interaction: discord.Interaction):
    print(f"COMMAND : /ping used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    embed = BotEmbed(title="PONG", colour=discord.Colour.green())
    embed.remove_footer()
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Renvoit une présentation du bot
@bot.slash_command(guild_ids=SERVERS, name="hello", description="Dis bonjour !")
async def hello(interaction: discord.Interaction):
    print(f"COMMAND : /hello used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    embed = BotEmbed(title="SALUTATIONS", description=f"Bonjour maître {interaction.user.mention} !\nC'est un plaisir de faire votre connaissance !\n\nN'hésitez pas à faire appel à moi pour préparer vos parties de Civilization VI et garder une trace de vos résultats et de vos statistiques dans différent jeux.\n\nMon code est accessible ici : https://github.com/Matezzi777/Bobby_le_gentil_robot\n\nSi vous avez une idée pour m'améliorer, utilisez la commande ***/feedback*** pour faire une suggestion !")
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Distribue des leaders de civilization vi aux joueurs présents dans le salon vocal
@bot.slash_command(guild_ids=SERVERS, name="civ_draft", description="Distribue aléatoirement des leaders aux joueurs dans le salon vocal.")
async def civ_draft(interaction: discord.Interaction, nb_leaders : int = 10):
    print(f"COMMAND : /civ_draft used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    author = interaction.user
    if (not author.voice):
        print(f"    - ERREUR : Le joueur doit se trouver dans un salon vocal.")
        missing_voice_embed = BotEmbed(title=f"PLEASE JOIN A VOICE CHANNEL", description=f"Veuillez rejoindre un salon vocal avec les autres joueurs avant de réutiliser cette commande pour recevoir les drafts.")
        return await interaction.response.send_message(embed=missing_voice_embed, ephemeral=True)
    else:
        channel = author.voice.channel
        players = channel.members

    nb_players = len(players)
    if (nb_players < 2): #S'il n'y a pas assez de joueurs
        print(f"    - ERREUR : Nombre de joueurs insuffisant.")
        embed = BotEmbed(title=f"ERREUR", description=f"Au minimum 2 joueurs sont nécessaires pour générer une draft. Demandez aux autres joueurs de rejoindre votre salon vocal.", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif (nb_players > 25): #S'il y a trop de joueurs
        print(f"    - ERREUR : Nombre de joueurs trop élevé.")
        embed = BotEmbed(title=f"ERREUR", description=f"Les drafts ne supportent que 25 joueurs au maximum.", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif (nb_leaders > 15): #Si le nombre de leaders demandé est trop grand
        print(f"    - ERREUR : Nombre de leaders trop élevé.")
        embed = BotEmbed(title=f"ERREUR", description=f"Trop de leaders par joueur demandés (max. 15).", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    elif (nb_players * nb_leaders > 77): #S'il n'y a pas assez de leaders dans le jeu pour en fournir assez à chaque joueur
        print(f"    - ERREUR : Pas assez de leaders pour fournir tous les joueurs.")
        embed = BotEmbed(title=f"ERREUR", description=f"Le jeu ne comporte pas assez de leaders différents pour en fournir {nb_leaders} à {nb_players} joueurs.", colour=discord.Colour.red())
        return await interaction.response.send_message(embed=embed, ephemeral=True)
    else: #Si tous les paramètres sont valides
        message = ""
        i : int = 0
        while (i < len(players)):
            message = message + f"{players[i].mention} "
            i = i + 1
        draft = create_draft(nb_players, nb_leaders)
        embed_draft = BotEmbed(title="DRAFT", description=f"New draft for {nb_players} players with {nb_leaders} leaders by player.")
        i : int = 0
        while (i < nb_players):
            k : int = 0
            field_value : str = f"**{players[i].mention} :**\n"
            while (k < nb_leaders):
                field_value = field_value + f"{emote_from_id(draft[i*nb_leaders+k])} {leader_from_id(draft[i*nb_leaders+k])}\n"
                k = k + 1
            field_value = field_value[:-1]
            embed_draft.add_field(name=f"", value=field_value)
            i = i + 1
        print(f"    - SUCCES : Drafts distribuées.")
        await interaction.response.send_message(message)
        return await interaction.followup.send(embed=embed_draft)

#Renvoit un formulaire pour émettre des suggestions d'amélioration du bot
@bot.slash_command(guild_ids=SERVERS, name="feedback", description="Formulaire pour envoyer une suggestion d'amélioration.")
async def feedback(interaction: discord.Interaction):
    print(f"COMMAND : /feedback used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    await interaction.response.send_modal(FeedbackForm())

#========================= RUN ==========================
bot.run(TOKEN)