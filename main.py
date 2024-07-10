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
from wordle import *

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

#=================== SLASH COMMANDES ====================
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
    embed = BotEmbed(title="SALUTATIONS", description=f"Bonjour maître {interaction.user.mention} !\nC'est un plaisir de faire votre connaissance !\n\nN'hésitez pas à faire appel à moi pour préparer vos parties de Civilization VI, jouer à Wordle ou garder une trace de vos résultats et de vos statistiques dans différent jeux.\n\nMon code est accessible [ici](https://github.com/Matezzi777/Bobby_le_gentil_robot).\n\nSi vous avez une idée pour m'améliorer, utilisez la commande ***/feedback*** pour faire une suggestion !")
    await interaction.response.send_message(embed=embed, ephemeral=True)

#Distribue des leaders de civilization vi aux joueurs présents dans le salon vocal
@bot.slash_command(guild_ids=SERVERS, name="civ_draft", description="Distribue aléatoirement des leaders aux joueurs dans le salon vocal.")
async def civ_draft(interaction: discord.Interaction,
                    nb_leaders = discord.Option(int, "Le nombre de leaders à distribuer à chaque joueur.", required=False, default=10)):
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

#Lance une partie de Wordle
@bot.slash_command(guild_ids=SERVERS, name="wordle", description="Lance une partie de Wordle.")
async def wordle(interaction: discord.Interaction, nb_lettres: int = discord.Option(int, "Le nombre de lettres du mot à deviner.", required=False, default=5), nb_essais: int = discord.Option(int, "Le nombre d'essais maximum pour deviner'.", required=False, default=6)):
    author : discord.Member = interaction.user
    print(f"COMMAND : /wordle used by @{author.name} in {interaction.guild.name} (#{interaction.channel.name})")
    #Trouve un mot du bon nombre de lettres
    mot: str = get_word(nb_lettres)
    print(f"    Mot à trouver : {mot}")
    #Affiche la grille
    embed = BotEmbed(title="WORDLE", description=f"Essayez de trouver ce mot de {nb_lettres} lettres en moins de {nb_essais} essais !")
    embed_content : list[str] = initialize_embed_content(nb_lettres, nb_essais)
    embed.add_field(name="", value=get_str_from_list(embed_content), inline=False)
    embed.add_field(name="", value=f"**Encore {nb_essais} essais.**", inline=False)
    #Affiche le message initial
    message = await interaction.response.send_message(embed=embed)
    i: int = 0
    while (i < nb_essais):
        #Attends pour une réponse
        guess: discord.Message = await bot.wait_for('message', check=lambda message: message.channel == interaction.channel)
        proposition: str = f"{guess.content.upper().strip()}"
        print(f"        Guess : {proposition} ({i+1}/{nb_essais})")
        #Vérifie la réponse
        new_line: str = check_guess_validity(proposition, mot)
        if (new_line == "MISSING"):
            embed_response = BotEmbed(title="MOT INTROUVABLE", colour=discord.Colour.red(), description=f"Le mot {proposition} n'est pas dans le dictionnaire. Vérifiez l'orthographe du mot.")
            await guess.delete()
            await interaction.followup.send(embed=embed_response,ephemeral=True)
        elif (new_line == "INVALIDE"):
            embed_response = BotEmbed(title="LONGUEUR INCORRECTE", colour=discord.Colour.red(), description=f"Vous recherchez une mot de {nb_lettres} lettres.\n'{proposition}' fait {len(proposition)} lettres.")
            await guess.delete()
            await interaction.followup.send(embed=embed_response, ephemeral=True)
        elif (new_line == "FOUND"):
            print("    VICTOIRE")
            new_embed = BotEmbed(title="WORDLE", description=f"Essayez de trouver ce mot de {nb_lettres} lettres en moins de {nb_essais} essais !")
            line: str = ""
            z: int = 0
            while (z < len(proposition)):
                line = f"{line}🟩 "
                z = z + 1
            embed_content[i] = f"{line} --- {mot}"
            new_embed.add_field(name="", value=get_str_from_list(embed_content), inline=False)
            embed_response = BotEmbed(title="MOT TROUVÉ", colour=discord.Colour.green(), description=f"Félicitations ! Vous avez trouvé le mot {mot} en {i+1} essais !")
            await guess.delete()
            await message.edit(embed=new_embed)
            return await interaction.followup.send(embed=embed_response)
        else:
            new_embed = BotEmbed(title="WORDLE", description=f"Essayez de trouver ce mot de {nb_lettres} lettres en moins de {nb_essais} essais !")
            embed_content[i] = new_line
            new_embed.add_field(name="", value=get_str_from_list(embed_content), inline=False)
            new_embed.add_field(name="", value=f"**{nb_essais-i-1} essais restants.**", inline=False)
            await guess.delete()
            await message.edit(embed=new_embed)
            i = i + 1
    print("    DÉFAITE")
    embed_response = BotEmbed(title="WORDLE", colour=discord.Colour.red(), description=f"GAME OVER ! Le mot à trouver était {mot}.")
    return await interaction.followup.send(embed=embed_response)

#==================== USER COMMANDES ====================

#================== MESSAGES COMMANDES ==================
#Répète un message
@bot.message_command(guild_ids=SERVERS, name="repeat")
async def repeat(interaction : discord.Interaction, message : discord.Message):
    print(f"MESSAGE COMMAND : Repeat used by @{interaction.user.name} in {interaction.guild.name} (#{interaction.channel.name})")
    embed = BotEmbed(title="REPEAT", description=f"{message.created_at}")
    embed.add_field(name=f"", value=f"**{message.author.mention} said :**\n{message.content}")
    return await interaction.response.send_message(embed=embed)

#Traduis un message

#========================= RUN ==========================
bot.run(TOKEN)